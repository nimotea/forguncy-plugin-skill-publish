# 属性校验与高级校验 (Validation)

通过给属性添加校验规则，可以在设计器阶段就拦截用户的错误输入，减少运行时的错误处理负担。

## 1. 基础校验 (Attributes)
活字格支持使用 `System.ComponentModel.DataAnnotations` 命名空间下的标准特性进行校验。

### 1.1 必填校验 (Required)
使用 `[Required]` 特性标记属性为必填。如果用户未填写，设计器会提示错误。

```csharp
using System.ComponentModel.DataAnnotations;

public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("用户名")]
    [Required] // 必填
    public string Username { get; set; }
}
```

### 1.2 长度校验 (MinLength/MaxLength)
使用 `[MinLength]` 和 `[MaxLength]` 限制字符串的长度。

```csharp
[DisplayName("密码")]
[MinLength(6, ErrorMessage = "密码至少6位")]
[MaxLength(20, ErrorMessage = "密码不能超过20位")]
public string Password { get; set; }
```

---

## 2. 高级自定义校验 (Custom Validation)

### 2.1 对象属性校验 (ObjectDesigner)
对于使用 `[ObjectProperty]` 或 `[ObjectListProperty]` 的复杂对象，可以通过重写 `ObjectDesigner.Validate` 方法实现校验。

```csharp
// 1. 关联 Designer
[Designer(typeof(MyObjectDesigner))]
public class MyConfigObj : ObjectPropertyBase
{
    public string PropA { get; set; }
    public string PropB { get; set; }
}

// 2. 实现 Designer
public class MyObjectDesigner : ObjectDesigner
{
    public override string Validate()
    {
        if (this.Obj is MyConfigObj myObj)
        {
            // 示例：A和B必须且只能填一个
            bool hasA = !string.IsNullOrEmpty(myObj.PropA);
            bool hasB = !string.IsNullOrEmpty(myObj.PropB);

            if (hasA && hasB)
                return "属性 A 和 属性 B 不能同时存在";
            if (!hasA && !hasB)
                return "必须填写 属性 A 或 属性 B";
        }
        return base.Validate(); // 必须调用基类方法以触发标准校验
    }
}
```

### 2.2 命令级校验 (CommandDesigner)
如果需要对整个命令的多个属性进行联合校验（例如：属性1 + 属性2 必须大于 100），可以重写 `CommandDesigner.Validate` 方法。

```csharp
public class MyPluginServerCommandDesigner : CommandDesigner<MyPluginServerCommand>
{
    public override string Validate()
    {
        if (this.Command.MyProperty + this.Command.MyProperty1 < 100)
        {
            return "MyProperty 与 MyProperty1 的和必须大于 100";
        }
        return base.Validate();
    }
}
```

### 2.3 生成时校验 (ICommandChecker)
如果需要在**生成工程**（Build/Publish）时进行更复杂的检查，并且希望区分“错误”和“警告”级别，可以让 Designer 实现 `ICommandChecker` 接口。
> **注意**：此校验逻辑会在每次生成工程时触发，请确保逻辑高效，避免耗时操作。

```csharp
using GrapeCity.Forguncy.Plugin;

public class MyPluginServerCommandDesigner : CommandDesigner<MyPluginServerCommand>, ICommandChecker
{
    public IEnumerable<ForguncyErrorInfo> CheckCommandErrors(IBuilderCommandContext context)
    {
        var sum = this.Command.MyProperty + this.Command.MyProperty1;

        // 情况1：严重错误（阻止生成）
        if (sum <= 10)
        {
            yield return new ForguncyErrorInfo()
            {
                ErrorType = ForguncyErrorType.Error,
                Message = "两数之和不能小于等于 10，这将导致运行错误！"
            };
        }
        // 情况2：警告（不阻止生成）
        else if (sum < 100)
        {
            yield return new ForguncyErrorInfo()
            {
                ErrorType = ForguncyErrorType.Warning,
                Message = "两数之和小于 100 可能导致性能下降。"
            };
        }
    }
}
```
