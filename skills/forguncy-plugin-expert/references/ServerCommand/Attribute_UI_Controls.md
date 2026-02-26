# UI 控件与图标 (UI Controls & Icons)

本章节介绍用于控制属性在属性面板中显示样式的 Attribute，以及如何为插件设置图标。

## 1. 单选按钮组 [RadioGroupProperty]

默认的枚举属性或固定选项属性通常显示为下拉框。如果选项较少（如 2-4 个），使用单选按钮组（Radio Group）可以提供更好的交互体验。

### 代码示例

```csharp
public class MyPluginCommand : Command
{
    // 配合枚举使用
    [RadioGroupProperty]
    public MyEnum LogLevel { get; set; }
}

public enum MyEnum
{
    [Description("详细")]
    Verbose,
    [Description("普通")]
    Info,
    [Description("错误")]
    Error
}
```

或者配合 `RecommendedValues` 使用（如果是字符串类型）：

```csharp
[RadioGroupProperty]
[RecommendedValues("OptionA", "OptionB")]
public string Selection { get; set; }
```

## 2. 基础列表 [ListProperty]

用于简单数据类型的列表编辑。与 `[ObjectListProperty]` 不同，`[ListProperty]` 适用于 `List<string>`, `List<int>` 等基础类型。

### 代码示例

```csharp
[ListProperty]
[DisplayName("白名单 IP 列表")]
public List<string> IpWhitelist { get; set; }
```

设计器会提供一个简单的列表编辑器，允许用户添加/删除字符串项。

## 3. 图标设置 [Icon]

为插件命令设置图标，使其在设计器工具箱中更易识别。

### 步骤
1.  准备一个 16x16 或 32x32 像素的 PNG 图片。
2.  将图片添加到项目中，并将“生成操作”设置为 **“嵌入的资源” (Embedded Resource)**。
3.  使用 `[Icon]` 特性指定资源路径。

### 资源路径格式
`项目命名空间.文件夹名.图片名.png`

### 代码示例

```csharp
// 假设图片位于项目根目录的 Resources 文件夹下，项目命名空间为 MyPlugin
[Icon("MyPlugin.Resources.MyCommandIcon.png")]
public class MyPluginCommand : Command
{
    // ...
}
```

**注意**：如果路径不正确，图标将显示为默认齿轮。务必检查 Assembly 命名空间和文件夹层级。
