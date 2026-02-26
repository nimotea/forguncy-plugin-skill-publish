# 单元格设计时支持 - 自定义行为与校验 (Behavior & Validation)

## 1. 重新定义双击行为
[重新定义单元格双击行为 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/redefinecelldoubleclickbehavior)

默认情况下，双击单元格会进入文本编辑模式。对于不绑定值的单元格（如按钮、图表），可以将其改为弹出特定属性的编辑对话框。

让 Designer 实现 `IDefaultEditAction` 接口。

```csharp
public class MyPluginCellTypeDesigner : CellTypeDesigner<MyPluginCellType>, IDefaultEditAction
{
    public void OnStartEditStarting(IBuilderContext builderContext, StartEditingEventArgs args)
    {
        // 指定默认编辑的属性名（必须是列表、命令等弹出式属性）
        args.DefaultActionPropertyName = nameof(MyPluginCellType.MyListProperty);
        // 取消默认的文本编辑
        args.CancelEdit = true;
    }
}
```

## 2. 自定义校验
[自定义校验 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/Custom-verification)

实现复杂的属性校验逻辑（如属性 A + B 必须 < 100）。
让 Designer 实现 `ICellTypeChecker` 接口。

```csharp
public class MyPluginCellTypeDesigner : CellTypeDesigner<MyPluginCellType>, ICellTypeChecker
{
    public IEnumerable<ForguncyErrorInfo> CheckCellTypeErrors(IBuilderContext context)
    {
        if (this.CellType.Prop1 + this.CellType.Prop2 > 100)
        {
            yield return new ForguncyErrorInfo()
            {
                ErrorType = ForguncyErrorType.Error, // 或 Warning
                Message = "属性1与属性2之和不能超过100"
            };
        }
    }
}
```

## 3. 属性说明与显示名
- **[DisplayName]**: 修改属性在面板中的显示名称。
- **[Description]**: 添加鼠标悬停提示说明。

```csharp
[DisplayName("最大值")]
[Description("设置允许输入的最大数值，超过此值将报错。")]
public int MaxValue { get; set; }
```
