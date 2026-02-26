# 添加属性 - 百分比属性 (Percentage Property)

## 参考资料
此特性为活字格 V9 新增功能。

## 概述
百分比属性允许用户在设计器中以百分比形式（如 `50%`）输入，而代码中以小数形式（如 `0.5`）存储。

## 基础用法
属性类型必须为 `double`。

```csharp
public class MyPluginCellType : CellType
{
    [PercentageProperty]
    [DisplayName("透明度")]
    public double Opacity { get; set; }
}
```

## 注意事项
1. 用户输入 `50`，设计器会自动添加 `%`，值为 `0.5`。
2. 支持负值。
