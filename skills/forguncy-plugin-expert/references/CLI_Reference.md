# forguncy-plugin-create CLI 参考

## 调用格式
```bash
forguncy-plugin-create --name <PluginName> --types <types> [选项...]
```

## 参数说明

| 参数 | 说明 | 必须 | 默认值 |
|------|------|------|--------|
| `--name <name>` | 插件名称（必须是合法 C# 标识符） | 是 | MyPlugin |
| `--types <types>` | 类型，逗号分隔（celltype/command/servercommand） | 是 | celltype,command,servercommand |
| `--framework <fw>` | 前端框架：none/react/vue | 否 | none（强推 vue） |
| `--lang <lang>` | 前端语言：js/ts | 否 | js（强推 ts） |
| `--locale-name <name>` | 插件中文显示名称 | 否 | 同 --name |
| `--description <text>` | 插件描述 | 否 | 这是一个活字格插件 |
| `--forguncy-path <path>` | 活字格安装路径 | 否 | C:\Program Files\Forguncy 11 |
| `--plugin-path <path>` | 插件工程输出目录 | 否 | %USERPROFILE%\Documents\HZG-Plugins\ |

## 推荐命令

### Vue + TypeScript（强推）
```bash
forguncy-plugin-create --name WeatherWidget --types celltype,command,servercommand --framework vue --lang ts --locale-name 天气组件 --forguncy-path "C:\Program Files\Forguncy 12" --plugin-path "C:\MyPlugins\WeatherWidget"
```

### 纯后端（无前端）
```bash
forguncy-plugin-create --name MyServerCommand --types servercommand --forguncy-path "C:\Program Files\Forguncy 12"
```

## 工作流程

### Step 1: 环境预检

1. **检查 .NET SDK**
   ```bash
   dotnet --version
   ```
   未安装则引导用户安装 .NET SDK

2. **检查 CLI 工具**
   ```bash
   forguncy-plugin-create --help
   ```
   未安装则执行：
   ```bash
   dotnet tool install --global GrapeCity.Forguncy.PluginCreator --version 11.1.0
   ```
   更新（可选）：
   ```bash
   dotnet tool update --global GrapeCity.Forguncy.PluginCreator
   ```

3. **确认活字格安装路径**
   - 默认路径：`C:\Program Files\Forguncy 11`
   - 验证方法：检查该路径下是否存在 `Forguncy.exe`
   - 路径无效会导致创建失败

4. **Node.js 检查**（如果选择 Vue/React 框架）
   ```bash
   node --version
   ```
   需要 20.19+ 或 22.12+

5. **确认输出目录不存在**
   - 目录已存在会导致 CLI 报错（退出码 1）

### Step 2: 组装 CLI 参数

从用户需求中提取：
- 插件名称 → `--name`
- 插件类型 → `--types`
- 前端框架 → `--framework`（强推 vue）
- 前端语言 → `--lang`（强推 ts）
- 活字格路径 → `--forguncy-path`
- 输出路径 → `--plugin-path`

**智能默认值**：
- 用户提到"现代化"/"复杂 UI"/"前端工程化" → 自动采用 vue + ts
- 未指定类型 → 默认 celltype,command,servercommand
- 仅 --types 包含 celltype 时 --framework 和 --lang 才有意义

### Step 3: 执行创建命令

**[CRITICAL] 必须带参数执行**。无参数会启动 GUI 交互模式。

路径含空格时必须用双引号包裹。

### Step 4: 退出码处理

| 退出码 | 含义 | 处理方式 |
|--------|------|----------|
| 0 | 成功 | 读取 stdout 获取生成路径 |
| 1 | 失败 | 读取 stderr 分析原因 |

**常见错误**：
- 路径已存在 → 询问用户换目录或先删除
- 找不到活字格 → 询问用户正确安装路径
- 其他错误 → 展示错误信息，协助排查

### Step 5: 构建项目

**[CRITICAL] 严禁手动进入前端目录执行 npm install / npm run build！**

.csproj 文件已预置 MSBuild PreBuild 事件自动处理。

只需在项目根目录执行：
```bash
dotnet build
```

前端依赖安装和编译由 MSBuild 自动触发完成。
