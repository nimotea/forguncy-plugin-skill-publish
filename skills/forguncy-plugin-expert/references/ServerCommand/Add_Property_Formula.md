# 添加属性 - 公式属性 (Formula Property)

当属性值需要依赖公式的计算结果动态变化时（例如引用单元格值 `=A1` 或使用函数 `=IF(...)`），必须使用公式属性。

## 1. 基础用法
要创建一个公式属性，必须满足以下两个条件：
1.  属性类型必须为 `object`。
2.  属性必须标注 `[FormulaProperty]` 特性。

在运行时，必须通过 `context.EvaluateFormulaAsync()` 方法来计算公式的最终值。

### 代码示例
```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("动态参数")]
    [FormulaProperty]
    public object DynamicParam { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        // 计算公式的值
        var calculatedValue = await dataContext.EvaluateFormulaAsync(this.DynamicParam);
        
        return new ExecuteResult() 
        { 
            Message = calculatedValue?.ToString() 
        };
    }
}
```

---

## 2. 高级配置
`FormulaPropertyAttribute` 提供了一些参数来控制设计器中的行为。

### 2.1 提供备选列表 (RecommendedValues)
设置 `RecommendedValues` 属性可以为用户提供下拉选择项。多个选项使用竖线 `|` 分隔。

```csharp
[DisplayName("用户类型")]
[FormulaProperty(RecommendedValues = "学生|教师|工人")]
public object UserType { get; set; }
```
> **注意**：即使用户选择了备选项，该属性本质上仍然是公式属性，运行时依然需要使用 `EvaluateFormulaAsync` 解析。

### 2.2 支持多行文本 (AcceptsReturn)
设置 `AcceptsReturn = true` 可以让输入框支持回车换行。

```csharp
[DisplayName("SQL查询语句")]
[FormulaProperty(AcceptsReturn = true)]
public object SqlQuery { get; set; }
```

### 2.3 控制多语言支持 (CanSelectResource)
公式属性默认开启多语言支持（允许选择资源）。如果不需要，可以通过 `CanSelectResource = false` 关闭。

```csharp
[DisplayName("内部标识")]
[FormulaProperty(CanSelectResource = false)]
public object InternalId { get; set; }
```
*(此特性为 10.0.0.0 新增)*

---

## 3. 最佳实践
- **类型安全**：虽然属性类型是 `object`，但 `EvaluateFormulaAsync` 返回的结果通常是基础类型（int, string, double, bool）。建议在获取结果后进行类型检查或转换。
- **变量引用**：公式属性是插件引用活字格上下文变量（如页面单元格值）的标准方式。不要尝试自己解析变量名，始终通过公式属性交给引擎处理。
