> Source: asimplecommandplugin.md (Imported from external documentation)

# 一个简单的命令插件

## Content


开始本教程前，请确保已经仔细阅读了[快速开始](/solutions/huozige/help/docs/plugindevelopment/quickstart)章节，并已经完成了环境准备，并通过活字格插件构建器创建了默认工程。后续的文档都会基于活字格插件构建器创建的空白工程进行讲解。

  

现在，我们已经通过活字格插件构建工具开发了第一个命令插件，但是这个命令插件没有任何逻辑，我们需要编写C#和JavaScript代码来添加插件的业务逻辑。

首先，先查看代码结构。

![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958146/image2023-1-18_16-40-37.png)

修改单元格插件，我们重点关注两个文件：MyPluginCommand.cs 和 MyPluginCommand.js。

MyPluginCommand.cs 默认代码如下：

```
    [Icon("pack://application:,,,/MyPlugin;component/Resources/Icon.png")]
    [Designer("MyPlugin.Designer.MyPluginCommandDesigner, MyPlugin")]
    public class MyPluginCommand : Command
    {
        [DisplayName("命令属性")]
        [FormulaProperty]
        public object MyProperty { get; set; }

        public override string ToString()
        {
            return "我的插件命令";
        }
    }
```

1.  第一行代码 \[Icon("pack://application:,,,/MyPlugin;component/Resources/Icon.png")\] 用于指定图标文件的位置。
2.  第二行代码 \[Designer("MyPlugin.Designer.MyPluginCommandDesigner, MyPlugin")\] 用于指定设计时功能所在的类，刚开始开发插件时可以无视这句。
3.  第三行 public class MyPluginCommand : Command 用于定义命令类型，必须从 Command 类或其子类派生。
4.  第五行 public object MyProperty { get; set; } 定义了一个示例属性。
5.  第九行重写了 ToString() 方法指定了在设计器中命令显示的文本。

MyPluginCommand.js 默认代码如下：

```
/// <reference path="../Declarations/forguncy.d.ts" />
/// <reference path="../Declarations/forguncy.Plugin.d.ts" />
class MyPluginCommand extends Forguncy.Plugin.CommandBase{
    execute() {
        // 获取MyProperty属性值，注意，这里的MyProperty应该与 MyPluginCommand.cs 文件定义的属性名一致
        let text = this.CommandParam.MyProperty; 
        // MyProperty 属性的值可能是用户提供的公式，所以这里通过 evaluateFormula 方法计算出真实的值
        text = this.evaluateFormula(text);
        
        alert(text);
    }
}

Forguncy.Plugin.CommandFactory.registerCommand("MyPlugin.MyPluginCommand, MyPlugin", MyPluginCommand);
```

1.  第一行和第二行声明了活字格接口 ".d.ts" 文件的位置，以便在编写JavaScript代码时一个提供代码补全，提高开发效率。  
    ![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958146/image2023-1-18_16-41-40.png)  
    
2.  第三行定义了 MyPluginCommand 类型，必须从 Forguncy.Plugin.CommandBase 派生。
3.  第4行到第11行重写了 execute 方法，获取自定义属性的值，通过evaluateFormula计算可能的公式结果，并通过 alert 方法在消息框中显示计算后的值。命令的执行逻辑都会写到这里。后续的教程中，主要是修改这个函数的实现来达成各种效果。
4.  第14行注册这个写的命令给活字格，这样活字格才知道有一个新的命令插件加入了。registerCommand方法的第一个参数格式： 【命令名字空间】.【命令名称】,【空格】【应用程序集名称】。

  

好，我们已经了解了命令插件的代码结构，让我们做一些小的修改来简单尝试一下开发一个命令插件吧。

比如，我们希望开发一个计算加法的命令。我们把 MyPluginCommand.cs 修改如下。

```
    public class MyPluginCommand : Command
    {
        [DisplayName("加数1")]
        [FormulaProperty]
        public object AddNumber1 { get; set; }

        [DisplayName("加数2")]
        [FormulaProperty]
        public object AddNumber2 { get; set; }

        public override string ToString()
        {
            return "我的加法命令";
        }
    }
```

MyPluginCellType.js 代码修改如下：

```
class MyPluginCommand extends Forguncy.Plugin.CommandBase{
    execute() {
        const add1Formula = this.CommandParam.AddNumber1; 
        const add2Formula = this.CommandParam.AddNumber2; 

        const add1 = this.evaluateFormula(add1Formula);
        const add2 = this.evaluateFormula(add2Formula);

        const result = Number(add1) + Number(add2);
        alert(add1 + "与" + add2 + "相加结果为" + result);
    }
}

Forguncy.Plugin.CommandFactory.registerCommand("MyPlugin.MyPluginCommand, MyPlugin", MyPluginCommand);
```

修改之后，编译代码，重启设计器。

在设计器中找到 “我的加法命令”命令插件，把命令添加到按钮命令上。我们可以看见在命令设置面板中多了2个设置，正好和C#代码中的2个属性对应。  
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958146/image2023-1-18_16-42-52.png)  

在页面上添加两个文本框，并通过公式设置命令的属性值与文本框绑定。

![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958146/image2023-1-18_16-43-4.png)单击绿色开始按钮之后，在文本框中输入数字，单击按钮。

![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958146/image2023-1-18_16-43-17.png)

在单元格里设置不同的值，就可以计算不同数字的相加结果。

也许你还不理解这些代码的意思，没关系，后续的教程中对这些代码都会有详细的解释。