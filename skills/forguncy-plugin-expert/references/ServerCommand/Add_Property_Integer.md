# 添加属性 - 整数属性 (Integer Property)

在服务端命令插件开发中，整数属性用于接收用户输入的整数值（int）。

## 1. 默认整数属性
默认情况下，如果属性类型是 `int`，活字格会自动识别为整数属性，设计器会限制用户只能输入数字。
默认范围：
- 最小值：0
- 最大值：999

### 代码示例
```csharp
public class MyPluginCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("重试次数")]
    public int RetryCount { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        return new ExecuteResult();
    }
}
```

---

## 2. 高级配置 (IntPropertyAttribute)
使用 `[IntProperty]` 特性可以自定义数值范围、可空性等。
> **注意**：标注 `IntPropertyAttribute` 的属性类型必须是 `int` 或 `int?`。

### 2.1 控制数值范围 (Min/Max)
通过设置 `Min` 和 `Max` 属性来限制输入的数值范围。

```csharp
[DisplayName("评分")]
[IntProperty(Min = 1, Max = 10)]
public int Rating { get; set; }
```
如果不指定 Max/Min，且使用了 `[IntProperty]`，则默认范围扩展为 int 的完整取值范围（-2147483648 到 2147483647）。

### 2.2 支持空值 (AllowNull)
默认的 `int` 类型属性不允许为空。如果业务逻辑允许空值（例如“不填代表无限制”），需要将属性类型设为 `int?` 并设置 `AllowNull = true`。

**代码示例：**
```csharp
public class MyPluginCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("超时时间(毫秒)")]
    [IntProperty(AllowNull = true, Watermark = "无限制")]
    public int? Timeout { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        // 如果用户未填，Timeout 为 null
        int actualTimeout = Timeout ?? -1; 
        
        // ... 业务逻辑 ...
        return new ExecuteResult();
    }
}
```

## 3. 常见问题
- **Q: 为什么我输入的负数被自动变回0了？**
  A: 默认不加特性时最小值为 0。如需支持负数，请添加 `[IntProperty(Min = -100)]`。
- **Q: 属性类型写成 `long` 可以吗？**
  A: 不可以。`[IntProperty]` 仅支持 `int` 或 `int?`。长整型请参考其他处理方式或使用字符串转换。
