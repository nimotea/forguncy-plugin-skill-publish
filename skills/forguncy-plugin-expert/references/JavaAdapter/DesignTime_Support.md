# DesignTime Support

## CommandDesignTimeSupport

# 命令设计时支持

## Content

* [属性校验](/solutions/huozige/help/docs/java-adapter/java-server-command/command-design-time-support/property-verification)
* [高级自定义校验](/solutions/huozige/help/docs/java-adapter/java-server-command/command-design-time-support/advanced-custom-validation)
* [动态隐藏属性](/solutions/huozige/help/docs/java-adapter/java-server-command/command-design-time-support/visible)
* [命令的分组与排序](/solutions/huozige/help/docs/java-adapter/java-server-command/command-design-time-support/command-group-filter)
* [给命令属性添加说明](/solutions/huozige/help/docs/java-adapter/java-server-command/command-design-time-support/add-description-to-attribute)
* [给命令添加说明](/solutions/huozige/help/docs/java-adapter/java-server-command/command-design-time-support/add-description-to-command)
* [属性值联动](/solutions/huozige/help/docs/java-adapter/java-server-command/command-design-time-support/property-value-linkage)
* [折叠高级属性](/solutions/huozige/help/docs/java-adapter/java-server-command/command-design-time-support/fold-advanced-attributes)
* [插件升级](/solutions/huozige/help/docs/java-adapter/java-server-command/command-design-time-support/update)

---

## IconAndDescription

# 图标与描述

## Content

* [更换插件包图标](/solutions/huozige/help/docs/java-adapter/java-server-command/icon-and-description/change-plugin-package-icon)
* [更换命令图标](/solutions/huozige/help/docs/java-adapter/java-server-command/icon-and-description/change-command-icon)
* [更新插件名称与描述](/solutions/huozige/help/docs/java-adapter/java-server-command/icon-and-description/update-plugin-name-and-description)

---

## ChangeCommandIcon

# 更换命令图标

## Content

命令可以指定图标。
 
可以通过替换 Icon.png 文件来更新图标。
如果一个插件包中存在多个命令，并且希望每个命令使用不同的图标。可以在 resources目录下创建多个图片文件。
之后修改源代码中 @Icon 的值，指定新的图标名。

---

## ChangePluginPackageIcon

# 更换插件包图标

## Content

插件安装后，会在插件管理中显示。

可以通过替换 PluginLogo.png 图片来更新插件包图标。

插件图标建议大小为 100 \* 100 像素。