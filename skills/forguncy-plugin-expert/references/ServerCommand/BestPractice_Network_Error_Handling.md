# 外部服务连接防御性编程最佳实践

## 1. 背景与痛点
在服务端插件开发中，调用外部 API（如 AI 模型服务、第三方支付接口、企业内部 ERP）是常见场景。当外部服务不可用（如服务未启动、网络中断、防火墙拦截）时，默认的异常堆栈信息（如 `System.Net.Sockets.SocketException`）通常包含大量技术细节，但对最终用户（低代码开发者或应用使用者）来说：
- **难以理解**：不清楚具体的业务影响。
- **无法行动**：不知道是配置错误、网络问题还是服务宕机。

## 2. 核心原则
1.  **区分错误类型**：将“基础设施错误”（连接失败、超时）与“业务逻辑错误”（参数无效、权限不足）区分处理。
2.  **提供行动指南**：错误信息应包含“发生了什么”以及“该怎么做”。
3.  **保护敏感信息**：避免将服务器 IP、端口或 API Key 直接暴露在未处理的异常堆栈中。

## 3. 推荐实现模式

### 3.1 基础 try-catch 结构
不要只捕获 `Exception`，应优先捕获特定的网络异常。

```csharp
using System.Net.Http;
using System.Threading.Tasks;

// ...

try 
{
    // 执行外部 API 调用
    var response = await httpClient.PostAsync(url, content);
    response.EnsureSuccessStatusCode();
}
catch (HttpRequestException ex)
{
    // 场景：网络连接失败（DNS 解析失败、连接拒绝、超时）
    // 转换：包装为友好的业务异常
    throw new Exception($"无法连接到 [目标服务名称] (URL: {url})。请检查：\n1. 服务是否已启动？\n2. 网络配置是否正确？\n3. 防火墙是否允许访问？", ex);
}
catch (TaskCanceledException ex) when (ex.CancellationToken != cancellationToken)
{
    // 场景：请求超时
    throw new Exception($"连接 [目标服务名称] 超时。请检查网络状况或联系管理员。", ex);
}
catch (Exception ex)
{
    // 场景：其他未知错误
    // 记录日志并抛出通用错误
    this.Context.Log.AppendLine($"未知错误: {ex.ToString()}");
    throw new Exception("处理请求时发生未知错误，请查看服务器日志了解详情。", ex);
}
```

### 3.2 进阶：自愈引导与文档链接
对于复杂的集成场景，建议在错误信息中附带排查文档链接。

```csharp
catch (HttpRequestException ex)
{
    var helpUrl = "https://your-docs.com/troubleshooting/connection-refused";
    var errorMsg = $"服务连接失败。错误代码: NET_ERR_01。\n排查指南: {helpUrl}";
    
    // 如果是活字格环境，可以使用特定的日志记录方式（如果有）
    // 最终抛出一个包含帮助信息的异常
    throw new Exception(errorMsg, ex);
}
```

### 3.3 陷阱警示：预检请求与版本协商 (Pre-flight Checks)
在执行核心业务前进行版本检查（CheckVersion）或健康检查（HealthCheck）时，**严禁**使用宽泛的 `try-catch` 吞没网络错误。

**错误示范**（会导致“无法连接”被误报为“版本过低”）：
```csharp
try {
    var version = await CheckVersionAsync(); // 如果这里连接失败抛出异常
    if (version < RequiredVersion) throw new Exception("版本过低");
}
catch {
    // 错误！所有异常（包括网络中断）都会被视为版本不匹配
    throw new Exception("服务端版本过低，请升级。"); 
}
```

**正确示范**：
```csharp
try {
    var version = await CheckVersionAsync();
    if (version < RequiredVersion) 
    {
        // 明确的逻辑不匹配
        throw new Exception($"服务端版本过低 (当前: {version}, 需要: {RequiredVersion})。请升级服务。");
    }
}
catch (HttpRequestException ex)
{
    // 明确的连接失败
    throw new Exception("无法连接到版本检查接口，请检查网络设置。", ex);
}
// 其他异常正常冒泡或单独处理
```

## 4. 常见异常对照表

| 异常类型                              | 常见原因               | 建议提示文案                                              |
| :------------------------------------ | :--------------------- | :-------------------------------------------------------- |
| `SocketException` (ConnectionRefused) | 服务未启动、端口错误   | “目标计算机积极拒绝连接，请确认服务是否在端口 X 上运行。” |
| `HttpRequestException` (401/403)      | API Key 无效、权限不足 | “认证失败，请检查插件配置中的 API Key 是否正确。”         |
| `HttpRequestException` (404)          | 接口地址变更、配置错误 | “找不到指定的 API 端点，请检查服务地址配置。”             |
| `TaskCanceledException`               | 网络慢、服务响应超时   | “请求超时，服务响应时间过长。”                            |

## 5. 总结
优秀的插件不仅功能强大，更具备良好的**可支持性**。通过防御性编程，我们可以将 80% 的“环境配置问题”拦截在第一线，显著降低用户的挫败感和技术支持成本。
