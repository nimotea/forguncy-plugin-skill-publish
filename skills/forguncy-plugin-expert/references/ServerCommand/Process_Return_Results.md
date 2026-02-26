# 支持返回结果 (Support Return Results)

服务端命令执行后，通常需要将结果返回给调用者（如前端页面或其他命令）。活字格提供了标准机制来处理返回结果，并支持简单值、复杂对象和列表等多种类型。

## 1. 基础返回结果

对于简单的返回结果（如字符串、数字），只需定义一个属性来接收“变量名”，并标记 `[ResultToProperty]` 特性。

### 代码示例

```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    // 输入参数
    [FormulaProperty]
    public object InputValue { get; set; }

    // 返回结果变量名
    [ResultToProperty]
    [DisplayName("将结果保存到变量")]
    public string ResultTo { get; set; } = "结果";

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        // 1. 计算结果
        var result = "Hello " + InputValue?.ToString();

        // 2. 将结果存入上下文变量
        // 注意：ResultTo 属性存储的是变量名（如 "MyResult"），而不是值本身
        dataContext.Parameters[ResultTo] = result;

        return new ExecuteResult();
    }
    
    public override CommandScope GetCommandScope()
    {
        return CommandScope.ExecutableInServer;
    }
}
```

## 2. 复杂结构类型的返回结果：接口选型指南

在活字格插件开发的演进过程中，存在两个用于描述返回结构的接口：`ICommandResultReturnDescription`（旧版）和 `IServerCommandParamGenerator`（新版/推荐）。

### 选型对比

| 特性 | IServerCommandParamGenerator (推荐) | ICommandResultReturnDescription (不推荐) |
| :--- | :--- | :--- |
| **引入版本** | 较新 (v7.0+) | 较旧 |
| **设计器支持** | **支持全功能智能感知** (对象属性、列表项) | 仅基础支持 |
| **中文友好度** | **高** (支持字段名与描述分离) | 低 (通常只能显示字段名) |
| **灵活性** | 支持对象 (`GenerateObjectParam`) 和列表 (`GenerateListParam`) | 较为单一 |
| **场景** | 所有需要返回复杂数据并希望用户获得提示的场景 | 仅在维护旧插件时参考 |

**结论**：除非你是为了维护非常古老的插件代码，否则**请始终使用 `IServerCommandParamGenerator`**。

### 接口定义

```csharp
public interface IServerCommandParamGenerator
{
    IEnumerable<GenerateParam> GetGenerateParams();
}
```

### 示例：返回复杂对象

假设我们要返回一个包含“姓名”和“年龄”的学生对象。

```csharp
using GrapeCity.Forguncy.Commands;
using System.Collections.Generic;

public class GetStudentCommand : Command, ICommandExecutableInServerSideAsync, IServerCommandParamGenerator
{
    [ResultToProperty]
    [DisplayName("将学生信息保存到变量")]
    public string ResultTo { get; set; } = "学生信息";

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        // 模拟获取数据
        var student = new Dictionary<string, object>
        {
            { "Name", "张三" },
            { "Age", 18 }
        };

        // 将字典或实体对象存入变量
        dataContext.Parameters[ResultTo] = student;

        return new ExecuteResult();
    }

    public override CommandScope GetCommandScope()
    {
        return CommandScope.ExecutableInServer;
    }

    // 实现接口，定义返回值的结构
    public IEnumerable<GenerateParam> GetGenerateParams()
    {
        // 创建对象参数描述
        var objectParam = new GenerateObjectParam
        {
            ParamName = this.ResultTo, // 关联属性中指定的变量名
            Description = "查询到的学生详细信息",
            // 定义子属性：Key 是代码引用的字段名，Value 是设计器显示的中文描述
            SubPropertiesDescription = new Dictionary<string, string>
            {
                { "Name", "姓名" }, 
                { "Age", "年龄" }
            }
        };

        yield return objectParam;
    }
}
```

### 示例：返回列表 (最佳实践)

对于列表类型，为了让用户在循环命令（如“循环命令”）中不仅能看到字段英文名，还能看到中文描述，**必须同时配置 `ItemProperties` 和 `ItemPropertiesDescription`**。

```csharp
public class GetStudentListCommand : Command, ICommandExecutableInServerSideAsync, IServerCommandParamGenerator
{
    [ResultToProperty]
    [DisplayName("将列表结果保存到变量")]
    public string ResultTo { get; set; } = "学生列表";

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        var list = new List<Dictionary<string, object>>();
        // ... 填充列表数据 ...
        
        dataContext.Parameters[ResultTo] = list;
        return new ExecuteResult();
    }

    public override CommandScope GetCommandScope()
    {
        return CommandScope.ExecutableInServer;
    }

    public IEnumerable<GenerateParam> GetGenerateParams()
    {
        var listParam = new GenerateListParam
        {
            ParamName = this.ResultTo,
            Description = "查询到的学生列表",
            
            // 1. 基础属性列表 (必需)
            ItemProperties = new List<string> { "Name", "Age", "ClassId" },
            
            // 2. 属性中文描述 (强烈推荐)
            // 这样设计器中用户输入点（.）时，会显示 "Name (姓名)"
            ItemPropertiesDescription = new Dictionary<string, string>
            {
                { "Name", "姓名" },
                { "Age", "年龄" },
                { "ClassId", "班级编号" }
            }
        };
        
        yield return listParam;
    }
}
```

## 关键点

1.  **ResultToProperty**：标记用于接收变量名的属性。
2.  **dataContext.Parameters**：在运行时通过变量名写入数据。
3.  **IServerCommandParamGenerator**：在设计时告诉设计器返回数据的结构，启用智能提示。
4.  **GenerateParam 子类**：
    *   `GenerateObjectParam`：用于单个对象。
    *   `GenerateListParam`：用于列表/数组。
