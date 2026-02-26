> Source: pluginconfigjson.md (Imported from external documentation)

# PluginConfig.json

## Content

PluginConfig 包含了插件的配置信息。
通过插件生成工具生成的默认配置如下：

```
{
  "assembly": [
    "MyPlugin.dll"
  ],
  "css": [],
  "javascript": [
    "Resources/MyPluginCellType.js",
    "Resources/MyPluginCommand.js"
  ],
  "serverApiAssembly": [],
  "image": "Resources/PluginLogo.png",
  "description": "这是一个活字格插件",
  "name": "我的插件",
  "pluginType": "cellType,command",
  "guid": "424ccd9c-7dc8-4dc5-a0fe-0c5dfad0b45f",
  "version": "1.0.0.0",
  "dependenceVersion": "8.0.104.0",
  "bundleJavaScript": true,
  "bundleCSS": true
}
```

属性说明如下：
**assembly**
插件的主程序集名称。
示例

```
  "assembly": [
    "MyPlugin.dll"
  ]
```

**css**
需要默认加载的 css 文件。
示例

```
  "css": [
    "Resources/MyPluginCellType.css",
    "Resources/MyPluginCommand.css"
  ]
```

**javascript**
需要默认加载的 javascript 文件
示例

```
  "javascript": [
    "Resources/MyPluginCellType.js",
    "Resources/MyPluginCommand.js"
  ],
```

**serverApiAssembly**
活字格服务器需要加载的程序集
示例

```
  "serverApiAssembly": [
    "MyPlugin.Server.dll"
  ],
```

**image**
插件包图标，[查看详细](/solutions/huozige/help/docs/plugindevelopment/publish/iconanddescription/changepluginpackageicon)
示例

```
"image": "Resources/PluginLogo.png",
```

**description**
插件包描述文本，[查看详细](/solutions/huozige/help/docs/plugindevelopment/publish/iconanddescription/updatepluginnameanddescription)
示例

```
"description": "这是一个活字格插件",
```

**name**
插件显示名称，[查看详细](/solutions/huozige/help/docs/plugindevelopment/publish/iconanddescription/updatepluginnameanddescription)
示例

```
"name": "我的插件",
```

**pluginType**
声明插件包内容，可选值 "cellType","command","cellType,command"
cellType 表示单元格插件，command 表示命令或服务端命令插件。
示例

```
"pluginType": "cellType,command",
```

**guid**
插件唯一标识，活字格通过这个Guid 区分不同的插件。安装插件时，如果相同guid的插件已经存在会覆盖已经存在的插件。
示例

```
"guid": "424ccd9c-7dc8-4dc5-a0fe-0c5dfad0b45f",
```

可以使用VisualStudio 的“工具->创建 GUID”来生成新的GUID。如果是通过插件生成工具创建的插件，默认会生成一个新的GUID。![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958789/image2023-1-19_15-57-39.png)

**version**
插件的版本号，由四个整数组成，格式为 [主版本号].[子版本号].[修正版本号].[编译版本号]
如果插件升级，新版本的版本号应该高于之前版本的版本号。
示例

```
"version": "1.0.0.0",
```

**dependenceVersion**
依赖活字格的版本号，通常插件会依赖特定版本的活字格接口。如果插件依赖活字格的版本号高于客户安装的活字格版本，则插件不能被安装。
示例

```
"dependenceVersion": "8.0.104.0",
```

**bundleJavaScript**
发布活字格应用后是否对JavaScript属性中声明的 JavaScript 文件进行压缩打包。
示例

```
"bundleJavaScript": true,
```

**bundleCSS**
发布活字格应用后是否对css属性中声明的 css 文件进行压缩打包。
示例

```
"bundleCSS": true
```