> Source: usecachingservice.md (Imported from external documentation)

# 使用缓存服务

## Content

### <span class="ne-text">缓存服务可以给中间件提供以下能力</span>

1. <span class="ne-text">获取缓存</span>
2. <span class="ne-text">设置缓存并指定缓存过期时间</span>

### <span class="ne-text">需要缓存的数据应该满足以下条件</span>

1. <span class="ne-text">获取数据时比较耗时，如数据库查询或请求第三方Web服务</span>
2. <span class="ne-text">此数据应该是修改不频繁或对数据的实时性要求不高</span>

### <span class="ne-text">缓存服务端的底层实现</span>

<span class="ne-text">缓存服务端在默认情况下使用 MemoryCache， 在负载均衡模式下会自动使用 Radis 数据库。</span>

### <span class="ne-text">示例代码</span>

#### <span class="ne-text">如何在中间件中获取应用程序服务（ICacheService）</span>

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
                var cacheService = context.RequestServices.GetService<ICacheService>();

                var key = "MyCacheKey";
                if (cacheService.Exists(key))
                {
                    // 判断要获取的数据在缓存中存在则直接返回
                    await context.Response.WriteAsync(cacheService.Get(key).ToString());
                }
                // 获取数据
                var cacheValue = "testValue";
                cacheService.Add(key, cacheValue, TimeSpan.FromSeconds(100)); // 添加到缓存中，100秒之后缓存会自动过期
                await context.Response.WriteAsync(cacheValue);
                return;
            }
            await _next(context);
        }
    }
}
```

### <span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 32px;">对应活字格版本</span>

<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">大于等于活字格9.0.100.0版本。</span>