# 服务端命令执行函数返回值 (Server Command Execute Function Return Value)

在服务端命令插件开发中，`ExecuteAsync` 函数的返回值用于指示命令的**执行状态**（成功或失败），而不是用于直接返回业务数据。

## 核心概念

`ExecuteAsync` 方法的签名如下：

```csharp
public Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext);
```

它返回一个 `ExecuteResult` 对象，该对象主要包含命令执行后的状态信息。

## ExecuteResult 类详解

`ExecuteResult` 类主要包含以下属性：

### 1. ErrCode (int)

- **作用**：表示命令执行的状态码。
- **默认值**：`0`。
- **约定**：
    - `0`：表示执行成功。
    - 非 `0`：表示执行失败。插件开发者可以定义不同的错误码来区分错误类型。

### 2. Message (string)

- **作用**：当 `ErrCode` 不为 0 时，用于描述错误的详细信息。
- **显示**：该信息通常会被记录到日志中，或在调试模式下显示给用户。

### 3. ReturnValues (Dictionary<string, object>)

- **作用**：虽然存在此属性，但在常规插件开发中，**不推荐**主要依赖它来返回业务数据给后续命令。
- **推荐做法**：使用 `dataContext.Parameters` 将结果存入上下文变量（参考 [支持返回结果](./Process_Return_Results.md)）。

## 常见用法示例

### 场景 1：执行成功

```csharp
public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
{
    // 业务逻辑...
    
    // 返回默认对象，ErrCode 默认为 0
    return new ExecuteResult();
}
```

### 场景 2：执行失败（业务错误）

```csharp
public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
{
    if (IsInvalidState())
    {
        // 返回明确的错误码和错误信息
        return new ExecuteResult 
        { 
            ErrCode = 400, 
            Message = "当前状态不允许执行此操作" 
        };
    }
    
    return new ExecuteResult();
}
```

### 场景 3：捕获异常

虽然活字格会自动捕获未处理异常并返回 ErrCode 500，但手动捕获可以提供更友好的错误信息。

```csharp
public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
{
    try
    {
        DoRiskyOperation();
        return new ExecuteResult();
    }
    catch (Exception ex)
    {
        return new ExecuteResult 
        { 
            ErrCode = 500, 
            Message = $"操作失败：{ex.Message}" 
        };
    }
}
```

## 区分“状态”与“数据”

- **状态 (Status)**：通过 `ExecuteResult` 返回。告诉活字格平台“命令是否成功运行”。
- **数据 (Data)**：通过 `dataContext.Parameters` 写入。告诉后续命令“这是我产生的结果”。

请务必区分这两者，避免尝试通过 `ExecuteResult` 返回业务数据（如查询结果、计算值等），导致后续命令无法获取。
