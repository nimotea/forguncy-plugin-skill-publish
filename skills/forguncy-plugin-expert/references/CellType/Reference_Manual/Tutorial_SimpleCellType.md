> Source: asimplecelltypeplugin.md (Imported from external documentation)

# 一个简单的单元格插件

## Content

开始本教程前，请确保已经仔细阅读了\[快速开始\]\(第五十四章 活字格插件开发/快速开始\)章节，并已经完成了环境准备，并通过活字格插件构建器创建了默认工程。后续的文档都会基于活字格插件构建器创建的空白工程进行讲解。
现在，我们已经通过活字格插件构建工具开发了第一个单元格插件，但是这个单元格插件没有任何逻辑，我们需要编写C#和JavaScript代码来添加插件的业务逻辑。
首先，先查看代码结构。
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80957814/image2023-1-17_17-21-43.png)

修改单元格插件，我们重点关注两个文件：MyPluginCellType.cs 和 MyPluginCellType.js。
MyPluginCellType.cs 默认代码如下：

```auto
[Icon("pack://application:,,,/MyPlugin;component/Resources/Icon.png")]
    [Designer("MyPlugin.Designer.MyPluginCellTypeDesigner, MyPlugin")]
    public class MyPluginCellType : CellType
    {
        public string MyProperty { get; set; } = "MyPlugin";

        public override string ToString()
        {
            return "我的插件单元格";
        }
    }
```

1. 第一行代码 [Icon("[pack://application:,,,/MyPlugin;component/Resources/Icon.png](pack://application,,,)")] 用于指定图标文件的位置
2. 第二行代码 [Designer("MyPlugin.Designer.MyPluginCellTypeDesigner, MyPlugin")] 用于指定设计时功能所在的类，通常用于实现设计时预览，刚开始开发插件时可以无视这句
3. 第三行 public class MyPluginCellType : CellType 用于定义单元格类型，必须从 CellType 类或其子类派生。
4. 第五行 public string MyProperty { get; set; } = "MyPlugin"; 定义了一个示例属性
5. 第九行重写了 ToString() 方法指定了在设计器中单元格显示的文本

MyPluginCellType.js 默认代码如下：

```auto
/// <reference path="../Declarations/forguncy.d.ts" />
/// <reference path="../Declarations/forguncy.Plugin.d.ts" />
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        // 获取MyProperty属性值，注意，这里的MyProperty应该与 MyPluginCellType.cs 文件定义的属性名一致
        const propValue = this.CellElement.CellType.MyProperty;

        // 构建 Jquery Dom 并返回
        const div = $("<div>" + propValue + "<div>")

        div.css("color", "Red"); // 字体颜色设置为红色

        return div;
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

1. 第一行和第二行声明了活字格接口 ".d.ts" 文件的位置，以便在编写JavaScript代码时一个提供代码补全，提高开发效率。
    ![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80957814/image2023-1-18_9-36-40.png)
2. 第三行定义了 MyPluginCellType 类型，必须从 Forguncy.Plugin.CellTypeBase 派生
3. 第4行到第15行重写了 createContent 方法，通过Jquery创建了一个 DIV 并返回。最后，活字格会使用 createContent 的返回值渲染这个单元格。单元格主要的渲染逻辑都会写到这里。后续的教程中，主要是修改这个函数的实现来达成各种效果
4. 第16行注册这个写的单元格给活字格，这样活字格才知道有一个新的单元格插件加入了。registerCellType方法的第一个参数格式： 【单元格名字空间】.【单元格名称】,【空格】【应用程序集名称】

好，我们已经了解了单元格插件的代码结构，让我们做一些小的修改来简单尝试一下开发一个单元格插件吧。

比如，我们希望开发一个按钮插件。我们把 MyPluginCellType.cs 修改如下：

```auto
    public class MyPluginCellType : CellType
    {
        [DisplayName("单击命令")]
        [CustomCommandObject]
        public object ClickCommand { get; set; }

        [DisplayName("右击命令")]
        [CustomCommandObject]
        public object RightClickCommand { get; set; }

        [DisplayName("按钮文本")]
        public string ButtonText { get; set; } = "默认文本";

        [DisplayName("透明度")]
        [Description("透明度取值范围，从0到1,0.5表示半透明，0表示完全透明")]
        [DoubleProperty(Max = 1, Min = 0)]
        public double Opacity { get; set; } = 1;

        public override string ToString()
        {
            return "我的按钮";
        }
    }
```

<span class="ne-text">MyPluginCellType.js 代码修改如下：</span>

```auto
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    content = null;
    createContent() {
        this.content = $("<button style='width:100%;height:100%;'></button>");
        const cellType = this.CellElement.CellType;
        this.content.click(() => {
            this.executeCustomCommandObject(cellType.ClickCommand);
        })
        this.content.contextmenu(() => {
            this.executeCustomCommandObject(cellType.RightClickCommand);
            return false;
        })
        this.content.css("opacity", cellType.Opacity);
        this.content.text(cellType.ButtonText);
        return this.content;
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```


修改之后，编译代码，重启设计器。
在设计器中找到 “我的按钮”单元格插件，添加到页面上。我们可以看见在单元格设置面板中多了4个设置，正好和C#代码中的4个属性对应。![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80957814/image2023-1-18_9-37-2.png)

单击绿色开始按钮之后，在浏览器中就看到了我们新编写的按钮插件。
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80957814/image2023-1-18_9-37-20.png)

通过设置不同的值，我们可以让单元格在点击右键或单击左键执行不同的命令。可以定制按钮的文本，可以修改按钮的透明度。是不是很酷呢？
也许你还不理解这些代码的意思，没关系，后续的教程中对这些代码都会有详细的解释。