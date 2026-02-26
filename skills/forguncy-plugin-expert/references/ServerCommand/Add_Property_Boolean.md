# 添加属性 - 布尔属性 (Boolean Property)

在服务端命令插件开发中，布尔属性用于接收用户输入的 `True/False` 值，通常在设计器中显示为复选框（Checkbox）。

## 1. 默认布尔属性
默认情况下，如果属性类型是 `bool`，活字格会自动识别为布尔属性。

### 代码示例
```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("启用日志")]
    public bool EnableLogging { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        return new ExecuteResult();
    }
}
```

---

## 2. 高级配置 (BoolPropertyAttribute)
使用 `[BoolProperty]` 特性可以控制复选框的缩进级别，使属性面板具有更好的视觉层次。

### 2.1 控制缩进 (IndentLevel)
通过 `IndentLevel` 属性设置缩进等级，默认值为 0。

```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("开启高级模式")]
    [BoolProperty(IndentLevel = 0)]
    public bool AdvancedMode { get; set; }

    [DisplayName("忽略错误")]
    [BoolProperty(IndentLevel = 1)] // 缩进一级，看起来像是上一项的子选项
    public bool IgnoreErrors { get; set; }

    [DisplayName("自动重试")]
    [BoolProperty(IndentLevel = 1)]
    public bool AutoRetry { get; set; }
}
```

## 3. 常见陷阱：默认值设置
**重要提示**：如果希望布尔属性的默认值为 `true`，**必须**同时做两件事：
1. 在 C# 属性初始化器中设为 `true`。
2. 添加 `[DefaultValue(true)]` 特性。

如果只做了第 1 步而没有添加 `[DefaultValue(true)]`，设计器可能无法正确保存该属性的默认状态。

**正确示例：**
```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("默认开启")]
    [DefaultValue(true)] // 必须添加！
    public bool IsActive { get; set; } = true; // 必须初始化！

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        return new ExecuteResult();
    }
}
```

## 4. 进阶技巧：默认开启且支持取消的模式 (Default True Hack)

如果你开发的是前端插件（如 CellType），且希望 JS 端逻辑更简洁（避免处理 `undefined`），可以使用“反向序列化技巧。

### 场景
你希望属性默认开启（True），但为了让 JS 端代码能简单地使用 `if (options.prop)` 判断（将 `undefined` 视为 false），你需要让 `true` 值被显式序列化，而 `false` 值被省略。

### 实现方式
- C# 初始值设为 `true`（业务默认值）。
- `[DefaultValue]` 设为 `false`（欺骗序列化器，使其认为 true 是非默认值，从而强制序列化）。

```csharp
public class MyPluginCellType : CellTypeBase
{
    [DisplayName("显示标题")]
    [DefaultValue(false)] // 关键点：欺骗序列化器
    public bool ShowTitle { get; set; } = true; // 实际默认值
}
```

### JS 端效果
- **默认情况**：`ShowTitle` 为 `true`，序列化为 `{"ShowTitle": true}`。JS 读到 `true`。
- **用户取消勾选**：`ShowTitle` 为 `false`，等于 `DefaultValue`，不序列化。JS 读到 `undefined` (Falsy)。
