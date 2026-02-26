> Source: debugjavascriptcode.md (Imported from external documentation)

# 调试JavaScript代码

## Content

在开发过程中，需要反复调试，以确保代码逻辑正确。
调试JavaScript代码通常有两种办法：

### 输出日志

以下代码第六行，通过 console.log 方法可以打印调试信息到控制台。

```
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        // 获取MyProperty属性值，注意，这里的MyProperty应该与 MyPluginCellType.cs 文件定义的属性名一致
        const propValue = this.CellElement.CellType.MyProperty ?? "MyCell";

        console.log("属性值为：" + propValue);

        // 构建 Jquery Dom 并返回
        const div = $("<div>" + propValue + "<div>")
        div.css("color", "Red"); // 字体颜色设置为红色
        return div;
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

在浏览器中，按F12，打开开发者工具就可以在控制台中查看打印的调试信息。
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958757/image2023-1-19_15-20-9.png)

### 在浏览器开发者工具调试

通过按下 F12 打开浏览器的开发者工具。
选择“源代码”标签，在 Forguny/Plugins/MyPlugin/Resources 目录下可以找到插件的源代码，单击打开，在源代码中可以添加断点。
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958757/image2023-1-19_15-20-30.png)

刷新页面或与页面交互，当代码执行到断点处就会停下。此时可以通过控制台或者属性窗口获取更多调试信息。![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958757/image2023-1-19_15-20-44.png)

提示：
在调试过程中，如果发现问题需要修改JavaScript源代码，只需要在修改后保存，在浏览器中刷新页面即可应用最新的代码，无需重启设计器或重新安装插件。