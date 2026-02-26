---
type: reference
module: CellType
concepts: [Properties, Boolean, Color, Decimal, Enum, Font, Formula, Integer, Percentage, String, ListView, DoubleClick, DisplayName, Category]
version: 8.0+
---

# 单元格基础属性指南

本文档详细介绍了活字格插件开发中常用的基础属性类型及其配置方法。

## 0. 通用特性 (Common Attributes)

在定义任何属性时，建议使用 `[DisplayName]` 和 `[Category]` 特性来优化设计器中的显示效果。

*   **DisplayName**: 设置属性在设计器面板中显示的名称（支持中文）。
*   **Category**: 设置属性的分组名称，便于分类管理。

```csharp
using System.ComponentModel; // 必须引用
using GrapeCity.Forguncy.Plugin;

public class MyPluginCellType : CellType
{
    [Category("外观设置")]
    [DisplayName("背景颜色")]
    public string BackgroundColor { get; set; }

    [Category("行为设置")]
    [DisplayName("是否只读")]
    public bool IsReadOnly { get; set; }
}
```

> [UI]: 属性面板将显示 "外观设置" 分组下的 "背景颜色" 和 "行为设置" 分组下的 "是否只读"。

---

## 1. 布尔属性 (BooleanProperty)

默认情况下，`bool` 类型的属性会被自动识别为布尔属性，在设计器中显示为复选框。

```csharp
using GrapeCity.Forguncy.CellTypes;
using System.ComponentModel;

public class MyPluginCellType : CellType
{
    [DisplayName("启用功能")]
    public bool MyProperty { get; set; }
}
```

> [UI]: 设计器中显示为一个名为 "启用功能" 的复选框。

### 进阶控制
使用 `[BoolProperty]` 特性可以控制复选框的缩进级别，从而在属性面板中构建层次结构。

```csharp
using GrapeCity.Forguncy.CellTypes;

public class MyPluginCellType : CellType
{
    [DisplayName("启用高级选项")]
    [BoolProperty(IndentLevel = 0)]
    public bool EnableAdvanced { get; set; }

    [DisplayName("选项 A")]
    [BoolProperty(IndentLevel = 1)]
    public bool OptionA { get; set; }

    [DisplayName("选项 B")]
    [BoolProperty(IndentLevel = 1)]
    public bool OptionB { get; set; }
}
```

> [UI]: "选项 A" 和 "选项 B" 会比 "启用高级选项" 向右缩进一级，形成从属关系。

**说明**：
*   若未标注 `[BoolProperty]`，默认缩进等级为 1。
*   若标注了 `[BoolProperty]` 但未设置 `IndentLevel`，默认缩进等级为 0。

> **注意**：如果布尔属性默认值为 `true`，必须添加 `[DefaultValue(true)]`，否则可能导致属性值无法正确保存。

```csharp
[DefaultValue(true)]
[DisplayName("默认开启")]
public bool MyProperty { get; set; } = true;
```

---

## 2. 颜色属性 (ColorProperty)

用于选择颜色的属性。属性类型必须为 `string`。

```csharp
using GrapeCity.Forguncy.CellTypes;
using System.ComponentModel;

public class MyPluginCellType : CellType
{
    [ColorProperty]
    [DisplayName("字体颜色")]
    public string TextColor { get; set; }
}
```

> [UI]: 设计器中显示为颜色选择器控件。

### 进阶控制
*   **支持无填充色**：设置 `SupportNoFill = true`。
*   **支持半透明**：设置 `SupportTranslucency = true` (v9.0.100.0+)。

```csharp
[ColorProperty(SupportNoFill = true, SupportTranslucency = true)]
[DisplayName("背景颜色")]
public string BackgroundColor { get; set; }
```

### JavaScript 处理
活字格中的颜色分为普通颜色（ARGB Hex）和主题颜色（名称+引用）。运行时建议使用 `Forguncy.ConvertToCssColor` 转换为 CSS 颜色。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const propValue = this.CellElement.CellType.BackgroundColor;
        const cssColor = Forguncy.ConvertToCssColor(propValue);
        const div = $("<div>Text</div>");
        div.css("background-color", cssColor);
        return div;
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

---

## 3. 小数属性 (DecimalProperty)

`double` 类型的属性自动识别为小数属性。

```csharp
using GrapeCity.Forguncy.CellTypes;
using System.ComponentModel;

public class MyPluginCellType : CellType
{
    [DisplayName("缩放比例")]
    public double Scale { get; set; }
}
```

> [UI]: 设计器中显示为数字输入框。

### 进阶控制 (`DoublePropertyAttribute`)
*   **限制范围**：设置 `Min` 和 `Max`。
*   **允许空值**：设置 `AllowNull = true`，并将属性类型设为 `double?`。

```csharp
using GrapeCity.Forguncy.CellTypes;

public class MyPluginCellType : CellType
{
    // 限制范围
    [DoubleProperty(Min = 0, Max = 10)]
    [DisplayName("评分 (0-10)")]
    public double Score { get; set; }

    // 允许为空
    [DoubleProperty(AllowNull = true, Watermark = "无限制")]
    [DisplayName("可选阈值")]
    public double? Threshold { get; set; }
}
```

---

## 4. 整数属性 (IntegerProperty)

`int` 类型的属性自动识别为整数属性。

```csharp
using GrapeCity.Forguncy.CellTypes;
using System.ComponentModel;

public class MyPluginCellType : CellType
{
    [DisplayName("数量")]
    public int Count { get; set; }
}
```

> [UI]: 设计器中显示为整数输入框。

### 进阶控制 (`IntPropertyAttribute`)
*   **限制范围**：`Min` 和 `Max`。
*   **允许空值**：`AllowNull = true` (属性类型需为 `int?`)。

