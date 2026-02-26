# 添加属性 - 对象列表属性 (Object List Property)

## 参考资料
[对象列表属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/objectlistproperty)

## 概述
用于管理复杂对象的列表。设计器提供增删改查的 UI。

## 基础用法 ([ObjectListProperty])
列表项类型必须实现 `INamedObject` 接口（用于显示列表项名称）。

> **关键点**：实现 `INamedObject` 接口意味着你**必须**在类中定义一个 `public string Name { get; set; }` 属性。

```csharp
public class MyPluginCellType : CellType
{
    [ObjectListProperty(ItemType = typeof(ColumnConfig))]
    public List<INamedObject> Columns { get; set; } = new List<INamedObject>();
}

// 必须继承 ObjectPropertyBase 并实现 INamedObject
public class ColumnConfig : ObjectPropertyBase, INamedObject
{
    [DisplayName("列名")]
    public string Name { get; set; } // 必须显式定义此属性以满足接口要求
    
    [DisplayName("宽度")]
    public int Width { get; set; }
}
```

## JS 处理逻辑
在 JS 中，列表属性会作为数组传递。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const columns = this.CellElement.CellType.Columns;
        const container = $("<div></div>");
        
        // 遍历列表
        for (const col of columns) {
            container.append(`<div>${col.Name}: ${col.Width}px</div>`);
        }
        
        return container;
    }
}
```
