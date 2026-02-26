# 添加属性 - 小数属性 (Double Property)

在服务端命令插件开发中，小数属性用于接收用户输入的浮点数值（double）。

## 1. 默认小数属性
默认情况下，如果属性类型是 `double`，活字格会自动识别为小数属性。

### 代码示例
```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("税率")]
    public double TaxRate { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        return new ExecuteResult();
    }
}
```

---

## 2. 高级配置 (DoublePropertyAttribute)
使用 `[DoubleProperty]` 特性可以自定义数值范围、可空性等。
> **注意**：标注 `DoublePropertyAttribute` 的属性类型必须是 `double` 或 `double?`。

### 2.1 控制数值范围 (Min/Max)
通过设置 `Min` 和 `Max` 属性来限制输入的数值范围。

```csharp
[DisplayName("折扣(0-1)")]
[DoubleProperty(Min = 0, Max = 1)]
public double Discount { get; set; }
```
如果不指定，范围为 `double` 类型的完整取值范围。

### 2.2 支持空值 (AllowNull)
默认的 `double` 类型属性不允许为空。如果业务逻辑允许空值，需要将属性类型设为 `double?` 并设置 `AllowNull = true`。

**代码示例：**
```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("自定义阈值")]
    [DoubleProperty(AllowNull = true, Watermark = "使用默认值")]
    public double? Threshold { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        // 处理空值逻辑
        double actualThreshold = Threshold ?? 0.05;
        
        return new ExecuteResult();
    }
}
```

## 3. 常见问题
- **Q: 为什么属性类型叫 Double 但文档标题是“小数”？**
  A: 在 C# 中使用 `double` 类型来表示小数/浮点数。活字格界面上称为“小数”。
- **Q: 可以用 `decimal` 类型吗？**
  A: 目前插件属性主要支持 `double`。如果需要高精度计算，建议先接收 `double` 再在代码中转换，或者使用字符串属性传入再解析。
