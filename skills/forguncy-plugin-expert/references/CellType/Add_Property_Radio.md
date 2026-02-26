# 添加属性 - 单选框属性 (Radio Property)

## 参考资料
[单选框属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/radioproperty)

## 概述
功能与下拉列表类似，但以单选框组的形式展示。属性类型必须为 `string`。

## 基础用法 ([RadioGroupProperty])
```csharp
public class MyPluginCellType : CellType
{
    [RadioGroupProperty(ValueList = "A|B|C")]
    public string MyProperty { get; set; }
}
```

## 高级用法

### 显示值与实际值不同 (DisplayList)
```csharp
[RadioGroupProperty(ValueList = "A|B", DisplayList = "选项A|选项B")]
public string MyProperty { get; set; }
```
