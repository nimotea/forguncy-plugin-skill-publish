> Source: useapplicationservices.md (Imported from external documentation)

# 使用应用程序服务

## Content

### <span class="ne-text">应用程序服务可以给中间件提供以下能力</span>

1. <span class="ne-text">获取应用程序信息，包括应用程序名，BaseUrl，应用程序的物理路径等</span>
2. <span class="ne-text">获取IUserInfos，获取应用程序的用户，角色，组织等信息，并提供了相应的操作接口</span>
3. <span class="ne-text">获取IDataAccess, IDataAccess提供了对活字格数据表的增删改查操作接口</span>
4. <span class="ne-text">获取应用程序的附件存储信息，如附件存储的物理路径等</span>

### <span class="ne-text">示例代码</span>

#### <span class="ne-text">如何在中间件中获取应用程序服务（IApplicationInformationService）</span>

<span class="ne-text">应用程序服务会在活字格启动时注册到Asp.net 的服务容器中，使用时只需要通过GetService方法即可获取。</span>

```
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
                var appService = context.RequestServices.GetService<IApplicationInformationService>();

                await context.Response.WriteAsync(appService.ApplicationName);
                return;
            }
            await _next(context);
        }
    }
}
```

#### <span class="ne-text">如何在服务端命令中获取应用获取应用程序服务（IApplicationInformationService）</span>

<span class="ne-text">IApplicationInformationService 同样可以在服务端命令中使用，使用方法和中间件类似。</span>

```
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
            var appService = dataContext.ServiceProvider.GetService<IApplicationInformationService>();
            return new ExecuteResult()
            {
                Message = "Application Name: " + appService.ApplicationName
            };
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

#### <span class="ne-text">通过IApplicationInformationService获取应用程序信息</span>

```
var appService = context.RequestServices.GetService<IApplicationInformationService>();
// 获取应用程序名称
var appName = appService.ApplicationName;
// 获取应用程序BaseUrl
var appBaseUrl = appService.ApplicationBaseUrl;
// 获取应用程序在服务器上的物理存储路径
var appStragePath = appService.ApplicationStoragePath;
// 是否是在设计器中运行
var isRunAtDesigner = appService.IsRunAtDesigner;
```

#### <span class="ne-text">通过IApplicationInformationService获取用户信息</span>

```
var appService = context.RequestServices.GetService<IApplicationInformationService>();
// 获取用户服务
var userInfos = appService.UserInfos;
// 获取所有用户信息
var users = await userInfos.GetUserInfosAsync();

var userName = "Administrator";
// 使用用户名获取用户的详细信息
var user = await userInfos.GetUserInfoAsync(userName);
// 使用用户名获取用户的权限信息
var permissions = await userInfos.GetRolesOfUserOwnedPermissionsAsync(userName);
```

#### <span class="ne-text">通过IApplicationInformationService操作数据库</span>

```
var appService = context.RequestServices.GetService<IApplicationInformationService>();
// 获取用户服务
var dataAccess = appService.GetDataAccess(context);

// 获取表1中，ID为1的数据
var rowData = await dataAccess.GetTableDataAsync("表1", new ColumnValuePair() { ColumnName = "ID", Value = 1 });

// 获取表1的所有数据
var rows = await dataAccess.GetTableDataAsync("表1") as List<Dictionary<string, object>>;

// 在表1中添加一行数据
await dataAccess.AddTableDataAsync("表1", new Dictionary<string, object>
{
    {"姓名", "张三" },
    {"年龄",30 }
});
// 更新表1中ID为1的数据
await dataAccess.UpdateTableDataAsync("表1", new ColumnValuePair() { ColumnName = "ID", Value = 1 },
    new Dictionary<string, object>
{
    {"姓名", "张三" },
    {"年龄",30 }
});
// 删除表1中ID为1的数据
await dataAccess.DeleteTableDataAsync("表1", new ColumnValuePair() { ColumnName = "ID", Value = 1 });
```

#### <span class="ne-text">通过IApplicationInformationService获取附件存储信息</span>

```
var appService = context.RequestServices.GetService<IApplicationInformationService>();

// 获取附件在服务器上保存的物理文件夹路径
var uploadFolderPath = appService.ApplicationAttachmentStorageInfo.LocalUploadFolderPath;
```

### <span class="ne-text">对应活字格版本</span>

<span class="ne-text">大于等于活字格9.0.100.0版本。</span>

