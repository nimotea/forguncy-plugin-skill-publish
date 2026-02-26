# 添加属性 - 对象属性 (Object Property)

对象属性允许将一组相关的配置项封装在一个复杂的对象中。在设计器中，这通常表现为一个“编辑...”按钮，点击后弹出一个二级对话框来设置该对象内部的子属性。

## 1. 基础用法
要创建一个对象属性，需要：
1.  定义一个继承自 `ObjectPropertyBase` 的类（作为数据容器）。
2.  在 Command 中定义该类型的属性，并标注 `[ObjectProperty]`。

### 代码示例

**1. 定义对象类 (MyConfigObj)：**
```csharp
// 必须继承 ObjectPropertyBase 以支持深克隆
public class MyConfigObj : ObjectPropertyBase
{
    [DisplayName("用户名")]
    public string Username { get; set; }

    [DisplayName("密码")]
    public string Password { get; set; }
    
    // 子属性也可以是公式属性
    [DisplayName("动态参数")]
    [FormulaProperty]
    public object DynamicParam { get; set; }
}
```

**2. 在 Command 中引用：**
```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("高级配置")]
    [ObjectProperty(ObjType = typeof(MyConfigObj))]
    public MyConfigObj Config { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        // 访问子属性
        var user = Config.Username;
        // ...
        return new ExecuteResult();
    }
}
```

---

## 2. 高级配置

### 2.1 添加说明文字 ([Description])
在对象类上添加 `[Description]` 特性，可以在弹出的二级对话框顶部显示一段说明文字，帮助用户理解配置项的用途。
*(要求活字格版本 >= 10.0.0.0)*

```csharp
[Description("请在此配置第三方服务的连接参数。如果不知道如何填写，请联系管理员。")]
public class MyConfigObj : ObjectPropertyBase
{
    // ...
}
```

### 2.2 自定义校验 (ObjectDesigner)
如果需要对对象内部的多个属性进行联合校验（例如：属性A和属性B至少填一个），可以编写自定义的 `ObjectDesigner`。
*(要求活字格版本 >= 10.0.0.0)*

```csharp
[Designer(typeof(MyObjectDesigner))] // 关联 Designer
public class MyConfigObj : ObjectPropertyBase
{
    public string PropA { get; set; }
    public string PropB { get; set; }
}

public class MyObjectDesigner : ObjectDesigner
{
    public override string Validate()
    {
        // 获取当前对象实例
        if (this.Obj is MyConfigObj myObj)
        {
            if (string.IsNullOrEmpty(myObj.PropA) && string.IsNullOrEmpty(myObj.PropB))
            {
                return "PropA 和 PropB 不能同时为空！";
            }
        }
        return base.Validate();
    }
}
```

### 2.3 内嵌显示 (FlatObjectProperty)
如果不想弹出二级对话框，而是希望对象的子属性直接显示在父级属性面板中，可以使用 `[FlatObjectProperty]`。

```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("基本信息")]
    [FlatObjectProperty] // 关键特性：扁平化/内嵌显示
    public MyConfigObj Config { get; set; }
}
```
此时，`MyConfigObj` 中的属性会直接展平显示在 Command 的属性列表中，通常看起来像是一组相关的属性。

## 3. 常见问题
- **Q: 为什么要继承 `ObjectPropertyBase`？**
  A: 为了支持活字格内部的深克隆机制（例如在复制/粘贴单元格或命令时）。如果不继承该基类，复制后的对象可能只是引用副本，导致修改一个地方影响另一个地方。
