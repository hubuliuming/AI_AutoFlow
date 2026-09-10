# AI 项目导航总图

> AI_AutoFlow 是一个围绕 Unity 项目协作、AI 文档理解和本地 Skill 管理组织的工程仓库。

## 0. 使用规则

- 默认先读取本文件，用它判断下一步应该读取哪些文档。
- 只在任务命中对应领域时读取模块文档，不默认展开所有文档。
- `Doc/ChangeLog/` 是冷层历史记录，默认不读取。
- 只有追溯历史、解释既有变更、排查回归或用户明确要求时，才读取 `Doc/ChangeLog/`。
- `Doc/Decisions/` 仅用于架构级决策记录；当前不存在该目录，普通变更不得为了形式创建 ADR。
- 未在项目文档、已确认方案或真实文件中证明的信息一律视为 `UNKNOWN`。

## 1. 快速路由表

| 用户问题类型 | 先读文档 | 再读文档 | 默认不读 |
|---|---|---|---|
| 项目整体理解 | `Doc/AI_Understanding.md` | `README.md` | `Doc/ChangeLog/` |
| Unity 侧执行规则 | `Doc/Unity.md` | `Unity/AGENTS.md` 或 `Unity/CLAUDE.md` | `Doc/ChangeLog/` |
| Cocos 侧执行规则 | `Doc/Cocos.md` | `Cocos/AGENTS.md` 或 `Cocos/CLAUDE.md` | `Doc/ChangeLog/` |
| Codex 编写或修改 Cocos 代码 | `Doc/Cocos.md` | `Cocos/AGENTS.md` -> `Cocos/CodeRule.md` | `Doc/ChangeLog/` |
| Skill 创建、更新或同步 | `Doc/Skills.md` | `AGENTS.md`、`Com/Skill/<skill-name>/SKILL.md` | 历史日志 |
| 变更历史追溯 | `Doc/ChangeLog/README.md` | 对应月份 `Doc/ChangeLog/ChangeLog_YYYY-MM.md` | 不相关月份日志 |
| 架构级决策原因 | `Doc/AI_Understanding.md` | `Doc/Decisions/` 中对应 ADR（若存在） | `Doc/ChangeLog/` |

## 2. 文档索引

| 文档 | 职责 | 读取时机 | 默认读取 |
|---|---|---|---|
| `Doc/AI_Understanding.md` | AI 项目导航总图、路由表、全局事实与未知项 | 每次需要理解项目边界时 | 是 |
| `Doc/Unity.md` | Unity 侧规则入口、读取路径、边界和验证提示 | Unity 相关任务 | 按需 |
| `Doc/Cocos.md` | Cocos 侧规则入口、读取路径、边界和验证提示 | Cocos 相关任务 | 按需 |
| `Doc/Skills.md` | 本地 Skill 清单、同步规则和读取路径 | Skill 相关任务 | 按需 |
| `Doc/ChangeLog/README.md` | ChangeLog 目录规则和索引 | 需要追溯历史时 | 否 |
| `Doc/ChangeLog/ChangeLog_2026-05.md` | 2026-05 的真实变更记录 | 追溯 2026-05 变更时 | 否 |
| `README.md` | 外部使用者入口说明 | 需要仓库用途和协作概览时 | 否 |
| `AGENTS.md` | 根目录 Codex 协作规则和 Skill 同步规则 | 修改 Skill 或执行仓库级任务时 | 按需 |
| `Unity/AGENTS.md` | Unity 侧 Codex 执行约束 | Unity 侧 Codex 任务 | 按需 |
| `Unity/CLAUDE.md` | Unity 侧 Claude 执行约束 | Unity 侧 Claude 任务 | 按需 |
| `Cocos/AGENTS.md` | Cocos 侧 Codex 执行约束 | Cocos 侧 Codex 任务 | 按需 |
| `Cocos/CodeRule.md` | Cocos 代码结构、失败暴露和编写代码规范 | Codex 编写或修改 Cocos TypeScript / JavaScript 代码前 | 代码修改时必读 |
| `Cocos/CLAUDE.md` | Cocos 侧 Claude 执行约束 | Cocos 侧 Claude 任务 | 按需 |

## 3. 目录地图

| 路径 | 职责 | 读取时机 |
|---|---|---|
| `Doc/` | AI 面向的项目导航、模块地图和冷层历史记录 | 需要项目事实或文档索引时 |
| `Doc/ChangeLog/` | 按月拆分的真实变更记录 | 需要追溯历史时 |
| `Com/Skill/` | 项目内 Codex Skill | 修改或检查 Skill 时 |
| `Unity/` | Unity 侧项目区域和 harness 规则文档 | Unity 相关任务 |
| `Cocos/` | Cocos 侧项目区域、harness 规则文档和通用协议说明 | Cocos 相关任务 |
| `README.md` | 仓库外部说明 | 需要仓库概览时 |
| `AGENTS.md` | 根目录执行规则 | 仓库级执行或 Skill 同步任务 |
| `LICENSE` | 许可证文件 | 需要许可证信息时 |

