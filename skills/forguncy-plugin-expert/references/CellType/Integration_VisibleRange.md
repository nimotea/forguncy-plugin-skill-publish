# 和活字格原生功能集成 - 设置单元格可见范围 (Visible Range)

## 参考资料
[设置单元格可见范围 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/setthevisiblerangeofcells)

## 概述
通过 `[SupportUsingScope]` 特性控制单元格插件在哪些类型的页面中可用（例如仅 PC 或仅移动端）。

## 基础用法
在插件类上添加特性。

```csharp
[SupportUsingScope(PageScope.AllPCPage, ListViewScope.None)]
public class MyPluginCellType : CellType
{
}
```

## 参数说明

### PageScope (页面范围)
| 值 | 说明 |
| :--- | :--- |
| `AllPage` | 所有页面 (默认) |
| `AllPCPage` | 所有 PC 页 |
| `AllMobilePage` | 所有手机页 |
| `NormalPCPage` | 普通 PC 页面 |
| `NormalMobilePage` | 普通手机页面 |
| `MasterPCPage` | PC 母版页 |
| `UserControlPage` | 组件 |
| ... | ... |

### ListViewScope (表格范围)
目前插件单元格不支持直接在表格（ListView）中使用，**必须传 `ListViewScope.None`**。
