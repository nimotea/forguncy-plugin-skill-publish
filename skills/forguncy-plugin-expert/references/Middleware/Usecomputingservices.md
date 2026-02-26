> Source: usecomputingservices.md (Imported from external documentation)

# 使用计算服务

## Content

### 计算服务可以给中间件提供以下能力

1. 获取全局变量的值
2. 修改全局变量的值

### 示例代码

#### 如何在中间件中获取应用程序服务（ICalcService）

应用程序服务会在活字格启动时注册到Asp.net 的服务容器中，使用时只需要通过GetService方法即可获取。

```auto
using GrapeCity.Forguncy.ServerApi;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.DependencyInjection;
using System.Threading.Tasks;

namespace MyPlugin.Server
{
    internal class MyPluginMiddleware
    {
        private readonly RequestDelegate _next;
        public MyPluginMiddleware(RequestDelegate next)
        {
            _next = next;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            if (context.Request.Path.Value == "/MyPluginMiddleware")
            {
                var calcService = context.RequestServices.GetService<ICalcService>();
                // 修改全局变量的值
                await calcService.SetGlobalVariableValueAsync("MyVar", "test");
                // 获取全局变量的值
                var appKey = await calcService.GetGlobalVariableValueAsync("MyAppKey");
                await context.Response.WriteAsync(appKey);
                return;
            }
            await _next(context);
        }
    }
}
```

#### 如何在服务端命令中获取应用获取应用程序服务（IApplicationInformationService）

IApplicationInformationService 同样可以在服务端命令中使用，使用方法和中间件类似。

```auto
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.ServerApi;
using Microsoft.Extensions.DependencyInjection;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            var calcService = dataContext.ServiceProvider.GetService<ICalcService>();
            // 修改全局变量的值
            await calcService.SetGlobalVariableValueAsync("MyVar", "test");
            // 获取全局变量的值
            var appKey = await calcService.GetGlobalVariableValueAsync("MyAppKey");
            return new ExecuteResult()
            {
                Message = "Application Key: " + appKey
            };
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

### <span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 32px;">对应活字格版本

<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">大于等于活字格9.0.100.0版本。