# AI Understanding

## Project Identity

- Repository path: `C:\dev\U3D\AI_AutoFlow`
- Repository name: `AI_AutoFlow`
- License file exists: `LICENSE`
- `README.md` exists and is currently empty.
- Visible project purpose: `UNKNOWN`

## Document Index

- `Doc/AI_Understanding.md`: project-level AI understanding entry document.
- `AGENTS.md`: root Codex collaboration rule document.
- `Unity/AGENTS.md`: Unity-side controlled execution rules.
- `Unity/CLAUDE.md`: Claude-side counterpart of Unity execution rules.

## Directory Map

- `.git/`: git repository metadata.
- `.idea/`: IDE metadata.
- `Com/Skill/`: local Codex skills.
- `Doc/`: AI-facing project documents.
- `Unity/`: Unity-side project area and harness instruction files.
- `README.md`: present but empty.
- `LICENSE`: project license file.

## Confirmed Facts

- Root `AGENTS.md` says the agent has three duties: generate a plan from the user prompt, execute based on a confirmed plan, and synchronize real changes back to project documents.
- Root `AGENTS.md` requires Codex client-side Skill synchronization whenever content under `Com/Skill/` is modified.
- `Unity/AGENTS.md` and `Unity/CLAUDE.md` define the Unity-side agent as a controlled code execution agent.
- Unity-side rules require a confirmed plan before execution.
- Unity-side rules require real changes to be synchronized back to project documents after execution.
- Unity-side rules require Chinese documents to be read and written with explicit UTF-8 encoding.
- `Com/Skill/sync-harness/` exists as a local Skill for synchronizing `AGENTS.md` or `AGENT.md` with `CLAUDE.md`.
- `Com/Skill/init-ai-docs/` exists as a local Skill for creating or updating AI-facing project understanding documents under `Doc/`.
- `Com/Skill/init-ai-docs/` has been synchronized to the Codex client-side Skill path `C:\Users\song\.codex\skills\init-ai-docs\`.

## Module Overview

- `Com/Skill`: contains local Codex skills.
  - `sync-harness`: synchronizes harness instruction files while preserving tool-specific differences.
  - `init-ai-docs`: initializes or refreshes `Doc/AI_Understanding.md` and optional module docs based on scanned project facts.
- `Unity`: contains Unity-side harness instruction documents. Runtime Unity assets, scripts, scenes, and prefabs are not visible in the current tracked file list.

## Current Strategy

- The project follows a plan-first workflow: no implementation work should start until a plan is confirmed.
- After execution, project documents must reflect only real changes that occurred.
- The AI understanding document is the project-level entry point for future AI agents.
- Module documents under `Doc/` should be created only when module boundaries are explicit and separate documentation improves AI understanding.
- Changes under `Com/Skill/` must be synchronized to the corresponding Codex client-side Skill under `C:\Users\song\.codex\skills\<skill-name>\` when the client-side target is confirmed.
- The current project-side and Codex client-side `init-ai-docs` Skill files are synchronized.

## Known Issues

- No documented active issues found.

## Unknowns

- Actual Unity runtime architecture is `UNKNOWN`.
- Actual gameplay, editor tooling, build process, and asset layout are `UNKNOWN`.
- Project purpose beyond the repository name is `UNKNOWN`.
- Whether additional module documents are needed beyond `AI_Understanding.md` is `UNKNOWN` until more project files or documented modules exist.
