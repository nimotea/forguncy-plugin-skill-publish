# 命令的分组与排序 (Grouping & Sorting)

在活字格设计器中，为了更好地组织和管理自定义命令，可以通过特性（Attribute）来指定命令的分组（Category）以及在分组内的排序权重（OrderWeight）。

## 1. 命令分组 (Category)

默认情况下，自定义插件命令会被归类到“其他”分组中。使用 `[Category]` 特性可以将其移动到指定分组。

### 自定义分组

如果指定的分组不存在，设计器会自动创建一个新的分组。

```csharp
using System.ComponentModel; // 引用 Category 特性

[Category("我的插件工具包")]
public class MyPluginCommand : Command
{
    // ...
}
```

### 归入现有分组

如果指定的分组名称与活字格内置的分组名称一致（如“数据”、“页面”、“逻辑”等），插件命令会被归入该现有分组中。

```csharp
[Category("数据")]
public class MyDataCommand : Command
{
    // ...
}
```

## 2. 命令排序 (OrderWeight)

当同一个分组下有多个命令时，可以使用 `[OrderWeight]` 特性来控制它们的显示顺序。

- **特性类**：`[OrderWeight(int)]`
- **规则**：数字越小，排列越靠前（通常从 1 开始）。
- **注意**：如果不指定，排序可能不确定或按字母顺序。

### 代码示例

```csharp
using GrapeCity.Forguncy.Commands;
using System.ComponentModel;

namespace MyPlugin
{
    [OrderWeight(1)]
    [Category("我的工具箱")]
    public class ToolCommand1 : Command
    {
        // ...
    }

    [OrderWeight(2)]
    [Category("我的工具箱")]
    public class ToolCommand2 : Command
    {
        // ...
    }

    [OrderWeight(10)]
    [Category("我的工具箱")]
    public class AdvancedToolCommand : Command
    {
        // ...
    }
}
```

## 综合示例

```csharp
[Category("企业级扩展")]
[OrderWeight(5)]
[Description("这是一个用于处理企业级业务逻辑的高级命令")]
public class EnterpriseCommand : Command
{
    // ...
}
```
