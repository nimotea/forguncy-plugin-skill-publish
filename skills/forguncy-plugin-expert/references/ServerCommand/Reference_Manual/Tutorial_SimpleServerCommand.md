> Source: asimpleservercommandplugin.md (Imported from external documentation)

# 一个简单的服务端命令插件

## Content

开始本教程前，请确保已经仔细阅读了[快速开始](/solutions/huozige/help/docs/plugindevelopment/quickstart)章节，并已经完成了环境准备，并通过活字格插件构建器创建了默认工程。后续的文档都会基于活字格插件构建器创建的空白工程进行讲解。
现在，我们已经通过活字格插件构建工具开发了第一个服务端命令插件。
首先查看代码结构。
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958483/image2023-1-19_13-50-35.png)

修改服务端命令插件，我们核心关注 MyPluginServerCommand.cs。

MyPluginServerCommand.cs 默认代码如下：

```auto
[Icon("pack://application:,,,/MyPlugin;component/Resources/Icon.png")]
    [Designer("MyPlugin.Designer.MyPluginServerCommandDesigner, MyPlugin")]
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [FormulaProperty]
        [DisplayName("加数1")]
        public object AddNumber1 { get; set; }

        [FormulaProperty]
        [DisplayName("加数2")]
        public object AddNumber2 { get; set; }

        [ResultToProperty]
        [DisplayName("相加结果")]
        public string ResultTo { get; set; } = "结果";

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            var add1 = await dataContext.EvaluateFormulaAsync(AddNumber1); // 计算的一个加数的公式值
            var add2 = await dataContext.EvaluateFormulaAsync(AddNumber2); // 计算第二个家属的公式值

            double.TryParse(add1?.ToString(), out var add1Number); // 对第一个加数做类型转换
            double.TryParse(add2?.ToString(), out var add2Number); // 对第二个加数做类型转换

            dataContext.Parameters[ResultTo] = add1Number + add2Number;  // 把计算的结果设置到结果变量中

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
```

1. 第一行代码 [Icon("pack://application:,,,/MyPlugin;component/Resources/Icon.png")] 用于指定图标文件的位置。
2. 第二行代码 [Designer("MyPlugin.Designer.MyPluginServerCommandDesigner, MyPlugin")] 用于指定设计时功能所在的类，刚开始开发插件时可以无视这句。
3. 第三行 public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync 用于定义服务端命令类型，必须从 Command 类或其子类派生，并且实现 ICommandExecutableInServerSideAsync 接口。
4. 第五行至第十五行 定义了两个公式属性“加数1”和“加数2”，以及一个返回值属性“相加结果”。开发者需要根据自己的业务需求定义属性，关于如何定义和使用属性，在后续添加属性章节中有详细的讲解。
5. 第十七到第二十八行 定义了 ExecuteAsync 方法，ExecuteAsync 方法是服务端命令的核心函数，用于定义服务端命令的执行逻辑，当服务端命令执行时，这个函数会被调用。示例代码中，ExecuteAsync 函数通过 dataContext.EvaluateFormulaAsync方法计算了两个加数的值，并把相加的结果回存到了结果变量中，完成了基本的执行逻辑。开发者需要根据业务需求重写这部分代码。
6. 第三十行重写了 ToString() 方法指定了在设计器中服务端命令显示的文本。
7. 第三十五行，GetCommandScope 函数用于定义服务端命令的使用范围。服务端命令可以控制仅在服务端命令（ServerSide）中使用，仅在计划任务（TaskSchedule）中使用，或者全部支持（ExecutableInServer）。

编译代码，重启设计器。
在设计器中找到 “我的插件服务端命令”服务端命令插件，可以看到定义的属性如下。
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958483/image2023-1-19_13-51-43.png)

给服务端命令定义“参数1”和“参数2”。
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958483/image2023-1-19_13-52-11.png)

并修改“我的插件服务端命令”。
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958483/image2023-1-19_13-52-36.png)

单击测试。
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958483/image2023-1-19_13-52-56.png)

在弹出的对话框中添加设置参数。
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958483/image2023-1-19_13-53-9.png)

查看结果页面。
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958483/image2023-1-19_13-53-19.png)

也许你还不理解这些代码的意思，没关系，后续的教程中对这些代码都会有详细的解释。
ICommandExecutableInServerSide **Vs** ICommandExecutableInServerSideAsync：
在活字格早期版本中会通过实现 ICommandExecutableInServerSide 接口的Execute方法来定义服务端命令。新版活字格增加了 ICommandExecutableInServerSideAsync 接口和 ExecuteAsync 方法。如果开发新的服务端命令，推荐使用 ICommandExecutableInServerSideAsync 加 async await 语法来实现异步逻辑。如果工具方法同时提供了 Async 方法和同步方法，推荐使用 Async 加 await 关键字。async await 可以显著提示服务端命令在高并发访问情况下的性能表现。