```csharp
using GrapeCity.Forguncy.CellTypes;

public class MyPluginCellType : CellType
{
    [IntProperty(Min = 1, Max = 100)]
    [DisplayName("页码")]
    public int PageIndex { get; set; }

    [IntProperty(AllowNull = true, Watermark = "默认")]
    [DisplayName("最大行数")]
    public int? MaxRows { get; set; }
}
```

---

## 5. 枚举属性 (EnumProperty)

枚举类型的属性在设计器中自动显示为下拉列表。

```csharp
using GrapeCity.Forguncy.CellTypes;
using System.ComponentModel;

public enum UserType
{
    [Description("学生")]
    Student,
    [Description("教师")]
    Teacher,
    [Description("工人")]
    Worker
}

public class MyPluginCellType : CellType
{
    [DisplayName("用户类型")]
    public UserType UserType { get; set; }
}
```

> [UI]: 设计器中显示包含 "学生"、"教师"、"工人" 的下拉列表。

### JavaScript 处理
枚举值在 JS 中被序列化为整数（索引）。建议在 JS 中建立映射表。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    userTypeMap = {
        0: "学生",
        1: "教师",
        2: "工人",
    }
    createContent() {
        const propValue = this.CellElement.CellType.UserType; // 0, 1, 2
        const text = this.userTypeMap[propValue] || "未知";
        return $("<div>" + text + "<div>");
    }
}
```

---

## 6. 字符串属性 (StringProperty)

`string` 类型属性自动识别为文本输入框。

```csharp
using GrapeCity.Forguncy.CellTypes;
using System.ComponentModel;

public class MyPluginCellType : CellType
{
    [DisplayName("标题")]
    public string Title { get; set; }
}
```

> [UI]: 设计器中显示为文本输入框。

### 进阶控制 (`TextPropertyAttribute`)
*   **水印**：`Watermark`。
*   **多行文本**：`AcceptsReturn = true`。
*   **多语言支持**：`CanSelectResource = true` (v10.0+)。

```csharp
[TextProperty(Watermark = "请输入...", AcceptsReturn = true, CanSelectResource = true)]
[DisplayName("描述")]
public string Description { get; set; }
```

**JS 获取多语言资源**:
```javascript
const propValue = this.getApplicationResource(this.CellElement.CellType.Description);
```

---

## 7. 公式属性 (FormulaProperty)

允许用户输入公式，属性值随公式计算结果动态变化。属性类型必须为 `object`。

```csharp
using GrapeCity.Forguncy.CellTypes;
using System.ComponentModel;

public class MyPluginCellType : CellType
{
    [FormulaProperty]
    [DisplayName("动态值")]
    public object DynamicValue { get; set; }
}
```

> [UI]: 设计器中显示为带有公式选择按钮的输入框。

### JavaScript 处理
在 `onPageLoaded` 中计算公式，并监听变化。

**推荐方式 (v10.0+)**:
使用 `onFormulaResultChanged`。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.content = $("<div></div>");
        return this.content;
    }
    onPageLoaded() {
        // 自动计算初始值并监听变化
        this.onFormulaResultChanged(this.CellElement.CellType.DynamicValue, result => {
            this.content.text(result);
        });
    }
}
```

### 进阶配置
*   **备选列表**：`RecommendedValues = "A|B|C"`。
*   **多行输入**：`AcceptsReturn = true`。
*   **禁用多语言**：`CanSelectResource = false`。

---

## 8. 字体属性 (FontProperty) (v9.1+)

用于选择字体。

```csharp
[FontFamilyProperty]
[DisplayName("字体")]
public string FontFamily { get; set; }
```

---

## 9. 百分比属性 (PercentageProperty) (v9.0+)

用于输入百分比，底层存储为 `double` (0-1)。

```csharp
[PercentageProperty]
[DisplayName("透明度")]
public double Opacity { get; set; }
```

---

## 10. 高级交互：自定义双击行为

### 场景 A：双击弹出自定义属性编辑器
对于非输入型单元格（如菜单），可以修改双击单元格时的默认行为（从进入编辑模式改为打开特定属性的编辑器）。

**实现 `IDefaultEditAction` 接口**:

```csharp
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Plugin;

public class MyPluginCellTypeDesigner : CellTypeDesigner<MyPluginCellType>, IDefaultEditAction
{
    public void OnStartEditStarting(IBuilderContext builderContext, StartEditingEventArgs args)
    {
        // 设置双击时默认激活编辑的属性名
        args.DefaultActionPropertyName = nameof(MyPluginCellType.MenuItems);
        // 取消进入表格编辑模式
        args.CancelEdit = true;
    }
}
```

### 场景 B：表格中双击进入编辑模式
如果单元格需要在表格（ListView）中支持双击编辑（类似 Excel 的单元格编辑体验）：

1.  **C# 配置**: 启用 `AllowEdit` 和 `AllowEnterEditMode`。

```csharp
public override ListViewOptions ListViewOptions => new ListViewOptions
{
    AllowEdit = true,
    AllowEnterEditMode = true,
};
```

2.  **JavaScript 实现**: 处理 `setValueToElement` (进入编辑) 和 `getValueFromElement` (保存编辑)。

> 详细生命周期：`createContent` (创建DOM) -> `setValueToElement` (设值) -> `getValueFromElement` (取值) -> `onDestroyInListView` (销毁)。

```javascript
// 简略示例
class StateCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.input = $("<input>");
        return this.input;
    }
    setValueToElement(_, value) {
        this.input.val(value);
    }
    getValueFromElement() {
        return this.input.val();
    }
}
```
