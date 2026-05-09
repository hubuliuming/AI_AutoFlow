你的职责只有三件事：

1. 根据用户提词生成方案
2. 基于已确认方案执行
3. 将真实改动同步回项目文档

---

## Skill 同步规则

每当修改 `Com/Skill/` 下任意 Skill 内容时，必须同步修改 Codex 客户端侧对应 Skill。

默认同步目标：

- `C:\Users\song\.codex\skills\<skill-name>\`

同步范围：

- `SKILL.md`
- `agents/openai.yaml`
- 该 Skill 下实际存在的 `scripts/`、`references/`、`assets/` 等资源

执行要求：

1. 先确认项目内被修改的 Skill 名称与路径
2. 再确认 Codex 客户端侧对应 Skill 路径是否存在
3. 将项目内 Skill 的真实改动同步到客户端侧对应 Skill
4. 同步后检查项目内 Skill 与客户端侧 Skill 的差异
5. 最后同步更新项目文档

阻断条件：

- 客户端侧 Skill 路径不存在
- 同步目标不明确
- 写入客户端侧路径需要额外权限且未获确认
- 项目内 Skill 与客户端侧 Skill 结构不兼容

遇到阻断时必须停止，并输出：

- 【阻断原因】
- 【需要确认】
