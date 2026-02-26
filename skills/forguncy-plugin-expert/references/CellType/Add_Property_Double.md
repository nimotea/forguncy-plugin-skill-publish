# 添加属性 - 小数属性 (Decimal/Double Property)

## 参考资料
[小数属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/decimalproperty)

## 概述
`double` 类型的属性会自动识别为小数属性。

## 基础用法
```csharp
public class MyPluginCellType : CellType
{
    public double MyProperty { get; set; }
}
```

## 高级用法 ([DoubleProperty])

### 1. 限制范围 (Min, Max)
```csharp
[DoubleProperty(Min = 0.0, Max = 1.0)]
public double MyProperty { get; set; }
```

### 2. 允许空值 (AllowNull)
属性类型必须为 `double?`。
```csharp
[DoubleProperty(AllowNull = true)]
public double? MyProperty { get; set; }
```
