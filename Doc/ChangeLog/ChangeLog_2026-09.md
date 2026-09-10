# 2026-09 变更记录

## 2026-09-10

- 将 `Cocos/AGENTS.md` 中的“代码结构清晰”“失败暴露优先”和“编写代码规范”迁移至 `Cocos/CodeRule.md`，保留原规则含义及适用范围。
- 在 `Cocos/AGENTS.md` 中增加代码规范强制读取入口，并在标准执行流程中要求编写或修改 Cocos TypeScript / JavaScript 代码前先读取同目录的 `CodeRule.md`。
- 同步更新 `Doc/Cocos.md` 和 `Doc/AI_Understanding.md` 的代码规范入口、事实与阅读路径。
- 调整 `Cocos/CodeRule.md` 的失败暴露和保护性代码规则，新增批量处理与单项失败隔离规范：独立条目加载、实例化或初始化失败时记录错误并继续后续项，覆盖异步处理、失败项清理、成功状态登记和日志定位要求，并明确整批必要前提失效及整体一致性操作的边界。
- 同步更新 `Doc/Cocos.md` 的代码规范说明和批量失败处理约束。
