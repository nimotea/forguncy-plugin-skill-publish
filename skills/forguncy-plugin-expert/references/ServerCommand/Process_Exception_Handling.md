# 异常处理 (Exception Handling)

在服务端命令插件开发中，正确处理异常和返回错误状态对于保证系统稳定性和调试便利性至关重要。

## 核心机制

服务端命令的核心执行方法是 `ExecuteAsync`，其返回值类型为 `ExecuteResult`。

### 返回值约定

- **成功**：`ExecuteResult.ErrCode` 为 `0`（默认值）。
- **失败**：`ExecuteResult.ErrCode` 为非 `0` 值。

### 自定义错误码

当存在多种错误情况时，插件开发者可以自行定义不同的 `ErrCode`，以便于前端区分错误类型或进行调试。

### 未处理异常

如果 `ExecuteAsync` 方法中抛出了未捕获的异常（Unhandled Exception），活字格平台会自动处理：
1. 将 `ExecuteResult.ErrCode` 设置为 `500`。
2. 将 `ExecuteResult.Message` 设置为异常的详细信息。
3. 生成错误日志。

## 代码示例

```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        // 示例：检查权限
        if (CheckPermission() == false)
        {
            // 返回自定义错误码 1 和错误消息
            return new ExecuteResult() { ErrCode = 1, Message = "权限不足，无法执行操作" };
        }

        // 示例：检查业务条件
        if (NotEnoughStorage())
        {
            // 返回自定义错误码 2 和错误消息
            return new ExecuteResult() { ErrCode = 2, Message = "库存不足" };
        }

        try 
        {
            // 执行核心业务逻辑
            DoSomething();
        }
        catch (Exception ex)
        {
            // 也可以手动捕获异常并封装返回
            return new ExecuteResult() { ErrCode = 999, Message = $"执行出错: {ex.Message}" };
        }

        // 成功执行（ErrCode 默认为 0）
        return new ExecuteResult();
    }

    public override CommandScope GetCommandScope()
    {
        return CommandScope.ExecutableInServer;
    }
    
    // 模拟辅助方法
    private bool CheckPermission() => true;
    private bool NotEnoughStorage() => false;
    private void DoSomething() { }
}
```
