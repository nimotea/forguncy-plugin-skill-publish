---
type: reference
module: ClientCommand
concepts: [Properties, Boolean, Color, Decimal, Enum, Font, Formula, Percentage, String, DisplayName, Category]
version: 8.0+
---

# 客户端命令基础属性指南

本文档详细介绍了活字格客户端命令插件开发中常用的基础属性类型及其配置方法。

## 0. 通用特性 (Common Attributes)

在定义任何属性时，建议使用 `[DisplayName]` 和 `[Category]` 特性来优化设计器中的显示效果。

*   **DisplayName**: 设置属性在设计器面板中显示的名称（支持中文）。
*   **Category**: 设置属性的分组名称，便于分类管理。

```csharp
using System.ComponentModel; // 必须引用
using GrapeCity.Forguncy.Plugin;

public class MyPluginCommand : Command
{
    [Category("视觉效果")]
    [DisplayName("动画时长")]
    public int AnimationDuration { get; set; }
}
```

> [UI]: 属性面板将显示 "视觉效果" 分组下的 "动画时长"。

---

## 1. 布尔属性 (BooleanProperty)

`bool` 类型的属性自动识别为复选框。

```csharp
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;
using System.ComponentModel;

public class MyPluginCommand : Command
{
    [DisplayName("是否可见")]
    public bool IsVisible { get; set; }
}
```

> [UI]: 设计器中显示为一个名为 "是否可见" 的复选框。

### 进阶控制
使用 `[BoolProperty]` 控制缩进级别。

```csharp
[DisplayName("启用确认")]
[BoolProperty(IndentLevel = 0)]
public bool EnableConfirmation { get; set; }

[DisplayName("自定义确认消息")]
[BoolProperty(IndentLevel = 1)]
public bool CustomMessage { get; set; }
```

> [UI]: "自定义确认消息" 会比 "启用确认" 向右缩进一级。

> **注意**：如果默认值为 `true`，必须添加 `[DefaultValue(true)]`。

---

## 2. 颜色属性 (ColorProperty)

用于选择颜色的属性。属性类型必须为 `string`。

```csharp
[ColorProperty]
[DisplayName("背景颜色")]
public string BackgroundColor { get; set; }
```

> [UI]: 设计器中显示为颜色选择器控件。

### 进阶控制
*   **支持无填充色**：`SupportNoFill = true`。
*   **支持半透明**：`SupportTranslucency = true` (v9.0.100.0+)。

```csharp
[ColorProperty(SupportNoFill = true, SupportTranslucency = true)]
[DisplayName("边框颜色")]
public string BorderColor { get; set; }
```

### JavaScript 处理
建议使用 `Forguncy.ConvertToCssColor`。

```javascript
class MyPluginCommand extends Forguncy.Plugin.CommandBase {
    execute() {
        const propValue = this.CommandParam.BorderColor;
        const cssColor = Forguncy.ConvertToCssColor(propValue);
        document.body.style.borderColor = cssColor;
    }
}
Forguncy.Plugin.CommandFactory.registerCommand("MyPlugin.MyPluginCommand, MyPlugin", MyPluginCommand);
```

---

## 3. 小数属性 (DecimalProperty)

`double` 类型的属性自动识别为小数输入框。

```csharp
[DisplayName("不透明度")]
public double Opacity { get; set; }
```

> [UI]: 设计器中显示为数字输入框。

### 进阶控制 (`DoublePropertyAttribute`)
*   **限制范围**：`Min` 和 `Max`。
*   **允许空值**：`AllowNull = true` (属性类型需为 `double?`)。

```csharp
[DoubleProperty(Min = 0, Max = 1)]
[DisplayName("缩放比例 (0-1)")]
public double Scale { get; set; }

[DoubleProperty(AllowNull = true, Watermark = "默认")]
[DisplayName("最大高度")]
public double? MaxHeight { get; set; }
```

---

## 4. 枚举属性 (EnumProperty)

枚举类型自动显示为下拉列表。

```csharp
public enum UserType
{
    [Description("学生")]
    Student,
    [Description("教师")]
    Teacher,
    [Description("工人")]
    Worker
}

public class MyPluginCommand : Command
{
    [DisplayName("选择角色")]
    public UserType Role { get; set; }
}
```

> [UI]: 设计器中显示包含 "学生"、"教师"、"工人" 的下拉列表。

### JavaScript 处理
```javascript
class MyPluginCommand extends Forguncy.Plugin.CommandBase {
    userTypeMap = {
        0: "学生",
        1: "教师",
        2: "工人",
    }
    execute() {
        const propValue = this.CommandParam.Role;
        alert(this.userTypeMap[propValue] || "未知");
    }
}
```

---

## 5. 字体属性 (FontProperty) (v9.1+)

用于选择字体。

```csharp
[FontFamilyProperty]
[DisplayName("字体")]
public string FontFamily { get; set; }
```

---

## 6. 公式属性 (FormulaProperty)

属性类型必须为 `object`。

```csharp
[FormulaProperty]
[DisplayName("输入值")]
public object InputValue { get; set; }
```

> [UI]: 设计器中显示为带有公式选择按钮的输入框。

### JavaScript 计算公式
使用 `this.evaluateFormula`。

```javascript
class MyPluginCommand extends Forguncy.Plugin.CommandBase {
    execute() {
        const formula = this.CommandParam.InputValue;
        const result = this.evaluateFormula(formula);
        alert(result);
    }
}
```

### 进阶配置
*   **备选列表**：`RecommendedValues = "A|B|C"`。
*   **多行输入**：`AcceptsReturn = true`。
*   **仅支持单元格引用**：`OnlySupportCell = true`。

**单元格引用处理**:
如果设置了 `OnlySupportCell = true`，可以使用 `getCellLocation` 和 `getCellByLocation` 操作单元格。

```javascript
class MyPluginCommand extends Forguncy.Plugin.CommandBase {
    execute() {
        const formula = this.CommandParam.InputValue; // 例如 "=A1"
        const cellLocation = this.getCellLocation(formula);
        const cell = Forguncy.Page.getCellByLocation(cellLocation);
        cell.setValue("Test");
    }
}
```

---

## 7. 百分比属性 (PercentageProperty) (v9.0+)

用于输入百分比，底层存储为 `double` (0-1)。

```csharp
[PercentageProperty]
[DisplayName("进度")]
public double Progress { get; set; }
```

---

## 8. 字符串属性 (StringProperty)

`string` 类型自动识别为文本输入框。

```csharp
[DisplayName("提示信息")]
public string Message { get; set; }
```

> [UI]: 设计器中显示为文本输入框。

### 进阶控制 (`TextPropertyAttribute`)
*   **水印**：`Watermark`。
*   **多行文本**：`AcceptsReturn = true`。
*   **多语言支持**：`CanSelectResource = true` (v10.0+)。

```csharp
[TextProperty(Watermark = "请输入...", AcceptsReturn = true, CanSelectResource = true)]
[DisplayName("详细描述")]
public string Description { get; set; }
```

### JavaScript 获取多语言资源
```javascript
class MyPluginCommand extends Forguncy.Plugin.CommandBase {
    execute() {
        let text = this.CommandParam.Description;
        // 获取当前语言对应的值
        text = this.getApplicationResource(text);
        alert(text);
    }
}
```
