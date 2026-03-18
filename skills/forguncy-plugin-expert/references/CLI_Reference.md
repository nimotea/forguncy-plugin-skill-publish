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

3. **确认活字格安装路径**（含缓存机制）
   - 默认路径：`C:\Program Files\Forguncy 11`
   - 首先检查缓存文件：`forguncy-plugin-expert\.forguncy-path-cache.json`
   - 如果缓存存在且路径有效，使用缓存路径
   - 如果缓存无效，使用默认路径
   - **路径处理逻辑**：
     1. **验证阶段**：检查路径是否有效
        - **重点**：活字格 exe 在子目录中，验证时需要检查子目录
        - 首先检查用户提供的路径是否直接包含 `Forguncy.exe`
        - 如果没有，检查 `WebSite\designerBin\Forguncy.exe` 是否存在
        - 如果存在，说明路径有效（即使 exe 不在根目录）
        - 如果仍不存在，提示用户确认完整路径
        - **缓存路径验证同理**：缓存存的是 `Forguncy 11`，验证时要查 `Forguncy 11\WebSite\designerBin\Forguncy.exe`
     2. **传参阶段**：提取正确的路径传给 CLI
        - 用户输入：`C:\Program Files\Forguncy 12\WebSite\designerBin\Forguncy.exe`
        - 传给 CLI：`C:\Program Files\Forguncy 12`（提取到 `WebSite` 的父目录）
        - 用户输入：`C:\Program Files\Forguncy 12\WebSite`
        - 传给 CLI：`C:\Program Files\Forguncy 12`（直接是父目录）
        - **原因**：`forguncy-plugin-create` CLI 需要的是版本号目录，而不是 `designerBin` 子目录
   - **典型安装目录结构**：
     ```
     C:\Program Files\Forguncy 12\
     ├── WebSite\
     │   └── designerBin\
     │       └── Forguncy.exe  ← 实际可执行文件
     ```
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
  - **必须是完整的项目文件夹路径**，不是父目录
  - 如果用户只提供父目录，AI 需要拼接插件名称：
    - 用户输入：`d:\Code\ForguncySkillWorkSpace`
    - 插件名称：`QRCodeGenerator`
    - 传给 CLI：`d:\Code\ForguncySkillWorkSpace\QRCodeGenerator`

**智能默认值**：
- 用户提到"现代化"/"复杂 UI"/"前端工程化" → 自动采用 vue + ts
- 未指定类型 → 默认 celltype,command,servercommand
- 仅 --types 包含 celltype 时 --framework 和 --lang 才有意义

### Step 3: 执行创建命令

**[CRITICAL] 必须带参数执行**。无参数会启动 GUI 交互模式。

路径含空格时必须用双引号包裹。

### Step 4: 缓存路径更新（创建成功后）
- **只有当 CLI 返回退出码 0（创建成功）时，才写入缓存**
- **AI 必须执行**：创建或更新缓存文件 `forguncy-plugin-expert\.forguncy-path-cache.json`
- 缓存文件位置：`forguncy-plugin-expert\.forguncy-path-cache.json`（相对于 skill 根目录）
- **缓存内容**：存储的是传给 CLI 的路径（截取后的版本号目录），不是用户提供原始路径
- 缓存格式：
  ```json
  {
    "forguncyPath": "C:\\Program Files\\Forguncy 12",
    "lastUpdated": "2025-01-15T10:30:00Z"
  }
  ```
  - 示例：如果用户提供 `C:\...\Forguncy 12\WebSite\designerBin`，缓存存 `C:\...\Forguncy 12`
- **写入时机**：CLI 返回退出码 0 后，立即写入缓存，不要等待后续步骤
- 如果创建失败（退出码 1），不更新缓存，询问用户实际路径后重试

### Step 5: 退出码处理

| 退出码 | 含义 | 处理方式 |
|--------|------|----------|
| 0 | 成功 | 读取 stdout 获取生成路径 |
| 1 | 失败 | 读取 stderr 分析原因 |

**常见错误**：
- 路径已存在 → 询问用户换目录或先删除
- 找不到活字格 → 询问用户正确安装路径
- 其他错误 → 展示错误信息，协助排查

### Step 6: 构建项目

**[CRITICAL] 严禁手动进入前端目录执行 npm install / npm run build！**

.csproj 文件已预置 MSBuild PreBuild 事件自动处理。

只需在项目根目录执行：
```bash
dotnet build
```

前端依赖安装和编译由 MSBuild 自动触发完成。
