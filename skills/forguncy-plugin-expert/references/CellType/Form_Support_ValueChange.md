# 开发表单类单元格 - 支持值变更命令 (Value Change Command)

## 参考资料
[支持值变更命令 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportvaluechangecommand)

## 概述
当单元格值发生变化时触发用户配置的命令（如“值变更时”命令）。

## 实现方法
让 C# 类实现 `ICommandCellType` 接口。

```csharp
public class MyPluginCellType : CellType, ICommandCellType
{
    [DisplayName("值变更命令")]
    public List<Command> CommandList { get; set; }

    // 指定命令触发时机为值变更时
    public CommandExcuteKind CommandExcuteKind => CommandExcuteKind.OnValueChanged;
}
```

## JS 处理
无需编写额外 JS 代码。只要在 JS 中调用了 `this.commitValue()`，活字格会自动检测值变更并执行命令。
