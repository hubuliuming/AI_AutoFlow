---
name: init-ai-docs
description: Use when the user says "初始化AI文档", asks to initialize or refresh Chinese AI navigation docs, or wants Codex to create or update Doc/AI_Understanding.md as a lightweight AI project map with module docs, reading routes, and cold ChangeLog storage under Doc/.
---

# 初始化 AI 文档

当用户要求“初始化AI文档”、刷新 `Doc/AI_Understanding.md`、生成 AI 快速理解项目的中文文档，或根据项目模块生成 `Doc/` 下的 AI 导航文档时，使用此 Skill。

## 核心定位

`Doc/AI_Understanding.md` 是 AI 项目导航总图，不是历史记录、方案文档或完整架构 spec。

它只负责：

- 使用规则
- 快速路由表
- 文档索引
- 目录地图
- 模块地图
- 推荐阅读路径
- 全局确认事实
- 全局未知项

详细事实写入对应模块文档；历史记录写入 `Doc/ChangeLog/`；架构级决策才写入 `Doc/Decisions/`。

## 文档冷热分层

- 热层：`Doc/AI_Understanding.md`，默认优先读取。
- 温层：`Doc/Unity.md`、`Doc/Cocos.md`、`Doc/Skills.md`、`Doc/Modules/<module>.md`，只在任务命中对应领域时读取。
- 冷层：`Doc/ChangeLog/`、`Doc/Decisions/`，默认不读取。

读取冷层的条件：

- 用户明确要求追溯历史。
- 需要解释既有变更原因。
- 需要排查回归。
- 当前任务明确依赖历史记录或架构决策。

## 文档语言规则

1. 所有写入 `Doc/` 的文档必须使用中文。
2. 专有名词、文件名、路径、类名、方法名、命令、配置键可以保留原文。
3. 无法从当前文件证明的信息写为 `UNKNOWN`。
4. 不允许为了完整而脑补项目目的、架构、运行流程或模块职责。
5. 读取和写入中文文档时必须显式使用 UTF-8。

## 扫描范围

从当前工作目录定位项目根目录，除非用户指定其他路径。

优先读取：

- `AGENTS.md`
- `AGENT.md`
- `CLAUDE.md`
- `README.md`
- `Doc/AI_Understanding.md`
- 与当前任务命中的 `Doc/<module>.md`
- `Com/Skill/`
- `Unity/`
- `Cocos/`

文件列表优先使用 `rg --files`；不可用时再使用平台递归文件列表。

默认不读取：

- `Doc/ChangeLog/` 下历史日志
- `Doc/Decisions/` 下 ADR
- 与当前任务无关的模块文档

## 文档集合

必须维护：

- `Doc/AI_Understanding.md`

按扫描结果维护：

- `Doc/Unity.md`：当存在 `Unity/` 时记录 Unity 侧规则、入口、边界和已确认事实。
- `Doc/Cocos.md`：当存在 `Cocos/` 时记录 Cocos 侧规则、入口、边界和已确认事实。
- `Doc/Skills.md`：当存在 `Com/Skill/` 时记录本地 Skill 信息和同步规则。
- `Doc/Modules/<模块名>.md`：仅当项目中存在边界明确的业务模块、系统模块或资源模块时创建。
- `Doc/ChangeLog/README.md`：当需要维护 ChangeLog 目录时记录读取和写入规则。
- `Doc/ChangeLog/ChangeLog_YYYY-MM.md`：按月份记录真实变更。
- `Doc/Decisions/ADR_YYYY-MM-DD_<slug>.md`：只有架构级决策需要记录原因、取舍和影响时才创建。

不要为空目录、不明确区域或无法证明职责的文件夹创建子模块文档。不要为了专业感创建空 ADR 或空模块文档。

## AI_Understanding.md 推荐结构

如果现有结构兼容，只更新受影响部分；否则使用以下中文结构：

```markdown
# AI 项目导航总图

> 一句话说明当前仓库是什么；无法证明就写 UNKNOWN。

## 0. 使用规则

## 1. 快速路由表

## 2. 文档索引

## 3. 目录地图

## 4. 模块地图

## 5. 推荐阅读路径

## 6. 全局确认事实

## 7. 全局未知项
```

`快速路由表` 必须使用表格，至少包含：

- 用户问题类型
- 先读文档
- 再读文档
- 默认不读

`文档索引` 必须使用表格，至少包含：

- 文档
- 职责
- 读取时机
- 默认读取

`模块地图` 必须使用表格，至少包含：

- 模块
- 入口路径
- 模块文档
- 状态
- 可信来源

## 模块文档推荐结构

每个模块文档使用以下中文结构：

```markdown
# <模块名> 模块地图

## 模块定位

## 入口文件

## 关键规则

## 事实清单

## 常见任务路由

## 不默认读取

## UNKNOWN
```

要求：

- `入口文件` 使用表格记录类型、路径、作用、读取时机。
- `事实清单` 使用表格记录事实和来源。
- `常见任务路由` 使用表格记录任务、先读、修改边界、验证方式。
- 模块文档只记录该模块相关事实，不重复粘贴总入口内容。

