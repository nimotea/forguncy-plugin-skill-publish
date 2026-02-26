# 添加属性 - 服务端命令选择属性 (Server Command Selection)

该属性允许用户在设计器中选择当前应用中已存在的其他“服务端命令”。插件可以在运行时调用选中的服务端命令。
*(此特性为活字格 V9.1 新增功能)*

## 1. 基础用法
使用 `[ServerCommandNameProperty]` 特性标记字符串属性。

### 代码示例
```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("调用回调命令")]
    [ServerCommandNameProperty]
    public string CallbackCommandName { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        // 如果用户选择了一个命令
        if (!string.IsNullOrEmpty(CallbackCommandName))
        {
            // 执行该服务端命令
            // 注意：第二个参数传递当前的上下文，以便被调用的命令可以访问上下文变量
            await dataContext.ExecuteServerCommandsAsync(this.CallbackCommandName, dataContext);
        }

        return new ExecuteResult();
    }
}
```

## 2. 运行时行为
- `ExecuteServerCommandsAsync` 方法会异步执行指定名称的服务端命令。
- 如果指定的服务端命令不存在，该方法可能会抛出异常或静默失败（取决于活字格版本），建议在调用前判空。
- 被调用的服务端命令将在当前上下文中执行，共享变量和事务（如果支持）。
