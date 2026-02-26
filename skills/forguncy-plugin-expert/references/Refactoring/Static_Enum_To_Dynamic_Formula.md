# Refactoring Guide: Static Enum to Dynamic Formula Property

本文档旨在指导开发者将现有的静态 `Enum` 属性重构为支持公式和变量的动态 `object` 属性。这种重构通常用于提升插件的灵活性，允许用户在运行时动态决定参数值。

## 重构 Checklist

- [ ] **类型变更**: 将属性类型从 `Enum` (或 `int`/`string`) 修改为 `object`。
- [ ] **Attribute 添加**: 添加 `[FormulaProperty]` 特性。
- [ ] **设计器兼容**: 如果需要保留下拉选择体验，添加 `[RecommendedValues]` (可选)。
- [ ] **解析逻辑**: 在 `ExecuteAsync` 中使用 `EvaluateFormulaAsync` 解析值。
- [ ] **校验逻辑**: 添加代码校验解析后的值是否在合法范围内（原 Enum 的值域）。
- [ ] **默认值/回退**: 处理解析失败或空值的情况。

## 详细步骤

### 1. 修改属性定义

**Before (Static Enum):**
```csharp
public enum RequestType
{
    Get,
    Post,
    Put
}

[DisplayName("请求类型")]
public RequestType Method { get; set; }
```

**After (Dynamic Formula):**
```csharp
[DisplayName("请求类型")]
[FormulaProperty] // 1. 标记为公式属性
public object Method { get; set; } // 2. 类型改为 object
```

### 2. (可选) 保留设计器下拉体验

如果你希望在设计器中仍然提供下拉选项，同时允许输入公式，可以使用 `ComboProperty` 或 `RecommendedValues` (视具体 SDK 版本支持情况而定，通常 `FormulaProperty` 会让设计器变为公式输入框，如果需要下拉提示，建议在描述中说明或使用自定义设计器)。

*注意：标准的 `[FormulaProperty]` 会将控件变为公式编辑框，用户可以直接输入常量字符串 "Get" 或公式 "=A1"。*

### 3. 重写解析逻辑 (ExecuteAsync)

**Before:**
```csharp
public override async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext context)
{
    // 直接使用 Enum
    if (this.Method == RequestType.Post) 
    {
        // ...
    }
}
```

**After:**
```csharp
public override async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext context)
{
    // 1. 解析公式
    var methodValue = await context.EvaluateFormulaAsync(this.Method);
    
    // 2. 转换为字符串并标准化 (处理大小写)
    string methodStr = methodValue?.ToString()?.Trim()?.ToUpperInvariant();

    // 3. 校验与映射
    if (string.IsNullOrEmpty(methodStr))
    {
        methodStr = "GET"; // 默认值
    }

    switch (methodStr)
    {
        case "GET":
        case "POST":
        case "PUT":
            // 合法值
            break;
        default:
            // 4. 错误处理
            return new ExecuteResult 
            { 
                Message = $"不支持的请求类型: {methodStr}. 请使用 GET, POST, 或 PUT." 
            };
    }

    // 业务逻辑...
}
```

### 4. 关键点总结

1.  **输入宽容性**: 用户可能输入 "Post", "post", 或 "POST"。转为动态属性后，务必进行 `ToUpper()` 或 `ToLower()` 标准化处理。
2.  **类型安全**: 原本由编译器保证的 Enum 类型安全现在需要手动校验。
3.  **文档提示**: 建议在 `[Description]` 中明确列出支持的字符串值，方便用户查阅。

```csharp
[DisplayName("请求类型")]
[Description("支持的值: GET, POST, PUT. 支持使用公式动态设置。")]
[FormulaProperty]
public object Method { get; set; }
```
