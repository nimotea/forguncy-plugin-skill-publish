# 添加属性 - 百分比属性 (Percentage Property)

在服务端命令插件开发中，百分比属性用于让用户以百分比形式（如 50%）输入数值，而后台实际接收为小数（如 0.5）。
*(此特性为活字格 V9 新增功能)*

## 1. 基础用法
使用 `[PercentageProperty]` 特性标记属性。
> **注意**：
> 1. 属性类型必须是 `double`。
> 2. 设计器中显示为百分数，代码中获取到的是小数。

### 代码示例
```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("完成度")]
    [PercentageProperty]
    public double CompletionRate { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        // 假设用户输入 50%，这里 CompletionRate 的值为 0.5
        var rate = this.CompletionRate;
        
        return new ExecuteResult()
        {
            Message = $"当前进度: {rate * 100}%"
        };
    }
}
```

## 2. 常见问题
- **Q: 为什么我输入 100，代码里变成了 100？**
  A: 如果没有加 `[PercentageProperty]`，输入 100 就是 100。加上该特性后，设计器会自动处理 `%` 符号，输入 `50%` 实际存储为 `0.5`。
- **Q: 支持负百分比吗？**
  A: 支持。