## ChangeLog 规则

使用目录而不是单文件：

```text
Doc/
  ChangeLog/
    README.md
    ChangeLog_YYYY-MM.md
```

规则：

- `Doc/ChangeLog/` 默认不读取。
- 默认写入当前月份 `ChangeLog_YYYY-MM.md`。
- 月度文件不存在时新建。
- 单月日志过大时，允许按领域拆分为 `ChangeLog_YYYY-MM_Unity.md`、`ChangeLog_YYYY-MM_Cocos.md` 等。
- ChangeLog 只记录真实发生的变更、执行记录和历史记录。
- ChangeLog 不写方案推演、未来计划、未发生事项或完整 spec。
- 当前事实、当前策略和已知问题仍写入对应项目文档或模块文档。

## Decisions 规则

`Doc/Decisions/` 是可选冷层目录。

只有满足以下任一条件时才创建 ADR：

- 存在架构级决策。
- 存在多个工程选项且需要记录取舍原因。
- 决策会影响未来较长时间的实现、维护或协作边界。

普通文档更新、规则措辞调整、小型代码落地和流水记录不得写 ADR。

## 项目体量评估规则

执行时必须先根据扫描结果评估项目体量，再决定文档分类数量。

评估维度：

- 顶层目录数量
- 可证明模块数量
- 关键文件数量
- 已有文档数量
- 单个模块内文件或职责是否明显过多
- 是否存在 Unity、Cocos、Skill、工具链、业务逻辑、资源结构等不同类型内容

体量判断：

- 小型项目：以 `Doc/AI_Understanding.md` 为总图，最多补充少量明确必要的模块文档。
- 中型项目：按明确顶层模块生成 `Doc/Skills.md`、`Doc/Unity.md`、`Doc/Cocos.md`、`Doc/Modules/<模块名>.md` 等。
- 大型项目：除顶层模块文档外，可继续按子系统、目录、功能域或资源类型拆分。

文档数量跟随项目真实规模动态调整。

## 单文档体量控制规则

1. `Doc/AI_Understanding.md` 只做导航总图和索引。
2. 如果某个文档开始覆盖多个职责明显不同的模块，应拆成多个子文档。
3. 如果某个模块文档明显过长，应继续按子系统、目录、功能域或资源类型拆分。
4. 拆分后必须在上一级文档保留索引和阅读路径。
5. 不为了减少文档数量而强行合并不同模块。
6. 不为了形式增加空文档或只有标题的文档。
7. 每个文档都必须有清晰边界：读者能知道它负责什么、不负责什么。

## 模块拆分规则

可以创建模块文档的情况：

- 存在独立顶层目录，且目录名表达明确职责。
- 已有文档明确说明模块职责。
- 文件结构显示稳定分组，例如多个同类 Skill、多个 Unity/Cocos 规则文档、明确命名的业务目录。

不得创建模块文档的情况：

- 目录为空。
- 只有零散文件，无法证明模块职责。
- 需要推测业务含义。
- 模块信息少到可以放在总入口的一行索引中。

## 工作流程

1. 使用显式 UTF-8 读取项目规则、README、已有 `Doc/` 文档和关键模块文件。
2. 扫描项目文件结构，识别可证明的模块边界。
3. 评估项目体量，决定文档分类数量。
4. 先规划文档集合：导航总图、模块地图、必要子模块、冷层 ChangeLog 或 Decisions。
5. 更新 `Doc/AI_Understanding.md` 为 AI 项目导航总图。
6. 创建或更新必要的模块文档。
7. 创建或更新 `Doc/ChangeLog/README.md` 和当前月份日志；不要默认读取历史月份。
8. 仅在确有架构级决策时创建或更新 `Doc/Decisions/`。
9. 每份文档只更新受影响部分，避免无关重写。
10. 检查 `git diff -- Doc`，确认中文正常且内容只包含真实扫描结果。
11. 如果本 Skill 自身发生修改，必须按项目 `AGENTS.md` 规则同步到 Codex 客户端侧 Skill。

## 输出要求

完成后用中文汇报：

- 创建或修改了哪些文档
- `AI_Understanding.md` 的导航总图变化
- 创建或更新了哪些模块文档
- ChangeLog 是否迁入 `Doc/ChangeLog/`
- 是否创建 ADR；如果没有，说明原因
- 项目体量判断和文档分类数量依据
- 记录了哪些关键事实
- 还保留哪些 `UNKNOWN`
- 是否检查了 UTF-8 读回、diff 和 Skill 同步差异

## 阻断条件

遇到以下情况必须停止并请求确认：

- 现有文档互相冲突，且无法判断优先级。
- 用户要求写入的信息无法从项目文件证明。
- UTF-8 读取或 diff 显示中文乱码。
- 用户要求拆分子模块文档，但当前项目结构无法证明模块边界。
- 需要写入 `Doc/` 之外的新文档位置。
- 修改 `Com/Skill/` 后客户端侧对应 Skill 路径不存在或结构不兼容。

阻断时使用：

```text
【阻断原因】
<具体原因>
【需要确认】
<需要用户确认的点>
```
