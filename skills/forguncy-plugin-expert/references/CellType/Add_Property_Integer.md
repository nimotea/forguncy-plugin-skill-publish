# 添加属性 - 整数属性 (Integer Property)

## 参考资料
[整数属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/integerproperty)

## 概述
`int` 类型的属性会自动识别为整数属性。

## 基础用法
```csharp
public class MyPluginCellType : CellType
{
    public int MyProperty { get; set; } = 0;
}
```

## 高级用法 ([IntProperty])

### 1. 限制范围 (Min, Max)
```csharp
[IntProperty(Min = 1, Max = 100)]
public int MyProperty { get; set; }
```

### 2. 允许空值 (AllowNull)
属性类型必须为 `int?`。
```csharp
[IntProperty(AllowNull = true, Watermark = "无限制")]
public int? MyProperty { get; set; }
```
