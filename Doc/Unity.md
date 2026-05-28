# Unity 模块地图

## 模块定位

Unity 模块记录 Unity 侧 harness 规则入口、执行边界和文档读取路径。当前仓库未暴露真实 Unity 运行时代码、场景、Prefab 或构建流程。

## 入口文件

| 类型 | 路径 | 作用 | 读取时机 |
|---|---|---|---|
| Codex 规则 | `Unity/AGENTS.md` | Unity 侧 Codex 受控执行规则 | Codex 执行 Unity 相关任务时 |
| Claude 规则 | `Unity/CLAUDE.md` | Unity 侧 Claude 受控执行规则 | Claude 执行 Unity 相关任务时 |

## 关键规则

- Unity 侧任务必须先有方案，再执行。
- 默认禁止直接修改 Animator Controller、Prefab 层级结构和 Scene 物体结构。
- 写入代码时必须保持职责边界清晰，必要时按已确认方案拆分脚本。
- 中文文档读写必须显式使用 UTF-8。
- 变更记录写入 `Doc/ChangeLog/ChangeLog_YYYY-MM.md`，默认不读取历史日志。

## 事实清单

| 事实 | 来源 |
|---|---|
| Unity 侧存在 Codex 和 Claude 两套 harness 规则文件 | `Unity/AGENTS.md`、`Unity/CLAUDE.md` |
| Unity 侧规则定义受控代码执行代理职责 | `Unity/AGENTS.md`、`Unity/CLAUDE.md` |
| Unity 侧规则要求方案确认后再执行 | `Unity/AGENTS.md`、`Unity/CLAUDE.md` |
| Unity 运行时架构未在当前文档中证明 | `Doc/AI_Understanding.md` |

## 常见任务路由

| 任务 | 先读 | 修改边界 | 验证方式 |
|---|---|---|---|
| 调整 Unity 侧执行规则 | `Doc/Unity.md` -> `Unity/AGENTS.md` -> `Unity/CLAUDE.md` | 只改规则文档和必要项目文档 | 对比 `AGENTS.md` 与 `CLAUDE.md` 差异 |
| Unity 代码或资源任务 | `Doc/Unity.md` -> `Unity/AGENTS.md` | 未确认方案前不执行；Scene/Prefab/Animator 需权限确认 | 按已确认方案验证 |

## 不默认读取

- `Doc/ChangeLog/`
- 与当前任务无关的 Cocos 或 Skill 文档

## UNKNOWN

- 实际 Unity 运行时代码结构是 `UNKNOWN`。
- 实际 Unity Scene、Prefab、Animator、构建流程和资源布局是 `UNKNOWN`。
