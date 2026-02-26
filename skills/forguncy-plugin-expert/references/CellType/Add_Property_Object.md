# 添加属性 - 对象属性 (Object Property)

## 参考资料
[对象属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/objectproperty)

## 概述
当属性需要包含多个子属性时，可以使用对象属性。设计器会弹出一个二级对话框（或内嵌显示）来编辑这些属性。

## 基础用法 ([ObjectProperty])
自定义对象类必须继承自 `ObjectPropertyBase`。

```csharp
public class MyPluginCellType : CellType
{
    [ObjectProperty(ObjType = typeof(MyConfig))]
    public MyConfig Config { get; set; } = new MyConfig();
}

public class MyConfig : ObjectPropertyBase
{
    [DisplayName("名称")]
    public string Name { get; set; }
    
    [DisplayName("启用")]
    public bool Enabled { get; set; }
}
```

## 内嵌显示 ([FlatObjectProperty])
直接在属性面板中展开显示子属性，而不是弹出对话框。

```csharp
public class MyPluginCellType : CellType
{
    [FlatObjectProperty]
    public MyConfig Config { get; set; } = new MyConfig();
}
```

## 高级用法

### 1. 折叠高级属性 ([AdvancedProperty])
将不常用的属性折叠起来。
*(V10.0+)*
```csharp
public class MyConfig : ObjectPropertyBase
{
    public string Prop1 { get; set; }

    [AdvancedProperty]
    public string Prop2 { get; set; }
}
```

### 2. 自定义校验 (Designer/Validate)
```csharp
[Designer(typeof(MyConfigDesigner))]
public class MyConfig : ObjectPropertyBase { ... }

public class MyConfigDesigner : ObjectDesigner
{
    public override string Validate()
    {
        var obj = this.Obj as MyConfig;
        if (string.IsNullOrEmpty(obj.Name)) return "名称不能为空";
        return base.Validate();
    }
}
```
