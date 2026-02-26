# 添加属性 - 字符串属性 (String Property)

在服务端命令插件开发中，字符串属性是最基础的属性类型。

## 1. 默认字符串属性
默认情况下，如果一个属性的类型是 `string`，活字格会自动将其识别为字符串属性，并在设计器中显示为文本输入框。

### 代码示例
```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("我的属性")]
    public string MyProperty { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        return new ExecuteResult();
    }
}
```

---

## 2. 高级配置 (TextPropertyAttribute)
如果需要更细致的控制（如水印、多行文本、多语言），可以使用 `[TextProperty]` 特性。
> **注意**：标注 `TextPropertyAttribute` 的属性类型必须是 `string`。

### 2.1 添加水印 (Watermark)
设置 `Watermark` 属性可以在输入框为空时显示提示文本。

```csharp
[DisplayName("名称")]
[TextProperty(Watermark = "请输入名称...")]
public string Name { get; set; }
```

### 2.2 支持多行文本 (AcceptsReturn)
设置 `AcceptsReturn = true` 可以让输入框支持回车换行，适用于输入长文本或代码片段。
*(要求活字格版本 >= 10.0.0.0)*

```csharp
[DisplayName("详细描述")]
[TextProperty(AcceptsReturn = true)]
public string Description { get; set; }
```

### 2.3 支持多语言 (CanSelectResource)
设置 `CanSelectResource = true` 会在属性编辑器旁显示资源选择按钮，允许用户选择多语言资源。
*(要求活字格版本 >= 10.0.0.0，且项目开启了多语言功能)*

**代码示例：**
```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("欢迎语")]
    [TextProperty(CanSelectResource = true)]
    public string WelcomeMessage { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        // 使用 GetApplicationResource 解析多语言 Key
        // 如果不是多语言环境，会直接返回原始字符串
        var message = this.GetApplicationResource(WelcomeMessage);
        
        return new ExecuteResult()
        {
            Message = message
        };
    }
}
```

## 3. 常见问题
- **Q: 为什么我看不到水印？**
  A: 请检查活字格设计器版本是否支持该特性。
- **Q: `GetApplicationResource` 哪里来的？**
  A: 它是 `Command` 基类的方法，用于在运行时解析资源键值。
