# forguncy-plugin-expert

This is a distribution package for the forguncy-plugin-expert skill.

## Installation

### 1. General Installation
To install this skill locally for most agents:

```bash
npx skills add . --skill forguncy-plugin-expert
```

### 2. Specific Agent Installation (Recommended)
To ensure the skill is correctly recognized by your specific AI tool, add the `--agent` flag:

**For Claude Code:**
```bash
npx skills add . --skill forguncy-plugin-expert --agent claude-code
```

**For Cursor:**
```bash
npx skills add . --skill forguncy-plugin-expert --agent cursor
```

**For VS Code / Copilot:**
```bash
npx skills add . --skill forguncy-plugin-expert --agent vscode
```

> **Note**: If your agent is not listed above, check the [official documentation](https://github.com/microsoft/skills) or try installing without the `--agent` flag to use the default shared location.

### Troubleshooting
If the skill is installed but not visible in your tool (e.g., Claude Code), it might be installed in a generic location. Try reinstalling with the explicit `--agent` flag as shown above.
