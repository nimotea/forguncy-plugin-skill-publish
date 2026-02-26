> Source: page-not-update.md (Imported from external documentation)

# 如何解决修改JavaScript文件后，刷新页面不更新的问题

## Content

## 问题描述

正常情况下，如果修改了插件中的 JavaScript/CSS 文件并保存后，只需要刷新浏览器（9.0.100.0 之后活字格版本支持热更新，只要保存，浏览器会自动刷新），就可以调试最新的代码。这个特性非常方便开发和调试插件，但是有时这个特性会失效。如果遇到自动更新失效时，可以尝试以下方法解决。

## 活字格插件自动刷新的原理

要排查自动更新失效的原因，首先需要了解活字格插件自动刷新的原理。
首先，活字格的插件会安装到 C:\\Users\\Public\\Documents 目录下，命名规则如 ForguncyPluginvXXX。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/image.d2b1b1.png?width=800)
XXX表示的活字格设计器的版本号，对应方式如下表。

| 文件夹名称 | 版本号模式 | 示例 |
| ----- | ----- | --- |
| ForguncyPluginv6 | 6.0.x.x | 6.0.0.0 / 6.0.1.0 |
| ForguncyPluginv6.1 | 6.0.10x.0 | 6.0.100.0 / 6.0.101.0 |
| ForguncyPluginv7 | 6.0.x.x | 7.0.0.0 / 7.0.1.0 |
| ForguncyPluginv7.1 | 6.0.10x.0 | 7.0.100.0 / 7.0.101.0 |
| ForguncyPluginvY | Y.0.x.x | 10.0.0.0 / 10.0.1.0 |
| ForguncyPluginvY.1 | Y.0.10x.x | 10.0.100.0 / 10.0.101.0 |

根据当前调试的活字格设计器版本号，可以找到对应的文件夹。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/image.549d4d.png?width=800)
找到对应的文件夹后，会找到当前设计器已经安装的插件，每个插件对应一个文件夹。根据文件夹名称可以大体判断出对应的插件。如果自己开发了插件，编译后，插件构建工具会自动创建/更新插件对应的文件夹中的内容。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/image.76b22c.png?width=800)
编译后，可以看到C:\\Users\\Public\\Documents\\ForguncyPluginv9目录下增加了 MyPlugin 文件夹。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/image.0dc00a.png?width=800)
在 MyPlugin 文件中，如果是通过编译源代码自动安装的插件，会找到一个名为 SourceCodePath 的文件。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/image.b0748e.png?width=800)
使用记事本打开 SourceCodePath 文件可以看到以下内容。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/image.153427.png?width=800)
看到这里相信大家已经明白了活字格前端代码更新的原理。当活字格加载插件的JavaScript/CSS 代码的时候，活字格会首先尝试查看插件的根目录下是否存在 SourceCodePath 文件，如果存在，则读取 SourceCodePath 内容，并尝试到 SourceCodePath 内容对应的路径下查找 JavaScript/CSS 文件进行加载。这样修改源文件中的代码就可以被活字感知并重新加载新的JavaScript文件了。

## 如何解决自动刷新失效的问题

如果自动刷新失效了，可以按以下方法进行排查：

1. 找到对应的插件文件夹，查看 SourceCodePath 文件是否存在，如果不存在，可以手工创建一个 SourceCodePath 文件，并把文件内容设置为插件源代码的根目录。
2. 如果 SourceCodePath 存在，用记事本打开 SourceCodePath 文件，查看 SourceCodePath 内容对应的路径是否正确，如果不正确（可能是源代码的位置变了），更新为正确的位置即可。
3. 如果 SourceCodePath 存在，内容指定的文件夹位置也正确，可以查看 C:\\Users\\Public\\Documents\\ForguncyPluginv9 目录下是否有相同的插件被多次安装。活字格加载插件时基于 PluginConfig.json 里的GUID来识别插件，如果多个文件里有 PluginConfig.json 中配置了相同的 GUID，会导致设计器随机加载了其中一个。插件可以通过打开 Fgcc 文件安装、通过编译自动安装，或通过葡萄城市场安装等，如下图。 此时，清理掉多余的插件，再重新编译即可。
    ![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/image.23745c.png?width=800)
4. 如果以上方法都不能解决，还可能是浏览器缓存问题。可以在浏览器中按 F12 打开开发者工具，并使用 Ctrl + F5 刷新浏览器，强制无效化缓存。
    ![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/image.f3be39.png?width=800)