# 和活字格原生功能集成 - 支持复杂类型的单元格格式 (Complex Cell Style)

## 参考资料
[支持复杂类型的单元格格式 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/supportcell-type-style-root/support-complex-cell-styles)

## 概述
对于复杂单元格（如表格、列表），可能需要为内部的不同部分（如表头、行）分别设置样式。
通过 `[CellFormatSetting]` 特性将样式配置保存到 `ForguncyStyleInfo` 对象中。

## 基础用法

### 1. 定义样式配置对象
```csharp
public class TableColumnConfig : ObjectPropertyBase, INamedObject
{
    public string Name { get; set; }

    [DisplayName("列头样式")]
    [CellFormatSetting] // 标记为样式配置
    public ForguncyStyleInfo HeaderStyle { get; set; }

    [DisplayName("列样式")]
    [CellFormatSetting]
    public ForguncyStyleInfo BodyStyle { get; set; }
}
```

### 2. 在插件类中使用
```csharp
public class MyTablePlugin : CellType
{
    [ObjectListProperty(ItemType = typeof(TableColumnConfig))]
    public List<INamedObject> Columns { get; set; } = new List<INamedObject>();
}
```

## 高级用法 - 限制样式选项

### 隐藏部分 Tab (FormatTabType)
```csharp
[CellFormatSetting(FormatTabType = PluginFormatDialogTabType.Normal ^ PluginFormatDialogTabType.Number)]
public ForguncyStyleInfo HeaderStyle { get; set; }
```
*示例：隐藏“数字”设置标签页*

### 隐藏部分对齐选项 (AlignmentFormatOptions)
```csharp
[CellFormatSetting(AlignmentFormatOptions = PluginAlignmentFormatOptions.All ^ PluginAlignmentFormatOptions.HorizontalAlignment)]
public ForguncyStyleInfo HeaderStyle { get; set; }
```
*示例：隐藏“水平对齐”设置*

## JS 处理逻辑
运行时获取到的 `ForguncyStyleInfo` 对象包含解析后的样式属性（如 `backgroundStr`, `fontFamily` 等）。

```javascript
// 示例：获取列配置中的样式
const column = this.CellElement.CellType.Columns[0];
const headerStyle = column.HeaderStyle; // 这是一个样式对象

// 需要自行解析并应用到对应的 DOM 元素
// 注意：ForguncyStyleInfo 的属性名在 JS 中是小驼峰（例如 BackgroundStr -> backgroundStr）
```
