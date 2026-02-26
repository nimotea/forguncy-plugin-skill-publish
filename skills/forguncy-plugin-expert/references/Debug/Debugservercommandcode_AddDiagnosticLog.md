> Source: add-diagnostic-log.md (Imported from external documentation)

# 添加诊断日志

## Content

此特性为V10.0.0.0新增的功能。
有时，有些问题可能只会在生产环境下发生。这种问题很难通过挂载集成开发环境来单步调试。添加适当的诊断日志对于排查问题非常有帮助。

#### 添加依赖

V10 最新版的插件构建工具会默认添加了日志相关的依赖。如果是使用最新版构建工具开发新插件不可以跳过此节。
如果是从V10之前版本升级插件，添加对 "活字安装路径\\Website\\bin\\Forguncy.Log.Abstractions.dll" 的引用。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.a432cd.png)
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.640fc4.png)

#### 添加日志代码

在代码的usring部分添加`using GrapeCity.Forguncy.Log;`
在代码需要记录日志的地方添加`Logger.Info("日志内容");`
这个 Logger 可以在所有 C# 代码中使用，包括服务端命令，自定义中间件，单元格插件，命令插件等。

```csharp
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Log;
using System;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            Logger.Info("#我的服务端命令# 这里是我的服务端命令记录的审计日志");

            Logger.Error("#我的服务端命令# 这里是一个错误日志，程序出错用于程序出错时使用");

            try
            {
                throw new Exception("程序出错了，快看看日志是什么情况");
            }
            catch (System.Exception e)
            {
                Logger.Exception(e);
            }

            return new ExecuteResult();
        }

        public override string ToString()
        {
            return "我的插件服务端命令";
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

#### 接口说明

Logger 类上有很多方法供不同场景下使用

| Info(string message) | 记录信息级别日志 |
| -------------------- | -------- |
| Error(string message) | 记录错误级别日志 |
| Warning(string message) | 记录警告级别日志 |
| Debug(string message) | 记录调试级别日志 |
| Trace(string message) | 记录跟踪级别日志 |
| Exception(Exception exception) | 记录异常日志，包括异常的详细信息，如调用堆栈等 |

日志的级别从低到高为：跟踪<调试<信息<警告<错误。活字格默认日志级别为信息，最终用户可以修改日志级别配置。出于性能考虑，如果日志特别多的情况，可以设置为调试级别。这样默认不会写入，只有需要追踪问题时，降低日志级别才需要记录。
异常日志的日志级别会被认为是 Warning, 对应为处理异常，应该记录为 Error。

#### 查看日志

对于已经发布的应用程序，可以在管理控制台查看诊断日志。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.c45f3e.png)
如果想要在设计器调试的时候查看日志，需要在 %temp%\\ForguncyDesignerLog\\App\\DiagnosticLog 找到日志文件, 查看日志内容。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.517566.png?width=1200)