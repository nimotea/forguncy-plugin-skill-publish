# 单元格设计时支持 - 分组与排序 (Grouping & Sorting)

## 参考资料
[单元格分组与排序 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/cellgroupingandsorting)

## 概述
控制插件单元格在设计器工具箱中的分类和显示顺序。

## 1. 单元格分组 ([Category])
如果不设置，默认在“其他”分组。

```csharp
[Category("我的插件组")]
public class MyPluginCellType : CellType
{
}
```
*提示：如果使用系统内置分组名（如“导航”），插件会显示在该分组下。*

## 2. 排序权重 ([OrderWeight])
控制同一分组内插件的显示顺序（数值越小越靠前）。

```csharp
[OrderWeight(1)]
[Category("我的插件组")]
public class MyPluginCellType1 : CellType { }

[OrderWeight(2)]
[Category("我的插件组")]
public class MyPluginCellType2 : CellType { }
```

## 3. 属性分组 ([CategoryHeader])
[属性分组 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/categoryheaderattribute)

在属性面板中对属性进行分组显示。

```csharp
public class MyPluginCellType : CellType
{
    [CategoryHeader("基础设置")]
    public string Prop1 { get; set; }

    [CategoryHeader("高级设置")]
    public string Prop2 { get; set; }
}
```
