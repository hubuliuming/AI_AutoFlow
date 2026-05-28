# Skills 模块地图

## 模块定位

Skills 模块记录项目内 Codex Skill 的入口、同步规则和读取路径。

## 入口文件

| 类型 | 路径 | 作用 | 读取时机 |
|---|---|---|---|
| 根规则 | `AGENTS.md` | 定义 Skill 同步规则 | 修改 `Com/Skill/` 时 |
| 初始化 AI 文档 Skill | `Com/Skill/init-ai-docs/SKILL.md` | 生成或更新 AI 导航文档 | 用户要求初始化或刷新 AI 文档时 |
| Harness 同步 Skill | `Com/Skill/sync-harness/SKILL.md` | 同步 `AGENTS.md` 或 `AGENT.md` 与 `CLAUDE.md` | 用户要求同步 harness 时 |

## 关键规则

- 修改 `Com/Skill/` 下任意 Skill 内容时，必须同步 Codex 客户端侧对应 Skill。
- 默认同步目标是 `C:\Users\song\.codex\skills\<skill-name>\`。
- 同步范围包括 `SKILL.md`、`agents/openai.yaml`，以及实际存在的 `scripts/`、`references/`、`assets/` 等资源。
- 同步后必须检查项目内 Skill 与客户端侧 Skill 的差异。

## 事实清单

| 事实 | 来源 |
|---|---|
| `Com/Skill/init-ai-docs/` 存在 | 文件扫描 |
| `Com/Skill/init-ai-docs/agents/openai.yaml` 存在 | 文件扫描 |
| `Com/Skill/sync-harness/` 存在 | `Doc/AI_Understanding.md` 既有事实 |
| 修改项目侧 Skill 后必须同步客户端侧 Skill | `AGENTS.md` |

## 常见任务路由

| 任务 | 先读 | 修改边界 | 验证方式 |
|---|---|---|---|
| 更新 `init-ai-docs` | `Doc/Skills.md` -> `AGENTS.md` -> `Com/Skill/init-ai-docs/SKILL.md` | 同步项目侧和客户端侧 Skill | 比较两个 Skill 目录差异 |
| 同步 harness | `Doc/Skills.md` -> `Com/Skill/sync-harness/SKILL.md` | 保留工具侧必要自指差异 | 使用文件对比检查 |

## 不默认读取

- `Doc/ChangeLog/`
- 与当前 Skill 无关的其他 Skill 资源

## UNKNOWN

- 除已扫描文件外，其他客户端侧 Skill 状态是 `UNKNOWN`。
