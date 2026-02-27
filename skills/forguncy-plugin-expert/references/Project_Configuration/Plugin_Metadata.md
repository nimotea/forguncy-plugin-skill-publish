# 插件发布元数据配置指南

在活字格插件开发中，正确的元数据配置对于插件的发布和管理至关重要。这些信息将直接显示在活字格设计器的插件管理界面以及插件市场中。

## 1. 核心元数据管理

活字格插件的元数据（如版本、作者、描述）通常分布在 `.csproj` 文件和 `PluginConfig.json`（可选但推荐）中。

### 1.1 推荐方案：以 PluginConfig.json 为准 (Source of Truth)

为了确保版本号和元数据的一致性，推荐将 `PluginConfig.json` 作为单一事实来源。在构建或打包前，确保其版本号已更新。

**PluginConfig.json 示例**:
```json
{
  "Version": "1.0.1",
  "Authors": "活字格插件大师",
  "Description": "这是一个功能强大的活字格插件..."
}
```

### 1.2 .csproj 配置

活字格插件项目基于标准的 .NET 项目结构，主要的元数据通过 `.csproj` 文件中的 `<PropertyGroup>` 进行配置。

#### 关键属性说明

| 属性            | 说明                                         | 示例                                     |
| :-------------- | :------------------------------------------- | :--------------------------------------- |
| **Description** | 插件的详细描述，显示在插件管理界面。         | `这是一个用于集成第三方支付的高级插件。` |
| **Authors**     | 插件作者。                                   | `活字格插件大师`                         |
| **Company**     | 公司名称。                                   | `活字格开发实验室`                       |
| **Version**     | 插件版本号，遵循 SemVer 规范。               | `1.0.0`                                  |
| **Product**     | 产品名称（通常与插件名一致或为所属产品线）。 | `Advanced Payment Plugin`                |
| **Copyright**   | 版权信息。                                   | `Copyright © 2024 MyCompany`             |
| **PackageIcon** | 插件包图标（在插件列表中显示）。             | `Icon.png`                               |
| **PackageTags** | 标签，有助于搜索（空格分隔）。               | `Forguncy Payment Integration`           |

### 示例代码

```xml
<PropertyGroup>
  <TargetFramework>net6.0</TargetFramework>
  <!-- 插件描述 -->
  <Description>这是一个功能强大的活字格插件，提供了...功能。</Description>
  <!-- 作者 -->
  <Authors>活字格插件大师</Authors>
  <!-- 公司 -->
  <Company>活字格开发实验室</Company>
  <!-- 版本号 -->
  <Version>1.0.0</Version>
  <!-- 产品名 -->
  <Product>MyAwesomePlugin</Product>
  <!-- 图标文件引用 (对应 ItemGroup 中的资源) -->
  <PackageIcon>icon.png</PackageIcon>
</PropertyGroup>
```

## 2. 插件图标配置

插件图标是用户识别插件的第一要素。

### 步骤 1: 准备图标文件
*   **格式**: 推荐使用 PNG 格式。
*   **尺寸**: 建议 128x128 像素或更高，以保证在高分屏下的显示效果。
*   **位置**: 将图标文件（如 `icon.png`）放置在项目根目录下。

### 步骤 2: 在 .csproj 中包含图标
你需要将图标文件作为资源包含在项目中，并将其打包路径 (`Pack`) 设置为 `true`，`PackagePath` 设置为根目录（即为空字符串或指定名称）。

```xml
<ItemGroup>
  <!-- Include the icon file -->
  <None Include="icon.png">
    <Pack>True</Pack>
    <PackagePath>\</PackagePath>
  </None>
</ItemGroup>
```

### 步骤 3: 关联图标属性
在 `<PropertyGroup>` 中通过 `<PackageIcon>` 属性引用该文件名。

```xml
<PropertyGroup>
  ...
  <PackageIcon>icon.png</PackageIcon>
  ...
</PropertyGroup>

> **🔔 重要提示：双重同步 (Dual Sync)**
> 开发者经常只更新了命令/单元格的 `[Icon]` 或 `.csproj` 中的 `PackageIcon`，而忽略了 `PluginConfig.json` 中的 `image` 字段。
> *   **表现差异**：`PluginConfig.json` 控制设计器插件列表中的图标，而 `[Icon]` 控制页面设计器左侧工具箱中的图标。
> *   **操作建议**：每次更新图标时，请务必同时检查 `PluginConfig.json`：
>     ```json
>     "image": "Resources/PluginLogo.png" // 确保此文件与你的主图标保持视觉一致
>     ```
```

