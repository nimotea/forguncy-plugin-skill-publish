# 单元格设计时支持 - 初始化属性值 (Initialize Properties)

## 参考资料
[创建单元格时初始化属性值 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/initializepropertyvalueswhencreatingcells)

## 概述
当用户在设计器中创建新单元格时，预先填充一些默认数据（特别是对于列表、对象等复杂类型）。

## 实现方法
让 `CellTypeDesigner` 实现 `ISupportPropertyInitialize` 接口。

```csharp
public class MyPluginCellTypeDesigner : CellTypeDesigner<MyPluginCellType>, ISupportPropertyInitialize
{
    public void InitDefaultPropertyValues(IBuilderContext context)
    {
        // 初始化列表属性，添加默认项
        this.CellType.Items.Add(new Item() { Name = "默认项目1" });
        this.CellType.Items.Add(new Item() { Name = "默认项目2" });
        
        // 初始化其他属性
        this.CellType.Title = "默认标题";
    }
}
```
