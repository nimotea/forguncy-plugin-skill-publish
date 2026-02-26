> Source: upgradepluginV81toV9.md (Imported from external documentation)

# 活字格V8.1插件升级至V9

## Content

1. [从.NET](http://xn--0mq.net/ "http://从.NET") 官网上下载 .NET 5.0 SDK，并安装，安装这个版本的SDK就是专门用来执行下面的 try-convert 工具的。 [Download .NET 5.0 (Linux, macOS, and Windows) (microsoft.com)](https://dotnet.microsoft.com/en-us/download/dotnet/5.0 "https://dotnet.microsoft.com/en-us/download/dotnet/5.0")
<br>
    ![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80960509/image2023-2-28_15-22-41.png)
2. 命令窗口执行如下命令安装官方转换工具 try-convert。
<br>
    `**dotnet tool install -g try-convert**   `
<br>
    ![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80960509/image2023-2-28_15-23-6.png)
3. 在插件目录下面执行如下命令。（以8.1版本的menu插件举例）
<br>
    **`try-convert`**
<br>
    ![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80960509/image2023-2-28_15-24-28.png)
4. [安装.NET](http://xn--49sq66h.net/ "http://安装.NET") 6 SDK，如果已经安装了Visual Studio 2022 的话可以不装。[Download .NET (Linux, macOS, and Windows) (microsoft.com)](https://dotnet.microsoft.com/en-us/download "https://dotnet.microsoft.com/en-us/download")
<br>
    ![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80960509/image2023-2-28_15-24-43.png)
5. 双击 sln 文件打开当前插件的工程，双击工程，此时会进入直接编辑的界面。此时我们还需要对当前插件做一些调整，使其能够编译通过。![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80960509/image2023-2-28_15-24-58.png)
6. 修改 TargetFramework 的版本为 net6.0-windows。
    ![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80960509/image2023-2-28_15-25-13.png)
7. 确保这三句话都在。插件有时候会有WPF相关的逻辑（比如设计时预览、Icon等），这里加上这三句话确保设计器里插件工作正常。

    ```auto
    <UseWindowsForms>true</UseWindowsForms>
    <UseWPF>true</UseWPF>
    <ImportWindowsDesktopTargets>true</ImportWindowsDesktopTargets>
    ```

    `![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80960509/image2023-2-28_15-25-31.png)   `
8. 加上如下几个设置，分别用来控制生成的产物的位置、产物的内容等。

    ```auto
    <AppendTargetFrameworkToOutputPath>false</AppendTargetFrameworkToOutputPath>
    <CopyLocalLockFileAssemblies>true</CopyLocalLockFileAssemblies>
    <EnableDefaultEmbeddedResourceItems>false</EnableDefaultEmbeddedResourceItems>
    ```

    ![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80960509/image2023-2-28_15-26-47.png)
9. 删除 Tools 目录下旧的打包工具，然后使用新的打包工具[`PluginPackageTool.zip`](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/attachments/8d57f04a-783b-413e-8161-f10dc365c3ac/PluginPackageTool.d0e9af.zip)，将这个压缩包解压到 Tools 目录下。![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80960509/image2023-2-28_15-26-59.png)
10. 使用新的格式编译时执行打包工具。新的格式：

```auto
<Target Name="PostBuild" AfterTargets="PostBuildEvent">
	<Exec Command="&quot;$(MSBuildProjectDirectory)\Tools\PluginPackageTool.exe&quot; &quot;$(MSBuildProjectDirectory)\\&quot; $(ConfigurationName)" />
</Target>
```

![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80960509/image2023-2-28_15-27-15.png)
替换成：
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80960509/image2023-2-28_15-27-57.png)