> Source: integrate-aspnet-core-controller-and-razorpage.md (Imported from external documentation)

# 如何集成Asp.net Core的Controller和RazorPage

## Content

如果做过 Asp.net Core开发，对 Controller （控制器）和 Razor Page 一定很熟悉。由于活字格服务器是用 Asp.net Core 开发的。所以同样也可以集成 Asp.net Core 的 Controller 和 Razor Page。
首先，请参考[开发自定义中间件](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcustommiddleware)章节，注册MyPlugin.Server 工程到插件中。

## 集成Controller

编辑 MyPluginMiddlewareInjector.cs 方法。修改 ConfigureServices 方法如下：

```auto
        public override List<ServiceItem> ConfigureServices(List<ServiceItem> serviceItems, IServiceCollection services)
        {
            serviceItems.Add(new ServiceItem()
            {
                Id = "7d467202-8432-4910-b32c-ebd806d00a5d",
                ConfigureServiceAction = () =>
                {
                    var assembly = Assembly.GetExecutingAssembly();

                    // 注册控制器
                    services.AddControllersWithViews().PartManager.ApplicationParts.Add(new AssemblyPart(assembly));
                },
                Description = "注册控制器"
            });

            return base.ConfigureServices(serviceItems, services);
        }
```

`services.AddControllersWithViews().PartManager.ApplicationParts` 代码可以让 Asp.net Core 通过反射查找当前程序集中的 Controller。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.d60d0c.png)
然后添加控制器即可。
1.右击 MyPlugin.Server 工程，单击“添加->新项目”。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.335dfe.png)
2.选择“API 控制器-空”。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.f4b9ba.png)
3.给 MyController 添加一个 Action。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.b23a34.png)
4.测试代码。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.1b2406.png)
之所以用“ api/My” 访问是因为默认的路由设置 [Route("api/[controller]")]。
“api”为前缀，“My”为控制器的名称。可以通过修改路由配置来控制其他路由方式。注意不要和活字格的默认路由冲突。

## 集成 Razor Page

集成 Razor Page 的方式和集成 Controller类似。
首先，相对于集成 Controller ，集成 Razor Page 需要额外添加一句`services.AddRazorPages().PartManager.ApplicationParts.Add(new CompiledRazorAssemblyPart(assembly));`
代码如下：

```auto
        public override List<ServiceItem> ConfigureServices(List<ServiceItem> serviceItems, IServiceCollection services)
        {
            serviceItems.Add(new ServiceItem()
            {
                Id = "7d467202-8432-4910-b32c-ebd806d00a5d",
                ConfigureServiceAction = () =>
                {
                    var assembly = Assembly.GetExecutingAssembly();

                    // 注册控制器
                    services.AddControllersWithViews().PartManager.ApplicationParts.Add(new AssemblyPart(assembly));

                    // 注册 Razor Page
                    services.AddRazorPages().PartManager.ApplicationParts.Add(new CompiledRazorAssemblyPart(assembly));
                },
                Description = "注册控制器"
            });

            return base.ConfigureServices(serviceItems, services);
        }
```

修改之后就可以添加 Razor Page 了。
1.右击“MyPlugin.Server”工程，单击“添加->新项目”，选择添加“Razor视图-空”。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.bb5c43.png)
2.添加之后，修改Razor页面的内容。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.cfcc1f.png)

>type=warning
> 注意，一定要修改 MyPage.cshtml 的“复制到输出目录”属性修改为“始终复制”否则插件产出物中不会包含 MyPage.cshtml 文件。

3.右击“MyPlugin.Server”工程，单击“添加->新项目”，选择添加“MVC控制器-空”。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.b1ee16.png)
4.修改 Index 方法，让 MvcController 和 MyPage.cshtml 关联。

```auto
using Microsoft.AspNetCore.Mvc;

namespace MyPlugin.Server
{
    public class MyRazorPageController : Controller
    {
        public IActionResult Index()
        {
            return View("MyPage.cshtml");
        }
    }
}
```

![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.7c5e2f.png)
5.运行查看效果。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.abd3fd.png)
默认的路由是“Controller/Action”，可以通过添加 [Route] 来配置自定义路由。注意不要和活字格的默认路由冲突。

## 给 Razor Page 添加 Model

上例中添加了Razor Page，但是没有添加Model，这样就只能显示一个静态页面。通常Razor Page通过绑定一个Model来实现动态页面的服务端渲染。以下代码演示了如何给Razor页面添加PageModel。
1.首先修改 MyRazorPageController.cs 文件如下：

```auto
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace MyPlugin.Server
{
    public class MyRazorPageController : Controller
    {
        public IActionResult Index()
        {
            var model = new MyRazorPageModel()
            {
                MyTitle = "我的自定义标题",
                MyBody = "我的自定义内容"
            };

            return View("MyPage.cshtml", model);
        }
    }
    public class MyRazorPageModel : PageModel
    {
        public string MyTitle { get; set; }
        public string MyBody { get; set; }
    }
}
```

![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.732bfb.png)
代码说明：

1. 代码 MyRazorPageController.cs 文件；
2. 定义 MyRazorPageModel 类从 RageModel 派生；
3. 通过 View 方法的第二个参数设置 model 把 MyPage.cshtml 和 MyRazorPageModel 的实例绑定。

2.然后修改 MyPage.cshtml 中的代码：

```html
@using MyPlugin.Server
@model MyRazorPageModel
@{
}
<html>
    <head>
        <title>@Model.MyTitle</title>
    </head>
    <body>
        <h1>我的Razor页面</h1>
    </body>
</html>
```

![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.57e15d.png)
代码说明：

1. 打开 MyPage.cshtml 文件；
2. 声明页面的 Model 类型为 MyRazorPageModel；
3. 在 cshtml 代码中通过 @Model.MyBody 使用 Model 中的属性。

3.运行时效果：
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.46ca24.png)