## 4. 使用内置工具快速生成专业图标

为了提升开发效率并确保插件在设计器中的专业感，本项目内置了 Logo 生成工具 `generate_logo.py`。
该工具基于 `Pillow` 库，能够生成高质量、抗锯齿的圆角渐变 PNG 图标。

### 4.1 核心优势
- **高质量渲染**：支持抗锯齿 (Anti-aliasing)、渐变背景 (Gradient) 和圆角 (Rounded Corners)。
- **双尺寸输出**：一次运行同时生成 `PluginLogo.png` (100x100) 和 `CommandIcon.png` (16x16)，满足不同场景需求。
- **AI 友好设计**：支持通过 JSON 配置文件或命令行参数灵活注入创意（颜色、文字），实现“实现路径固定，创意由 AI 注入”。

### 4.2 调用方式
AI 助手或开发者可以通过以下命令生成图标：

```bash
# 简单模式：指定文字和颜色
python scripts/generate_logo.py --text "FP" --bg-start "#4E73DF" --bg-end "#224ABE"

# 高级模式：使用配置文件
python scripts/generate_logo.py --config my_logo_config.json
```

**命令行参数说明**：
- `--text`: 显示在图标上的文字（建议 2 个字母，如 "FP"）。
- `--bg-start`: 背景渐变起始颜色 (Hex)。
- `--bg-end`: 背景渐变结束颜色 (Hex)。
- `--config`: JSON 配置文件路径。

### 4.3 配置文件示例 (JSON)
AI 可以生成如下配置来控制 Logo 样式：

```json
[
  {
    "output_path": "PluginLogo.png",
    "size": [100, 100],
    "text": "AI",
    "font_size_ratio": 0.5,
    "bg_color_start": "#FF5733",
    "bg_color_end": "#C70039",
    "text_color": "#FFFFFF",
    "border_radius_ratio": 0.2
  },
  {
    "output_path": "CommandIcon.png",
    "size": [16, 16],
    "text": "AI",
    "font_size_ratio": 0.7,
    "bg_color_start": "#FF5733",
    "bg_color_end": "#C70039"
  }
]
```

### 4.4 自动生成产物
运行脚本后，将在当前目录（或指定路径）生成：
1.  **PluginLogo.png** (100x100)：用于 `PluginConfig.json` 的 `image` 字段，展示在插件管理列表。
2.  **CommandIcon.png** (16x16)：用于 C# 代码的 `[Icon]` 属性，展示在设计器工具箱（建议设置为 Embedded Resource）。

> **注意**：脚本依赖 `Pillow` 库，使用前请运行 `pip install Pillow`。

此外，**CommandIcon.png** 必须在 `.csproj` 中设置为嵌入资源 (`Embedded Resource`) 才能在 C# 代码中通过 Pack URI 引用：

```xml
<ItemGroup>
  <EmbeddedResource Include="Resources\CommandIcon.png" />
</ItemGroup>
```

## 4. 资源加载配置 (PluginConfig.json)

对于大型前端插件，合理组织 JS 文件及其加载顺序至关重要。

### 4.1 javascript 数组

`PluginConfig.json` 中的 `javascript` 数组定义了插件加载时引入的脚本文件。

**关键原则**：
-   **顺序敏感**：浏览器将按数组定义的顺序依次加载并执行脚本。
-   **依赖优先**：底层库、常量定义、工具类应排在业务逻辑（如继承 `CellTypeBase` 的类）之前。

**多文件加载示例**:
```json
{
  "javascript": [
    "Scripts/lib/thirdparty-lib.js",  // 1. 第三方库
    "Scripts/Common/Constants.js",    // 2. 常量定义 (MyPlugin.Constants)
    "Scripts/Common/Utils.js",        // 3. 工具类 (MyPlugin.Utils)
    "Scripts/CellTypes/Main.js"       // 4. 业务逻辑类 (继承基类)
  ]
}
```

### 4.2 css 数组

同理，`css` 数组用于管理插件的样式表。

```json
{
  "css": [
    "Resources/BaseStyle.css",
    "Resources/Theme.css"
  ]
}
```

## 5. 常见问题

### Q: 修改了 Description 但设计器中没更新？
A: 尝试重新构建项目，并确保在活字格设计器中卸载旧版插件后重新安装新编译的插件包（或 Zip/Dll）。

### Q: 版本号规则是什么？
A: 活字格插件版本号建议遵循 `主版本.次版本.补丁版本` (X.Y.Z) 的格式。升级插件时，确保新版本号高于旧版本号，活字格会自动处理更新。
