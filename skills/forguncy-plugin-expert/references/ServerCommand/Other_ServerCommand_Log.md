# 服务端命令日志记录 (Server Command Logging)

在活字格服务端命令插件开发中，日志记录是调试和监控业务逻辑的关键手段。

## 核心机制

服务端命令的日志记录通过 `IServerCommandExecuteContext` 接口提供的 `Log` 属性实现。
该属性是一个 `StringBuilder` 对象。插件执行过程中写入该 `StringBuilder` 的内容，会在命令执行结束后被活字格服务捕获，并记录到系统的服务端日志文件中（或在设计器调试控制台中显示）。

### 关键接口定义

```csharp
public interface IServerCommandExecuteContext
{
    // ... 其他属性
    StringBuilder Log { get; } // 用于记录日志
}
```

## 最佳实践与规范

### 1. 属性引用 (Log vs Logger)

*   **正确做法**：始终使用 `context.Log`。
*   **常见误区**：不要尝试使用 `Logger` 属性或 `Console.WriteLine`。在 `IServerCommandExecuteContext` 上下文中，`Logger` 属性并不存在（这通常是 ServerAPI 上下文 `ForguncyApi` 中的概念），混用会导致编译错误。

### 2. 代码示例

建议使用 `AppendLine` 方法确保每条日志独占一行，便于阅读。同时，建议在 `try-catch` 块中捕获异常并记录，以防止插件崩溃导致没有任何反馈。

```csharp
using GrapeCity.Forguncy.ServerCommands;
using System;
using System.Threading.Tasks;

public class MyServerCommand : ICommand
{
    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        // 1. 记录开始执行
        dataContext.Log.AppendLine($"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] MyPlugin: 开始执行业务逻辑...");

        try
        {
            // 获取参数示例
            var userId = "User123"; 
            dataContext.Log.AppendLine($"[Info] 当前处理用户: {userId}");

            // 模拟业务逻辑
            await Task.Delay(100);

            // 2. 记录关键节点
            dataContext.Log.AppendLine("[Info] 业务逻辑处理成功。");
        }
        catch (Exception ex)
        {
            // 3. 异常捕获与记录
            // 注意：这里将异常信息写入 Log，有助于在活字格日志中排查问题
            dataContext.Log.AppendLine($"[Error] 执行过程中发生未处理异常: {ex.Message}");
            dataContext.Log.AppendLine($"[Stack Trace] {ex.StackTrace}");
            
            // 可以选择重新抛出异常，让外层命令感知失败
            // throw; 
            
            // 或者返回错误结果
            return new ExecuteResult { ErrCode = 500, Message = ex.Message };
        }

        return new ExecuteResult();
    }
}
```

## 上下文区分 (Context Awareness)

请务必区分 **服务端命令 (Server Command)** 与 **服务端 API (Server API)** 的上下文差异：

| 插件类型 | 上下文接口 | 日志属性 | 类型 |
| :--- | :--- | :--- | :--- |
| **Server Command** | `IServerCommandExecuteContext` | `.Log` | `StringBuilder` |
| **Server API** | `ForguncyApi` (通常通过 `Context`) | `.Logger` | `ILogger` (或其他日志接口) |

> **警告**：直接复制 Server API 的代码片段到 Server Command 中往往会因为 `Logger` 属性不存在而报错。请务必确认当前所处的上下文环境。
