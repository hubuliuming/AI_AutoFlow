#!/usr/bin/env python3
"""Read-only Markdown inventory and navigation audit (Python 3.10+)."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

COLD = {'changelog', 'decisions'}
INLINE = re.compile(r'(!?)\[([^\]\n]*)\]\(\s*(<[^>\n]+>|(?:[^\s()\\]|\\.|\([^()]*\))+)(?:\s+["\'][^\n]*?["\'])?\s*\)')
REFERENCE = re.compile(r'(!?)\[([^\]\n]+)\](?:\[([^\]\n]*)\])?')
DEFINITION = re.compile(r'^ {0,3}\[([^\]]+)\]:\s*(<[^>]+>|\S+)')


def plain_lines(text, strip_inline=True):
    """Keep line numbers, but remove fenced blocks and inline code."""
    fence = None
    result = []
    for line in text.splitlines():
        match = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
                fence = None
            result.append('')
        elif match:
            fence = match[1]
            result.append('')
        else:
            result.append(re.sub(r'(`+).*?\1', '', line) if strip_inline else line)
    return result


def label_key(label):
    return ' '.join(label.split()).casefold()


def links(lines):
    definitions = {}
    for line in lines:
        match = DEFINITION.match(line)
        if match:
            definitions[label_key(match[1])] = match[2]
    for number, line in enumerate(lines, 1):
        if DEFINITION.match(line):
            continue
        for match in INLINE.finditer(line):
            yield number, match[3].strip('<>'), bool(match[1])
        remainder = INLINE.sub('', line)
        for match in REFERENCE.finditer(remainder):
            key = label_key(match[3] or match[2])
            if key in definitions:
                yield number, definitions[key].strip('<>'), bool(match[1])


def cold(path, root):
    return any(part.casefold() in COLD for part in path.relative_to(root).parts[:-1])


def safe_file(path, root):
    """Do not follow symlink files or symlink ancestor directories."""
    if not path.is_relative_to(root):
        return False
    return not any(p.is_symlink() for p in [path, *path.parents] if p.is_relative_to(root))


def scan(args):
    root = Path(args.docs).resolve()
    if not root.is_dir():
        raise ValueError('文档根目录不存在或不是目录')
    findings, inventory = [], []
    graph = defaultdict(set)
    duplicates = defaultdict(list)

    def note(kind, path, detail, line=None, severity='warning'):
        item = {'kind': kind, 'path': str(path.relative_to(root)), 'detail': detail, 'severity': severity}
        if line is not None:
            item['line'] = line
        findings.append(item)

    def inside(raw):
        path = root / raw
        if not safe_file(path, root) or not path.resolve().is_relative_to(root):
            raise ValueError('路径必须位于文档根目录内且不经过符号链接: ' + raw)
        return path.resolve()

    entries = [inside(x) for x in (args.entry or ['AI_Understanding.md'])]
    if args.scope:
        paths = sorted(set(inside(x) for x in args.scope))
        if any(p.suffix.lower() != '.md' or not p.is_file() for p in paths):
            raise ValueError('--scope 必须指向存在的 Markdown 文件')
        if not args.include_cold and any(cold(p, root) for p in paths):
            raise ValueError('检查冷文档需同时指定 --include-cold')
    else:
        paths = sorted(p for p in root.rglob('*') if p.suffix.lower() == '.md'
                       and safe_file(p, root) and p.is_file()
                       and not any(x.startswith('.') for x in p.relative_to(root).parts)
                       and (args.include_cold or not cold(p, root)))
        for entry in entries:
            if entry not in paths:
                note('missing_entry', entry, '入口不存在或被排除，不能证明导航完整', severity='error')

    for path in paths:
        try:
            data = path.read_bytes()
            text = data.decode('utf-8-sig')
        except (OSError, UnicodeError) as exc:
            note('read_error', path, str(exc), severity='error')
            continue
        is_cold = cold(path, root)
        module = path.parent == root / 'Modules' and path.with_suffix('').is_dir() and any(
            p.is_file() and safe_file(p, root) for p in path.with_suffix('').rglob('*.md'))
        role = 'entry' if path in entries else 'module' if module else 'topic'
        budget = {'entry': args.entry_kib, 'module': args.module_kib, 'topic': args.topic_kib}[role]
        inventory.append({'path': path.relative_to(root).as_posix(), 'bytes': len(data),
                          'role': 'cold' if is_cold else role, 'budget_kib': None if is_cold else budget})
        if not is_cold and len(data) > budget * 1024:
            note('oversize', path, f'{len(data) / 1024:.1f} KiB > {budget:g} KiB；评估职责边界')
        if '\ufffd' in text:
            note('replacement_character', path, '发现 U+FFFD，需核对原始编码', severity='error')
        for number, line in enumerate(text.splitlines(), 1):
            if len(line) > args.long_line:
                note('long_line', path, f'{len(line)} 字符', number)
        lines = plain_lines(text)
        for number, destination, is_image in links(lines):
            try:
                parsed = urlsplit(destination)
            except ValueError:
                note('unsupported_link', path, destination, number)
                continue
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            raw = re.sub(r'\\([() ])', r'\1', unquote(parsed.path))
            if raw.startswith(('/', '\\')):
                note('unsupported_link', path, '根相对路径需人工核对: ' + destination, number)
                continue
            target = (path.parent / raw).resolve()
            if not target.exists():
                note('broken_link', path, destination, number, 'error')
            elif not is_image and target in paths:
                graph[path].add(target)
        if not is_cold:
            block, start = [], 0
            # Duplicate candidates keep punctuation and numbers; only whitespace is ignored.
            for number, line in enumerate([*plain_lines(text, strip_inline=False), ''], 1):
                if line.strip() and not line.lstrip().startswith(('#', '|')) and not DEFINITION.match(line):
                    if not block:
                        start = number
                    block.append(line)
                else:
                    normalized = re.sub(r'\s+', '', '\n'.join(block))
                    if len(normalized) >= args.duplicate_chars:
                        key = hashlib.sha256(normalized.encode('utf-8')).hexdigest()
                        duplicates[key].append({'path': path.relative_to(root).as_posix(), 'line': start})
                    block = []

    if not args.scope and all(e in paths for e in entries):
        reachable, queue = set(), list(entries)
        while queue:
            node = queue.pop()
            if node not in reachable:
                reachable.add(node)
                queue.extend(graph[node] - reachable)
        for path in paths:
            if path not in reachable and not cold(path, root):
                note('unreachable_candidate', path, '未沿受支持的 Markdown 链接从入口到达；需人工核对导航形式')
    for occurrences in duplicates.values():
        if len(occurrences) > 1:
            first = occurrences[0]
            note('duplicate_candidate', root / first['path'], occurrences, first['line'])
    return {'root': str(root), 'mode': 'scoped' if args.scope else 'full',
            'reachability_checked': not args.scope and all(e in paths for e in entries),
            'inventory': inventory, 'counts': dict(Counter(x['kind'] for x in findings)),
            'findings': findings,
            'limitations': ['仅检查支持的 Markdown 本地文件链接；不验证锚点或远端 URL',
                            '重复与不可达均为候选；不证明语义冲突、迁移完整或运行验收']}


def positive(value):
    number = float(value)
    if not 0 < number < float('inf'):
        raise argparse.ArgumentTypeError('必须是有限正数')
    return number


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError('必须是正整数')
    return number


def main():
    parser = argparse.ArgumentParser(description='只读审计 AI 文档；报告输出到 stdout，不写文件')
    parser.add_argument('docs')
    parser.add_argument('--entry', action='append')
    parser.add_argument('--scope', action='append')
    parser.add_argument('--include-cold', action='store_true')
    parser.add_argument('--entry-kib', type=positive, default=8)
    parser.add_argument('--module-kib', type=positive, default=4)
    parser.add_argument('--topic-kib', type=positive, default=24)
    parser.add_argument('--long-line', type=positive_int, default=500)
    parser.add_argument('--duplicate-chars', type=positive_int, default=160)
    parser.add_argument('--limit', type=positive_int, default=20)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    try:
        report = scan(args)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"扫描 {len(report['inventory'])} 份文档；模式 {report['mode']}；只读报告")
        print(json.dumps(report['counts'], ensure_ascii=False))
        for item in report['findings'][:args.limit]:
            detail = str(item['detail'])
            print(f"{item['kind']} {item['path']}:{item.get('line', '-')} {detail[:300]}")
        if len(report['findings']) > args.limit:
            print('其余详情已省略；使用 --json 获取完整报告。')
        print('仅机械检查；重复、不可达需复核，不代表业务或运行验收。')
    return 1 if any(x['severity'] == 'error' for x in report['findings']) else 0


if __name__ == '__main__':
    raise SystemExit(main())
