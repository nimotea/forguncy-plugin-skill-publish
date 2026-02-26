# Other Functions

## Databaseconnectionselectorproperty

# 数据库连接选择属性

## Content

<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">此特性为活字格V9.1新增功能。</span>

```
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [DatabaseConnectionSelectorProperty]
        public string Connection { get; set; }

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            var dataAccess = dataContext.DataAccess;
            var connectionStr = dataAccess.GetConnectionStringByID(Connection);

            dataAccess.BeginTransaction(connectionStr);
            try
            {
                var result = await dataAccess.ExecuteSqlAsync(Connection, "select * from 表1", null);
                dataAccess.CommitTransaction(connectionStr);
            }
            finally
            {
                dataAccess.RollbackTransaction(connectionStr);
            }
            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
```

<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">在设计器中效果如下：</span>
<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">在数据库连接管理中连接了一些外链数据库之后：</span>

<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">可以通过标注了</span><span class="ne-text">DatabaseConnectionSelectorProperty</span><span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">的属性选择特定数据库。</span>

<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">如果需要更细致的控制，可以通过</span><span class="ne-text">DatabaseConnectionSelectorProperty</span><span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">的其他属性来控制。</span>
**<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">（空）显示为内建库</span>**

1. <span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">设置</span><span class="ne-text">DatabaseConnectionSelectorProperty</span><span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">的IncludeBuiltInDatabase属性。</span>
2. 代码：

    ```
         public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [DatabaseConnectionSelectorProperty(IncludeBuiltInDatabase = true)]
            public string Connection { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                var dataAccess = dataContext.DataAccess;
                var connectionStr = dataAccess.GetConnectionStringByID(Connection);
    
                dataAccess.BeginTransaction(connectionStr);
                try
                {
                    var result = await dataAccess.ExecuteSqlAsync(Connection, "select * from 表1", null);
                    dataAccess.CommitTransaction(connectionStr);
                }
                finally
                {
                    dataAccess.RollbackTransaction(connectionStr);
                }
                return new ExecuteResult();
            }
    
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    ```
3. 效果：
    
4. 说明：<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">对于内建数据库（Sqlite）连接名称为null。</span>

<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">注意：标注DatabaseConnectionSelectorProperty的属性类型必须是 string。</span>

---

## Addsubcommand

# 添加子命令

## Content

可以通过实现 ISubListCommand 和 IContainSubCommands 实现给命令添加子命令。

```
using GrapeCity.Forguncy.Commands;
using System.Collections.Generic;
using System.ComponentModel;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync, ISubListCommand, IContainSubCommands
    {
        [Browsable(false)]
        public List<Command> CommandList { get; set; } = new List<Command>();

        public IEnumerable<List<Command>> EnumSubCommands()
        {
            yield return CommandList;
        }

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            dataContext.Log.AppendLine("子命令开始执行");
            var result = await dataContext.ExecuteCommandsAsync(this.CommandList);
            dataContext.Log.AppendLine("子命令执行结束");
            return result;
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

代码说明：

1. 给 CommandList属性标注 [Browsable(false)] 避免CommandList属性出现在主命令的属性中。
2. 通过 dataContext.ExecuteCommandsAsync 方法执行子命令。

效果：

---

## Databaseinteraction

# 数据库交互

## Content

在服务端命令中，可以通过 dataContext.DataAccess 属性对数据库进行增删改查。
本例中使用的示例数据库如下：

### **获取数据示例代码**

参数为OData字符串：

```
using GrapeCity.Forguncy.Commands;
using Newtonsoft.Json;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            var data = dataContext.DataAccess.GetTableData("表1?$select=ID,字段1,小数");

            return new ExecuteResult() { Message = JsonConvert.SerializeObject(data) };
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

效果如下：

### 新增数据示例代码

```
using GrapeCity.Forguncy.Commands;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            dataContext.DataAccess.AddTableData("表1", new Dictionary<string, object>
            {
                {"字段1", "xxx" },
                {"小数", "1.5" }
            });

            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

执行结果：

### 删除数据示例代码

```
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.ServerApi;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            dataContext.DataAccess.DeleteTableData("表1", new ColumnValuePair()
            {
                ColumnName = "ID",
                Value = 2
            });

            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

执行结果：

### 更新数据示例代码

```
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.ServerApi;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            dataContext.DataAccess.UpdateTableData("表1", new ColumnValuePair()
            {
                ColumnName = "ID",
                Value = 2
            },
            new Dictionary<string, object>()
            {
                {"字段1", "xxx" },
                {"小数", "1.5" }
            });

            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

执行结果：

---

## Servercommandlog

# 服务端命令日志

## Content

在服务端命令代码逻辑中添加日志，可以方便用户调试服务端命令，了解命令的执行状态。在ExecuteAsync方法内调用 Log.AppendLine 方法。

```
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            var add1 = await dataContext.EvaluateFormulaAsync(MyProperty); 

            dataContext.Log.AppendLine("这里是服务端命令日志, MyProperty属性值为：" + add1);

            return new ExecuteResult();
        }
```

测试效果：

如果需要树形结构来输出复杂的日志效果，可以使用 IncreaseIndent 和 DecreaseIndent 方法。

```
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            var add1 = await dataContext.EvaluateFormulaAsync(MyProperty); 

            dataContext.Log.AppendLine("这里是服务端命令日志, MyProperty属性值为：" + add1);

            dataContext.Log.IncreaseIndent();

            dataContext.Log.AppendLine("这里是二级服务端命令日志1：" + add1);
            dataContext.Log.AppendLine("这里是二级服务端命令日志2：" + add1);

            dataContext.Log.DecreaseIndent();

            return new ExecuteResult();
        }
```

测试效果：

注意：IncreaseIndent 和 DecreaseIndent方法必须成对调用。
如果希望写诊断日志到文件中，可以使用.net 原生的 Trace方法：

```
System.Diagnostics.Trace.WriteLine("xxxx");
```

* 如果是设计器，在 %Temp%\\ForguncyDesignerLog\\App 目录下查看；
* 如果是服务器，在 %temp%\\ForguncyServerLog\\应用名\\DiagnosticLog 中查看。

---

## Thirdpartynetworkserviceinteraction

# 第三方网络服务交互

## Content

在服务端命令中，推荐使用 HttpClient 来请求网络服务。

```
using GrapeCity.Forguncy.Commands;
using System.Net.Http;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        static HttpClient _httpClient = new HttpClient();
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            var response = await _httpClient.GetAsync("https://gitee.com/grape-city-software/forguncy-plugin-project-creator/raw/master/README.md");
            if (response.IsSuccessStatusCode)
            {
                var responseContent = await response.Content.ReadAsStringAsync();
                return new ExecuteResult() { Message = responseContent };
            }
            else
            {
                return new ExecuteResult() { ErrCode = (int)response.StatusCode, Message = response.StatusCode.ToString() };
            }
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

  

代码说明：HttpClient 应该定义为静态对象以节约网络资源。