# 添加属性 - 字体属性 (Font Property)

## 参考资料
[字体属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/fontproperty)

## 概述
提供字体选择器。属性类型必须为 `string`。
*(活字格 V9.1 新增)*

## 基础用法 ([FontFamilyProperty])
```csharp
public class MyPluginCellType : CellType
{
    [FontFamilyProperty]
    public string FontFamily { get; set; }
}
```

## 默认值
默认值为当前主题字体。
