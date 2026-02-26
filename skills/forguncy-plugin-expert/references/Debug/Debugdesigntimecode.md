> Source: debugdesigntimecode.md (Imported from external documentation)

# 调试设计时代码

## Content

如果需要调试设计器中的功能，如自定义编辑器，设计时预览等。可以通过VisualStudio的附加到进程功能。
方法如下：

1. 启动活字格设计器。
2. 用VisualStudio打开插件工程。
3. 在VisualStudio中找到附加到进程选项。
    ![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958762/image2023-1-19_15-30-13.png)
4. 在弹出窗口中找到Forguncy.exe进程，单击“附加”。
    ![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958762/image2023-1-19_15-30-27.png)
5. 附加完成后，在源代码中需要调试的部分添加断点。在设计器中做需要调试的操作。当逻辑执行到断点所在代码时，程序会停下。可以单步调试，也可以通过监视窗口查看程序上下文状态。
    ![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958762/image2023-1-19_15-30-40.png)

>type=warning
> 如果需要修改代码，需要重新编译项目。
>
> 1. 如果是调试设计器自带的 ForguncyServerConsole.exe 需要重启设计器；
> 2. 如果是调试发布之后的网站，需要重新发布。