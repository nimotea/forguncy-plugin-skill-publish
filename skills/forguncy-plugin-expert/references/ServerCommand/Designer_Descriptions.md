# 给命令和属性添加说明 (Descriptions)

在活字格设计器中，为了帮助用户更好地理解插件命令和属性的用途，可以使用 `[Description]` 特性为它们添加说明文本。

## 1. 给命令属性添加说明

当属性名无法完全表达其功能或用法时，通过添加描述来提供详细说明。描述文本会在用户将鼠标悬停在属性旁的问号图标上时显示。

### 代码示例

```csharp
using System.ComponentModel; // 必须引用

public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    // 单行描述
    [Description("这里可以写一些描述")]
    public string MyProperty1 { get; set; }

    // 多行描述，使用 \r\n 换行
    [FormulaProperty]
    [Description("描述文本可以是多行的\r\n通过鼠标悬停到问号图标上查看")]
    public object MyProperty2 { get; set; }

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

## 2. 给命令添加说明

为整个命令添加描述，通常用于解释命令的整体功能、使用场景或特殊策略。命令的描述会出现在属性列表的最下方。

### 代码示例

```csharp
using System.ComponentModel; // 必须引用

// 描述文本可以是多行的，如果文本过长会自动换行
[Description("这是一个示例插件命令。\r\n它用于演示如何添加命令级别的详细说明文档。")]
public class MyPluginCommand : Command
{
    public string MyProperty1 { get; set; }
    
    [FormulaProperty]
    public object MyProperty2 { get; set; }
}
```

## 最佳实践

1. **简洁明了**：描述应直击要点，避免过于冗长。
2. **多行格式**：对于复杂的参数说明，使用 `\r\n` 进行分行，提高可读性。
3. **特殊策略**：如果属性有默认行为或特殊限制（如“为空时表示无限”），务必在描述中说明。
4. **数据结构示例**：对于接收 JSON 或复杂对象的属性，**必须**在 `[Description]` 中包含示例数据结构。这能极大降低用户的理解成本。

### 复杂对象示例
```csharp
[DisplayName("数据序列")]
[FormulaProperty]
[Description("请输入包含数值的 JSON 数组，例如：\r\n[{\"depth\": 100, \"val\": 1}, {\"depth\": 200, \"val\": 2.5}]")]
public object DataSeries { get; set; }
```
