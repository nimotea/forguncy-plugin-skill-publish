# DesignTime Support

## Supportcommanddesigntime

# 命令设计时支持

## Content

*   [自定义命令编辑器](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/customcommandeditor)
*   [属性校验](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/attributeverification)
*   [动态 隐藏属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/dynamichiddenproperties)
*   [命令的分组与排序](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/commandgroupingandsorting)
*   [给命令属性添加说明](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/adddescriptionstocommandproperties)
*   [给命令添加说明](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/adddescriptiontocommand)

---

## Setcommandvisibilityrange

# 设置命令可见范围

## Content

有些命令只应该在PC页面使用，有些只应该在手机页面上使用，通过CommandSupportUsingScope可以控制命令的可见范围。

```
    [CommandSupportUsingScope(CommandPageScope.AllPCPage)]
    public class MyPluginCommand : Command
    {
    }
```

  

CommandPageScope 值

| NormalPCPage | 普通PC页面 |
| --- | --- |
| NormalMobilePage | 普通手机页面 |
| MasterPCPage | PC 母版页 |
| MasterMobilePage | 手机母版页 |
| TemplatePCPage | PC页图文列表模板 |
| TemplateMobilePage | 手机页图文列表模板 |
| UserControlPage | 组件  |
| AllPCPage | 所有PC页 |
| AllMobilePage | 所有手机页 |
| AllNormalPage | 所有普通页 |
| AllMasterPage | 所有母版页 |
| AllTemplatePage | 所有图文列表模板 |
| AllPage | 所有页面（默认值） |