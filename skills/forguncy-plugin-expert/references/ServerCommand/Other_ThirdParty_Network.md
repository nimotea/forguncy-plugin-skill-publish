# 第三方网络服务交互 (Third-party Network Interaction)

在服务端命令插件中，经常需要调用外部的 REST API 或其他网络服务。虽然可以使用 .NET 标准的 `HttpClient`，但建议遵循一定的最佳实践以确保性能和稳定性。

## 推荐方式

在插件中，可以直接使用 .NET 提供的 `System.Net.Http.HttpClient` 类。为了避免端口耗尽（Socket Exhaustion）等问题，建议使用静态实例或依赖注入（如果环境支持）。

### 代码示例

```csharp
using System.Net.Http;
using System.Threading.Tasks;

public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    // 建议声明为静态只读，以复用连接池
    private static readonly HttpClient client = new HttpClient();

    [FormulaProperty]
    [DisplayName("API 地址")]
    public object Url { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        string apiUrl = Url?.ToString();
        if (string.IsNullOrEmpty(apiUrl))
        {
            return new ExecuteResult { ErrCode = 1, Message = "URL 不能为空" };
        }

        try
        {
            // 发起 GET 请求
            var response = await client.GetAsync(apiUrl);
            
            // 确保请求成功
            response.EnsureSuccessStatusCode();
            
            // 读取内容
            var responseBody = await response.Content.ReadAsStringAsync();

            // 记录日志
            dataContext.Log.AppendLine($"请求成功，返回长度：{responseBody.Length}");

            // 可以将结果存入变量（参考“支持返回结果”章节）
            // ...
        }
        catch (HttpRequestException e)
        {
            return new ExecuteResult { ErrCode = 500, Message = $"请求异常: {e.Message}" };
        }

        return new ExecuteResult();
    }
}
```

## 注意事项

1.  **HttpClient 生命周期**：不要在每次 `ExecuteAsync` 中都 `new HttpClient()` 且使用 `using` 包裹，这在高并发下会导致 TIME_WAIT 状态的连接过多，引发 `SocketException`。建议使用静态实例 `static readonly HttpClient`。
2.  **超时设置**：可以通过 `client.Timeout` 设置超时时间，防止外部服务卡死导致插件长时间挂起。
3.  **异步编程**：务必使用 `await` 异步调用网络方法，不要使用 `.Result` 或 `.Wait()`，以免阻塞线程池导致死锁。
4.  **代理支持**：如果服务器环境需要代理访问外网，需要在初始化 `HttpClient` 时配置 `HttpClientHandler`。

## 高级用法

对于复杂的 JSON 处理，建议引入 `Newtonsoft.Json` (Json.NET) 库来序列化和反序列化请求/响应数据。

```csharp
// 序列化请求体
var jsonContent = new StringContent(JsonConvert.SerializeObject(payload), Encoding.UTF8, "application/json");
var response = await client.PostAsync(url, jsonContent);
```
