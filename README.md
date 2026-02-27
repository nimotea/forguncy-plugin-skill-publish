# forguncy-plugin-expert

这是 forguncy-plugin-expert 技能的发布版本。

## 安装指南

### 1. 在线安装 (推荐)
对于大多数用户，直接从 GitHub 安装即可：

```bash
npx skills add nimotea/forguncy-plugin-skill-publish
```

### 2. 本地安装 (开发者)
如果你克隆了本仓库，可以通过本地路径安装：

```bash
npx skills add /path/to/forguncy-plugin-skill-publish --skill forguncy-plugin-expert
```

### 3. 指定 Agent 安装
为了确保技能被你的 AI 工具正确识别，建议添加 `--agent` 参数。支持的工具列表请参考 [官方文档](https://www.npmjs.com/package/skills#available-agents)。

常用 Agent 示例：

**Claude Code:**
```bash
npx skills add nimotea/forguncy-plugin-skill-publish --agent claude-code
```

**Cursor:**
```bash
npx skills add nimotea/forguncy-plugin-skill-publish --agent cursor
```

**VS Code / Copilot:**
```bash
npx skills add nimotea/forguncy-plugin-skill-publish --agent vscode
```

**Trae:**
```bash
npx skills add nimotea/forguncy-plugin-skill-publish --agent trae
```

**OpenCode:**
```bash
npx skills add nimotea/forguncy-plugin-skill-publish --agent opencode
```

> **注意**: 如果安装后在工具中看不到技能，请尝试带上 `--agent` 参数重新安装。

## 卸载指南
如果你想移除该技能，可以运行：

```bash
npx skills remove forguncy-plugin-expert
```
