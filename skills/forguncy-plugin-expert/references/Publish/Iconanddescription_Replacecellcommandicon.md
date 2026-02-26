> Source: replacecellcommandicon.md (Imported from external documentation)

# 更换单元格/命令图标

## Content

单元格和命令可以指定图标。
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958782/image2023-1-19_15-52-3.png)

可以通过替换 Icon.png 文件来更新图标。
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958782/image2023-1-19_15-52-16.png)

如果一个插件包中存在多个命令或单元格，并且希望每个单元格，命令使用不同的图标。可以在 Resources目录下创建多个图片文件。在新的图标文件上右击，选择“属性”。
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958782/image2023-1-19_15-52-34.png)

在弹出的属性面板中找到生成操作选项，包值修改为资源。
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958782/image2023-1-19_15-52-49.png)

之后修改源代码中 IconAttribute 的值，指定新的图标名。
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958782/image2023-1-19_15-53-0.png)

重新编译项目，图标就更新了。
推荐图标大小为 16\*16 像素，96 DPI。