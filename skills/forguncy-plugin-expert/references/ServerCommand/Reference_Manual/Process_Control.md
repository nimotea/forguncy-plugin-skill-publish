# Process Control

## Processcontrol

# 流程控制

## Content

* [异常处理](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developservercommandplugin/processcontrol/exceptionhandling)
* [支持返回结果](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developservercommandplugin/processcontrol/supportreturnedresults)
    * [支持结构类型的返回结果](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developservercommandplugin/processcontrol/supportreturnedresults/supportsstructuretypereturnresults)
* [服务端命令Execute函数返回值](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developservercommandplugin/processcontrol/servercommandexecutefunctionreturnvalue)

---

## Exceptionhandling

# 异常处理

## Content

服务端命令的核心处理函数为ExecuteAsync，默认的返回值为 ExecuteResult 类型。
约定规定，返回 ExecuteResult.ErrCode值为 0 表示成功，非 0 为失败。如果 ErrorCode为非 0 时，如果存在多种错误情况，插件开发者可以自行定义ErrorCode，以方便调试。

```
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            if (CheckPermission())
            {
                return new ExecuteResult() { ErrCode = 1, Message = "权限不足" };
            }
            if (NotEnoughStorage())
            {
                return new ExecuteResult() { ErrCode = 2, Message = "库存不足" };
            }
            // 业务逻辑
            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
```

如果ExecuteAsync抛出为处理的异常，活字格会自动把 ExecuteResult.ErrCode 设置为 500，ExecuteResult.Message 设置为异常信息并生成日志。

---

## Servercommandexecutefunctionreturnvalue

# 服务端命令Execute函数返回值

## Content

### **ErrCode 和 Message**

服务端命令的执行函数 ExecuteAsync 返回值类型为 ExecuteResult 对象。
如果执行成功，只需要返回默认的 ExecuteResult对象即可。

```auto
public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
{
    return new ExecuteResult();
}
```

如果需要表示执行失败，应该设置返回的 ExecuteResult 对象的ErrCode属性为一个非 0 值。同时推荐设置 Message 属性说明失败原因。

```auto
public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
{
    return new ExecuteResult()
    {
        ErrCode = 1,
        Message = "库存不足"
    };
}
```

除了最常用的ErrCode属性和 Message属性，在特定场景下可能需要设置其他 ExecuteResult 实例上的属性以满足不同的需求。

### 自定义响应（Response）内容

默认情况下，服务端命令执行的最终 ExecuteResult 会被写入到 HTTP 请求的 ResponseBody（响应）中。如此，可以和前端的调用Http请求命令配合，完成前后端逻辑。
但是，有些情况下，服务端命令需要自己控制请求响应内容，此需求在与第三方系统集成时特别有用。通过设置 AllowWriteResultToResponse 为 False 可以阻止活字格把 ExecuteResult 对象写入HTTP 响应。

```auto
using GrapeCity.Forguncy.Commands;
using Microsoft.AspNetCore.Http;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            await dataContext.Context.Response.WriteAsync("自定义响应的内容");
            return new ExecuteResult() { AllowWriteResultToResponse = false };
        }
        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

### 流程控制

默认情况下，如果命令这些成功，会执命令列表中的下一个服务端命令。通过设置 ProcessControl 属性的值，可以命令列表的执行流程。

```auto
public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
{
    return new ExecuteResult()
    {
        ProcessControl = ProcessControl.Return
    };
}
```

ProcessControl 可用选项如下表：

| Continue | 默认值，表示继续执行后续命令。 |
| -------- | --------------- |
| Return | 立即返回，会跳过所有后续命令列表的执行。 |
| BreakLoopAndContinue | 如果当前命令是循环命令的子命令，跳出当前循环，继续执行循环命令之后的命令，类似于编程语言中的 break。 |
| ContinueLoop | 如果当前命令是循环命令的子命令，跳过此次循环的后续命令，继续执行下次循环，类似于编程语言中的 continue。 |

---

## Supportreturnedresults

# 支持返回结果

## Content

命令执行后，可以把命令的执行结果保持到变量里，以便后续的命令或逻辑使用。
可以通过实现ResultToPropertyAttribute来实现此效果。
示例代码：
注意：标注 ResultToProperty 的属性类型必须是 string。推荐给属性添加默认值，以方便用户使用。

```
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [FormulaProperty]
        [DisplayName("加数1")]
        public object AddNumber1 { get; set; }

        [FormulaProperty]
        [DisplayName("加数2")]
        public object AddNumber2 { get; set; }

        [ResultToProperty]
        [DisplayName("相加结果")]
        public string ResultTo { get; set; } = "结果";

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            var add1 = await dataContext.EvaluateFormulaAsync(AddNumber1);
            var add2 = await dataContext.EvaluateFormulaAsync(AddNumber2);

            double.TryParse(add1?.ToString(), out var add1Number);
            double.TryParse(add2?.ToString(), out var add2Number);

            dataContext.Parameters[ResultTo] = add1Number + add2Number;

            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