## 4. 模块地图

| 模块 | 入口路径 | 模块文档 | 状态 | 可信来源 |
|---|---|---|---|---|
| 项目协作规则 | `AGENTS.md` | 本文件 | 已确认 | `AGENTS.md`、`README.md` |
| Unity 侧规则 | `Unity/AGENTS.md`、`Unity/CLAUDE.md` | `Doc/Unity.md` | 已确认 | `Unity/AGENTS.md`、`Unity/CLAUDE.md` |
| Cocos 侧规则 | `Cocos/AGENTS.md`、`Cocos/CLAUDE.md`、`Cocos/CodeRule.md` | `Doc/Cocos.md` | 已确认 | `Cocos/AGENTS.md`、`Cocos/CLAUDE.md`、`Cocos/CodeRule.md` |
| Skill 管理 | `Com/Skill/` | `Doc/Skills.md` | 已确认 | `AGENTS.md`、`Com/Skill/*/SKILL.md` |
| 变更记录 | `Doc/ChangeLog/` | `Doc/ChangeLog/README.md` | 已确认 | 已确认方案、当前文件结构 |

## 5. 推荐阅读路径

- 最小路径：`Doc/AI_Understanding.md`。
- 仓库级规则任务：`Doc/AI_Understanding.md` -> `AGENTS.md`。
- Unity 任务：`Doc/AI_Understanding.md` -> `Doc/Unity.md` -> `Unity/AGENTS.md` 或 `Unity/CLAUDE.md`。
- Cocos 任务：`Doc/AI_Understanding.md` -> `Doc/Cocos.md` -> `Cocos/AGENTS.md` 或 `Cocos/CLAUDE.md`。
- Codex 编写或修改 Cocos 代码：在上述 Cocos 阅读路径中，读取 `Cocos/AGENTS.md` 后必须继续读取 `Cocos/CodeRule.md`。
- Skill 任务：`Doc/AI_Understanding.md` -> `Doc/Skills.md` -> `AGENTS.md` -> `Com/Skill/<skill-name>/SKILL.md`。
- 历史追溯任务：`Doc/AI_Understanding.md` -> `Doc/ChangeLog/README.md` -> 对应月份日志。

## 6. 全局确认事实

- 仓库路径是 `C:\dev\U3D\AI_AutoFlow`。
- 仓库名是 `AI_AutoFlow`。
- `LICENSE` 文件存在。
- `README.md` 提供仓库用途、使用流程、目录结构、协作约定和 Skill 同步维护说明。
- 根目录 `AGENTS.md` 规定职责为根据用户提词生成方案、基于已确认方案执行、将真实改动同步回项目文档。
- 修改 `Com/Skill/` 下任意 Skill 内容时，必须同步到 Codex 客户端侧对应 Skill。
- `Com/Skill/init-ai-docs/` 存在，用于初始化或刷新中文 AI 导航文档。
- `Com/Skill/sync-harness/` 存在，用于同步 `AGENTS.md` 或 `AGENT.md` 与 `CLAUDE.md`。
- Unity 侧规则文件是 `Unity/AGENTS.md` 和 `Unity/CLAUDE.md`。
- Cocos 侧规则文件是 `Cocos/AGENTS.md` 和 `Cocos/CLAUDE.md`。
- `Cocos/AGENTS.md` 将代码结构、失败暴露和编写代码规范指向同目录的 `CodeRule.md`，要求代码编写或修改前必读。
- Unity 和 Cocos 侧变更记录应写入 `Doc/ChangeLog/ChangeLog_YYYY-MM.md`，默认不进入常规读取上下文。
- 当前项目文档采用冷热分层：导航和模块地图为热/温层，ChangeLog 为冷层。

## 7. 全局未知项

- 实际 Unity 运行时架构是 `UNKNOWN`。
- 实际 Unity 玩法、编辑器工具、构建流程和资源布局是 `UNKNOWN`。
- 实际 Cocos 运行时架构是 `UNKNOWN`。
- 实际 Cocos 玩法、编辑器工具、构建流程、资源布局和资源绑定状态是 `UNKNOWN`。
- 仓库用途除 `README.md` 已描述内容外仍是 `UNKNOWN`。
- 是否需要更多业务模块文档，取决于未来能否从真实文件证明明确模块边界。
