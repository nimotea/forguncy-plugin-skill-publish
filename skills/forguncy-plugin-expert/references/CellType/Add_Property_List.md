# 添加属性 - 列表属性 (List Property)

## 参考资料
[列表属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/listproperty)

## 概述
用于管理简单类型的列表（如字符串列表）。

## 基础用法 ([ListProperty])
```csharp
public class MyPluginCellType : CellType
{
    [ListProperty]
    public List<string> Tags { get; set; } = new List<string>();
}
```

## 高级用法

### 设置列表项默认宽度
```csharp
[ListProperty]
[ListPropertyItemSetting(DefaultWidth = 200)]
public List<string> Tags { get; set; }
```
