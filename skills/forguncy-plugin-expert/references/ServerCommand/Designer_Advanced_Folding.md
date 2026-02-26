# 折叠高级属性 (Advanced Property Folding)

当插件的属性较多时，为了降低用户的学习成本和界面干扰，可以将不常用的属性标记为“高级属性”。这些属性在默认情况下会被折叠隐藏，点击“高级设置”后才会展开。

## 特性说明

- **特性类**：`[AdvancedProperty]`
- **行为**：
  - 默认情况下，被标记的属性会被折叠在“高级设置”分组中。
  - 如果用户修改了这些属性的值（即值不再是默认值），下次选中该插件时，“高级设置”会自动展开。
  - 建议配合 `[DefaultValue]` 使用，以便设计器正确判断属性是否被修改。

## 代码示例

### 1. 基础属性折叠

```csharp
using GrapeCity.Forguncy.Commands;
using System.ComponentModel;

public class MyPluginServerCommand : Command
{
    // 普通属性，始终显示
    public string NormalProperty { get; set; }

    // 高级属性，默认折叠
    [AdvancedProperty]
    [DefaultValue(null)] // 建议显式设置默认值
    public string AdvancedSetting1 { get; set; }

    [AdvancedProperty]
    [DefaultValue(false)]
    public bool EnableDebugMode { get; set; }
}
```

### 2. 对象属性中的字段折叠

同样适用于 `[ObjectProperty]` 定义的子属性对象中。

```csharp
public class MyPluginServerCommand : Command
{
    [ObjectProperty(ObjType = typeof(MyConfigObj))]
    public MyConfigObj Config { get; set; }
}

public class MyConfigObj : ObjectPropertyBase
{
    public string Host { get; set; }

    // 对象内部的高级属性
    [AdvancedProperty]
    [DefaultValue(8080)]
    public int Port { get; set; }
}
```

### 3. 对象列表中的字段折叠

适用于 `[ObjectListProperty]` 列表项中的属性。

```csharp
public class MyPluginServerCommand : Command
{
    [ObjectListProperty(ItemType = typeof(MyItem))]
    public List<INamedObject> Items { get; set; }
}

public class MyItem : ObjectPropertyBase, INamedObject
{
    public string Name { get; set; } // 必须实现 INamedObject

    public string Value { get; set; }

    // 列表项中的高级属性
    [AdvancedProperty]
    public string Description { get; set; }
}
```
