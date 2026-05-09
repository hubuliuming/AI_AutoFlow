---
name: sync-harness
description: Synchronize harness instruction files so AGENTS.md or AGENT.md and CLAUDE.md contain nearly identical rules. Use when the user says "同步harness", asks to sync harness rules, or asks to compare and reconcile AGENTS.md/AGENT.md with CLAUDE.md in the current workspace.
---

# Sync Harness

Use this skill to reconcile workspace harness instruction files while preserving tool-specific differences.

## Workflow

1. Locate the workspace root from the current working directory unless the user gives another path.
2. Find the source file: prefer `AGENTS.md`; if it is absent, check `AGENT.md`. If the user explicitly names `AGENT.md`, use that file instead.
3. Find `CLAUDE.md`.
4. If neither `AGENTS.md` nor `AGENT.md` exists, stop and report the missing source file.
5. Read the source file with explicit UTF-8 encoding.
6. If `CLAUDE.md` does not exist, create it with explicit UTF-8 encoding and exactly the same content as the source file.
7. If `CLAUDE.md` was created, skip semantic reconciliation and verify the diff for the actual files in use.
8. If `CLAUDE.md` already exists, read it with explicit UTF-8 encoding and compare the rule sets semantically, not only line by line:
   - Identify rules present only in `AGENTS.md` or `AGENT.md`.
   - Identify rules present only in `CLAUDE.md`.
   - Identify rules that conflict or have different priority language.
9. Apply only minimal, localized edits so both files carry the same general project rules.
10. Preserve legitimate harness-specific wording:
   - Keep Codex-specific tool names, channels, plugin behavior, and app directives in `AGENTS.md`.
   - Keep Claude-specific tool names, slash commands, agents, hooks, or Claude Code behavior in `CLAUDE.md`.
   - Do not force identical text when equivalent behavior requires different tool vocabulary.
11. Do not rewrite either existing document unless the user explicitly asks.
12. Do not add new policy that is absent from both files.
13. After editing or creating `CLAUDE.md`, run `git diff -- AGENTS.md CLAUDE.md` or `git diff -- AGENT.md CLAUDE.md`, depending on the source file in use. If both `AGENTS.md` and `AGENT.md` exist, include only the selected source file unless the user asks otherwise.

## Conflict Handling

Stop and ask for confirmation when:

- The two files give incompatible rules and neither side clearly has priority.
- A change would delete or weaken a safety, permission, testing, or documentation rule.
- The intended synchronization requires changing repository structure or generated resources.
- UTF-8 reading shows garbled text.
- Neither `AGENTS.md` nor `AGENT.md` exists, so there is no source content for `CLAUDE.md`.

Use this format when blocked:

```text
【阻断原因】
<specific reason>
【需要确认】
<specific decision needed>
```

## Editing Rules

- Use UTF-8 for all reads and writes.
- Keep edits scoped to `AGENTS.md`, `AGENT.md`, and `CLAUDE.md` unless the user confirms otherwise.
- Preserve existing heading style, ordering, and language where practical.
- Prefer adding the missing counterpart rule near the corresponding section.
- If the repository has its own instruction-file precedence rules, follow them.
