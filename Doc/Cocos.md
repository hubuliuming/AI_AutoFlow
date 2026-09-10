# Cocos 模块地图

## 模块定位

Cocos 模块记录 Cocos 侧 harness 规则入口、执行边界和文档读取路径。当前仓库存在一份通用后端协议说明，但该文档不自动构成当前 Cocos 项目的业务规则。

## 入口文件

| 类型 | 路径 | 作用 | 读取时机 |
|---|---|---|---|
| Codex 规则 | `Cocos/AGENTS.md` | Cocos 侧 Codex 受控执行规则 | Codex 执行 Cocos 相关任务时 |
| 代码规范 | `Cocos/CodeRule.md` | 代码结构、失败暴露、运行时代码性能和集合转换规范 | Codex 编写或修改 Cocos TypeScript / JavaScript 代码前必须读取 |
| Claude 规则 | `Cocos/CLAUDE.md` | Cocos 侧 Claude 受控执行规则 | Claude 执行 Cocos 相关任务时 |
| 通用说明 | `Cocos/CocosBackendProtocolGuide.md` | 通用 Cocos 后端协议组织说明 | 用户明确询问协议说明时 |

## 关键规则

- Cocos 侧任务必须先有方案，再执行。
- `AGENTS.md` 和 `CLAUDE.md` 只提供执行约束，不提供业务事实。
- `AGENTS.md` 要求编写或修改 Cocos TypeScript / JavaScript 代码前读取同目录的 `CodeRule.md`，并遵守其中适用的代码规范。
- 不得因为仓库中存在示例、说明或协议文档，就自动视为当前 Cocos 项目的业务规则。
- 修改 Scene、Prefab、Node、Animation、`.meta`、UUID、Bundle 或构建配置前必须先做权限确认。
- Cocos 运行时代码在保证正确性和已确认行为的前提下性能优先，禁止为未经证实的风险堆叠保护性代码。
- 变更记录写入 `Doc/ChangeLog/ChangeLog_YYYY-MM.md`，默认不读取历史日志。

## 事实清单

| 事实 | 来源 |
|---|---|
| Cocos 侧存在 Codex 和 Claude 两套 harness 规则文件 | `Cocos/AGENTS.md`、`Cocos/CLAUDE.md` |
| Cocos 侧规则定义受控执行代理职责 | `Cocos/AGENTS.md`、`Cocos/CLAUDE.md` |
| Codex 侧代码结构、失败暴露和编写代码规范集中在 `CodeRule.md`，由 `AGENTS.md` 强制指引读取 | `Cocos/AGENTS.md`、`Cocos/CodeRule.md` |
| Cocos 侧规则要求资源结构类修改先权限确认 | `Cocos/AGENTS.md`、`Cocos/CLAUDE.md` |
| `Cocos/CocosBackendProtocolGuide.md` 是通用说明，不自动成为当前项目业务事实 | `Cocos/AGENTS.md`、`Cocos/CocosBackendProtocolGuide.md` |

## 常见任务路由

| 任务 | 先读 | 修改边界 | 验证方式 |
|---|---|---|---|
| 调整 Cocos 侧执行规则 | `Doc/Cocos.md` -> `Cocos/AGENTS.md` -> `Cocos/CLAUDE.md` | 只改规则文档和必要项目文档 | 对比 `AGENTS.md` 与 `CLAUDE.md` 差异 |
| Codex 编写或修改 Cocos 代码 | `Doc/Cocos.md` -> `Cocos/AGENTS.md` -> `Cocos/CodeRule.md` | 按已确认方案和代码规范修改 | 检查规范符合性，按用户指定方式验收 |
| Cocos 资源或场景任务 | `Doc/Cocos.md` -> `Cocos/AGENTS.md` | 未权限确认前不改资源结构 | 按用户指定预览或验收方式 |
| 协议说明问题 | `Doc/Cocos.md` -> `Cocos/CocosBackendProtocolGuide.md` | 不自动外推到当前业务系统 | 核对用户问题与文档范围 |

## 不默认读取

- `Doc/ChangeLog/`
- 与当前任务无关的 Unity 或 Skill 文档

## UNKNOWN

- 实际 Cocos 运行时代码结构是 `UNKNOWN`。
- 实际 Cocos Scene、Prefab、Node、Animation、Bundle、构建配置和资源绑定状态是 `UNKNOWN`。
