---
type: reference
module: ServerCommand
concepts: [Properties, Boolean, Decimal, Enum, Formula, Integer, Percentage, String, DisplayName, Category]
version: 8.0+
---

# 服务端命令基础属性指南

本文档详细介绍了活字格服务端命令插件开发中常用的基础属性类型及其配置方法。

## 0. 通用特性 (Common Attributes)

在定义任何属性时，建议使用 `[DisplayName]` 和 `[Category]` 特性来优化设计器中的显示效果。

*   **DisplayName**: 设置属性在设计器面板中显示的名称（支持中文）。
*   **Category**: 设置属性的分组名称，便于分类管理。

```csharp
using System.ComponentModel; // 必须引用
using GrapeCity.Forguncy.Plugin;

public class MyPluginServerCommand : Command
{
    [Category("参数设置")]
    [DisplayName("连接字符串")]
    public string ConnectionString { get; set; }
}
```

> [UI]: 属性面板将显示 "参数设置" 分组下的 "连接字符串"。

---

## 1. 布尔属性 (BooleanProperty)

`bool` 类型的属性自动识别为复选框。

```csharp
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;
using System.ComponentModel;
using System.Threading.Tasks;

public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("启用日志")]
    public bool EnableLog { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        return new ExecuteResult();
    }

    public override CommandScope GetCommandScope()
    {
        return CommandScope.ExecutableInServer;
    }
}
```

> [UI]: 设计器中显示为一个名为 "启用日志" 的复选框。

### 进阶控制
使用 `[BoolProperty]` 控制缩进级别。

```csharp
[DisplayName("启用高级模式")]
[BoolProperty(IndentLevel = 0)]
public bool AdvancedMode { get; set; }

[DisplayName("子选项 A")]
[BoolProperty(IndentLevel = 1)]
public bool SubOptionA { get; set; }
```

> [UI]: "子选项 A" 会比 "启用高级模式" 向右缩进一级。

> **注意**：如果默认值为 `true`，必须添加 `[DefaultValue(true)]`。

---

## 2. 小数属性 (DecimalProperty)

`double` 类型的属性自动识别为小数输入框。

```csharp
[DisplayName("税率")]
public double TaxRate { get; set; }
```

> [UI]: 设计器中显示为数字输入框。

### 进阶控制 (`DoublePropertyAttribute`)
*   **限制范围**：`Min` 和 `Max`。
*   **允许空值**：`AllowNull = true` (属性类型需为 `double?`)。

```csharp
[DoubleProperty(Min = 0, Max = 1)]
[DisplayName("折扣系数 (0-1)")]
public double DiscountFactor { get; set; }

[DoubleProperty(AllowNull = true, Watermark = "默认")]
[DisplayName("阈值")]
public double? Threshold { get; set; }
```

---

## 3. 整数属性 (IntegerProperty)

`int` 类型的属性自动识别为整数输入框。

```csharp
[DisplayName("重试次数")]
public int RetryCount { get; set; }
```

> [UI]: 设计器中显示为整数输入框。

### 进阶控制 (`IntPropertyAttribute`)
*   **限制范围**：`Min` 和 `Max`。
*   **允许空值**：`AllowNull = true` (属性类型需为 `int?`)。

```csharp
[IntProperty(Min = 1, Max = 10)]
[DisplayName("线程数")]
public int ThreadCount { get; set; }

[IntProperty(AllowNull = true, Watermark = "无限制")]
[DisplayName("超时时间 (ms)")]
public int? Timeout { get; set; }
```

---

## 4. 枚举属性 (EnumProperty)

枚举类型自动显示为下拉列表。

```csharp
public enum UserType
{
    [Description("学生")]
    Student,
    [Description("教师")]
    Teacher,
    [Description("工人")]
    Worker
}

public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("用户身份")]
    public UserType UserRole { get; set; }
    // ... ExecuteAsync ...
}
```

> [UI]: 设计器中显示包含 "学生"、"教师"、"工人" 的下拉列表。

---

## 5. 字符串属性 (StringProperty)

`string` 类型自动识别为文本输入框。

```csharp
[DisplayName("用户名")]
public string UserName { get; set; }
```

> [UI]: 设计器中显示为文本输入框。

### 进阶控制 (`TextPropertyAttribute`)
*   **水印**：`Watermark`。
*   **多行文本**：`AcceptsReturn = true`。
*   **多语言支持**：`CanSelectResource = true` (v10.0+)。

```csharp
[TextProperty(Watermark = "请输入...", AcceptsReturn = true, CanSelectResource = true)]
[DisplayName("备注")]
public string Remarks { get; set; }
```

### 服务端获取多语言资源
在 `ExecuteAsync` 中使用 `GetApplicationResource` 方法。

```csharp
public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
{
    // 自动根据当前语言环境获取对应字符串
    var strValue = GetApplicationResource(Remarks);
    return new ExecuteResult { Message = strValue };
}
```

---

## 6. 公式属性 (FormulaProperty)

属性类型必须为 `object`。

```csharp
[FormulaProperty]
[DisplayName("计算公式")]
public object CalculationFormula { get; set; }
```

> [UI]: 设计器中显示为带有公式选择按钮的输入框。

### 服务端计算公式
在 `ExecuteAsync` 中使用 `dataContext.EvaluateFormulaAsync`。

```csharp
public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
{
    // 计算公式值
    var result = await dataContext.EvaluateFormulaAsync(this.CalculationFormula);
    return new ExecuteResult { Message = result?.ToString() };
}
```

### 进阶配置
*   **备选列表**：`RecommendedValues = "A|B|C"`。
*   **多行输入**：`AcceptsReturn = true`。
*   **禁用多语言**：`CanSelectResource = false`。

---

## 7. 百分比属性 (PercentageProperty) (v9.0+)

用于输入百分比，底层存储为 `double` (0-1)。

```csharp
[PercentageProperty]
[DisplayName("完成度")]
public double CompletionRate { get; set; }
```
