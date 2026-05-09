---
name: init-ai-docs
description: Use when the user says "初始化AI文档", asks to initialize AI understanding docs, or wants Codex to create or update Doc/AI_Understanding.md and module docs that help future AI agents understand the current project quickly.
---

# Initialize AI Docs

Use this skill to create or update AI-facing project understanding documents under `Doc/`.

## Trigger

Run this skill when the user says:

- `初始化AI文档`
- asks to initialize AI docs
- asks to create or refresh `AI_Understanding.md`
- asks to generate project understanding docs for future AI work

## Core Rules

1. Locate the project root from the current working directory unless the user gives another path.
2. Read project instructions first:
   - root `AGENTS.md`
   - nested `AGENTS.md`
   - `CLAUDE.md`
   - existing files under `Doc/`
3. Read all Chinese or Markdown documents with explicit UTF-8 encoding.
4. Scan the project structure before writing:
   - top-level directories and files
   - `Com/Skill/`
   - `Unity/`
   - existing `Doc/`
   - git-tracked files when available
5. Create `Doc/AI_Understanding.md` if it does not exist.
6. If `Doc/AI_Understanding.md` exists, update only affected sections.
7. Write only facts found in files or directory structure.
8. If a detail cannot be proven from current files, write `UNKNOWN`.
9. Do not infer architecture, runtime behavior, or module purpose beyond documented facts.
10. Do not rewrite unrelated documents.

## Document Set

Always maintain:

- `Doc/AI_Understanding.md` as the project-level entry document.

Create module documents only when the scan finds a clear independent module or workflow that would make `AI_Understanding.md` too dense. Prefer these names when applicable:

- `Doc/Unity.md` for Unity-side project rules, assets, scripts, and execution constraints.
- `Doc/Skills.md` for local Codex skills under `Com/Skill/`.
- `Doc/Modules/<module-name>.md` for larger project modules, if a module boundary is explicit.

Do not create module documents for empty or unclear areas.

## AI_Understanding.md Shape

Use this structure unless the existing document already has a compatible shape:

```markdown
# AI Understanding

## Project Identity

## Document Index

## Directory Map

## Confirmed Facts

## Module Overview

## Current Strategy

## Known Issues

## Unknowns
```

Section meanings:

- `Project Identity`: repository name, visible purpose, license, readme state.
- `Document Index`: AI-facing docs and what each one covers.
- `Directory Map`: important directories and files.
- `Confirmed Facts`: facts directly found in files.
- `Module Overview`: modules discovered during the scan.
- `Current Strategy`: current execution or collaboration rules already documented.
- `Known Issues`: documented problems only.
- `Unknowns`: missing or unproven information.

## Workflow

1. Read project docs and existing AI docs with explicit UTF-8 encoding.
2. List files with `rg --files` if available; otherwise use the platform's recursive file listing.
3. Inspect only files needed to identify project structure and module boundaries.
4. Decide whether `Doc/AI_Understanding.md` alone is sufficient or module docs are warranted.
5. Write minimal, factual updates.
6. Run `git diff -- Doc Com/Skill/init-ai-docs` after editing.
7. If the diff shows garbled Chinese or unrelated rewrites, stop and report the issue.

## Output Requirements

After updating docs, report:

- files created or changed
- module docs created, if any
- facts recorded
- unknowns that remain
- whether `git diff` was checked

## Blocking Conditions

Stop and ask for confirmation when:

- existing docs conflict and neither source has clear priority
- the requested document would require inventing facts
- UTF-8 reading or diff output shows garbled Chinese
- module boundaries are unclear but the user asked for separate module docs

Use this format when blocked:

```text
【阻断原因】
<specific reason>
【需要确认】
<specific decision needed>
```