```

设计器中的效果：

在后续命令编辑公式时，设置的变量可以直接在公式中使用。

---

## Supportsstructuretypereturnresults

# 支持结构类型的返回结果

## Content

从上一节[支持返回结果](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developservercommandplugin/processcontrol/supportreturnedresults)中，我们已经了解到，通过给属性标注ResultToPropertyAttribute，可以在命令执行后生成一个或多个返回结果，以便后续命令使用。
如果希望生成复杂的对象类型返回结果，或者生成数组类型的返回结果，通过标注ResultToPropertyAttribute，也是可以实现的。但是再后续的属性提示中，用户无法快捷的了解返回的对象有哪些子属性。只能通过点操作符硬取值。
例如以下代码：

```csharp
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;
using GrapeCity.Forguncy.ServerApi;
using System.ComponentModel;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [FormulaProperty]
        [DisplayName("学生Id")]
        public object StudentId { get; set; }

        [ResultToProperty]
        [DisplayName("查询结果")]
        public string ResultTo { get; set; } = "结果";

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            var id = await dataContext.EvaluateFormulaAsync(this.StudentId);
            var studentInfo = dataContext.DataAccess.GetTableData("学生表", new ColumnValuePair()
            {
                ColumnName = "ID",
                Value = id
            });

            dataContext.Parameters[ResultTo] = studentInfo;
            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

### 对象类型返回值

假设命令执行后，返回学生对象，包含姓名和年龄属性。但是再后续命令使用结果时只会提示结果变量，而如果需要获取子属性值，必须用户手动准确输入，用户体验较差。

如果希望同时提示子属性，可以通过实现IServerCommandParamGenerator接口实现。

```auto
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;
using GrapeCity.Forguncy.ServerApi;
using System.Collections.Generic;
using System.ComponentModel;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync, IServerCommandParamGenerator
    {
        [FormulaProperty]
        [DisplayName("学生Id")]
        public object StudentId { get; set; }

        [ResultToProperty]
        [DisplayName("查询结果")]
        public string ResultTo { get; set; } = "结果";

        public IEnumerable<GenerateParam> GetGenerateParams()
        {
            yield return new GenerateObjectParam()
            {
                ParamName = this.ResultTo,
                Description = "查询学生的详细信息结果",
                ParamScope = CommandScope.All,
                SubPropertiesDescription = new Dictionary<string, string>() {
                    { "姓名","学生姓名"},
                    { "年龄","学生年龄"}
                }
            };
        }
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            var id = await dataContext.EvaluateFormulaAsync(this.StudentId);
            var studentInfo = dataContext.DataAccess.GetTableData("学生表", new ColumnValuePair()
            {
                ColumnName = "ID",
                Value = id
            });

            dataContext.Parameters[ResultTo] = studentInfo;
            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

效果如下：

### 数组类型返回值

如果返回值是列表类型，同样可以通过实现IServerCommandParamGenerator解决。

```auto
using GrapeCity.Forguncy.Commands;
using System.Collections.Generic;
using System.ComponentModel;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync, IServerCommandParamGenerator
    {
        [ResultToProperty]
        [DisplayName("查询结果")]
        public string ResultTo { get; set; } = "结果";

        public IEnumerable<GenerateParam> GetGenerateParams()
        {
            yield return new GenerateListParam()
            {
                ParamName = this.ResultTo,
                Description = "查询学生的详细信息结果",
                ParamScope = CommandScope.All,
                ItemProperties = new List<string>() {
                    "姓名",
                    "年龄"
                }
            };
        }
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            var studentInfos = dataContext.DataAccess.GetTableData("学生表");
            dataContext.Parameters[ResultTo] = studentInfo;
            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

效果如下。
在普通命令中使用时：

在循环命令的子命令中使用时：

### 数组与对象嵌套混合类型返回值

如果返回值是列表或对象多级嵌套的复杂类型，同样可以通过实现IServerCommandParamGenerator解决，需要使用 GenerateObjectParam 类型的 SubGenerateProperties 属性和 GenerateListParam 的 ItemGenerateProperties 属性。

>type=note
> 说明：
> 多级混合嵌套特性为 V11.0.100.0 新增特性。

```javascript
using GrapeCity.Forguncy.Commands;
using System.Collections.Generic;
using System.ComponentModel;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync, IServerCommandParamGenerator
    {
        [ResultToProperty]
        [DisplayName("查询结果")]
        public string ResultTo { get; set; } = "结果";

        public IEnumerable<GenerateParam> GetGenerateParams()
        {
            yield return new GenerateObjectParam()
            {
                ParamName = this.ResultTo,
                ParamScope = CommandScope.All,
                SubGenerateProperties = new List<GenerateParam>()
                {
                    new GenerateNormalParam("姓名", "学生姓名"),
                    new GenerateNormalParam("年龄", "学生年龄"),
                    new GenerateListParam("更新历史", "更新历史记录")
                    {
                        ItemGenerateProperties = new List<GenerateParam>()
                        {
                            new GenerateNormalParam("日期", "更新日期"),
                            new GenerateNormalParam("更新人", "更新人")
                        }
                    },
                    new GenerateObjectParam("地址", "地址信息")
                    {
                        SubGenerateProperties = new List<GenerateParam>()
                        {
                            new GenerateNormalParam("国家", "国家"),
                            new GenerateNormalParam("省", "省份"),
                            new GenerateNormalParam("市", "城市"),
                            new GenerateNormalParam("街道", "街道")
                        }
                    }
                 }
            };
        }
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            //var studentInfo = await GetStudentInfo(); // 假设用过三方 API 获取到复杂的Json结构数据
            //dataContext.Parameters[ResultTo] = studentInfo;
            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

可以看到二级属性地址，下的有三级属性省，市等，效果如下：

此时，如果在循环命令中循环 “学生信息.更新历史”可以在 更新项目 中使用列表的二级属性“日期”“更新人”。