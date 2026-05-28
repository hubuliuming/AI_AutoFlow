# ChangeLog 索引

## 职责

`Doc/ChangeLog/` 只记录真实发生的变更、执行记录和历史记录。

## 读取规则

- 默认不读取历史 ChangeLog。
- 只有追溯历史、解释既有变更、排查回归或用户明确要求时，才读取本目录。
- 先读本文件，再按月份读取对应 `ChangeLog_YYYY-MM.md`。
- 不读取与当前问题无关的月份日志。

## 写入规则

- 默认写入当前月份文件：`ChangeLog_YYYY-MM.md`。
- 月度文件不存在时新建。
- 单月日志过大时，允许按领域拆分为 `ChangeLog_YYYY-MM_Unity.md`、`ChangeLog_YYYY-MM_Cocos.md` 等文件。
- ChangeLog 不写方案推演、未来计划或未发生事项。
- ChangeLog 不替代 `Doc/AI_Understanding.md` 或模块文档中的当前事实。

## 当前索引

| 文件 | 范围 |
|---|---|
| `ChangeLog_2026-05.md` | 2026-05 真实变更记录 |
