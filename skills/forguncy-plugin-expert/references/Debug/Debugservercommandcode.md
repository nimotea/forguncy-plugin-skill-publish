> Source: debugservercommandcode.md (Imported from external documentation)

# 调试服务端命令代码

## Content

如果要调试服务端命令或自定义中间件，可以使用VisualStudio的附加到进程功能。
方法如下：

1. 启动活字格设计器。
2. 用VisualStudio打开插件工程。
3. 在VisualStudio中找到附加到进程选项。
    ![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958767/image2023-1-19_15-49-50.png)
4. 在弹出窗口中找到ForguncyServerConsole.exe进程，单击附加。
    ![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958767/image2023-1-19_15-50-5.png)
5. 附加完成后，在源代码中需要调试的部分添加断点。通过设计器中的测试服务端命令功能，或者在网页中通过点击按钮“执行服务端命令”。当逻辑执行到断点所在代码时，程序会停下。可以单步调试，也可以通过监视窗口查看程序上下文状态。
    ![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958767/image2023-1-19_15-50-18.png)

如果需要修改代码，需要重新编译项目。

1. 如果是调试设计器自带的 ForguncyServerConsole.exe 需要重启设计器。
2. 如果是调试发布之后的网站，需要重新发布。