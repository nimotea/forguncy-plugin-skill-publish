# 添加属性 - 下拉列表属性 (Dropdown List Property)

在服务端命令插件开发中，除了使用枚举（Enum）创建下拉列表外，还可以通过 `[ComboProperty]` 特性为**字符串**类型的属性提供更灵活的下拉选择功能（例如支持自定义显示文本、允许输入新值、动态生成选项）。

## 1. 静态下拉列表 (ComboProperty)
如果属性类型是 `string`，可以使用 `[ComboProperty]` 特性并设置 `ValueList` 来提供候选项。

### 1.1 基础用法
```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("颜色")]
    [ComboProperty(ValueList = "Red|Green|Blue")]
    public string Color { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        return new ExecuteResult();
    }
}
```

### 1.2 分离显示值与实际值 (DisplayList)
通过 `DisplayList` 属性设置用户看到的文本，`ValueList` 设置实际存储的值。两者顺序必须对应。

```csharp
[DisplayName("请求方法")]
[ComboProperty(ValueList = "GET|POST|DELETE", DisplayList = "获取数据(GET)|提交数据(POST)|删除数据(DELETE)")]
public string Method { get; set; }
```

### 1.3 允许输入自定义值 (IsSelectOnly)
默认情况下 (`IsSelectOnly = true`)，用户只能从列表中选择。设置 `IsSelectOnly = false` 后，用户既可以从列表中选择，也可以直接输入列表以外的字符串。

```csharp
[DisplayName("字体")]
[ComboProperty(ValueList = "Arial|SimSun|微软雅黑", IsSelectOnly = false)]
public string FontFamily { get; set; }
```
> **注意**：当 `IsSelectOnly = false` 时，`DisplayList` 设置会被忽略。

### 1.4 支持搜索 (Searchable)
设置 `Searchable = true` 可以让下拉列表支持搜索过滤，适合选项较多的场景。

```csharp
[DisplayName("城市")]
[ComboProperty(ValueList = "Beijing|Shanghai|Guangzhou|Shenzhen|...", Searchable = true)]
public string City { get; set; }
```

---

## 2. 动态下拉列表 (Dynamic Dropdown)
如果下拉选项无法在编译时确定（例如需要读取数据库表名、打印机列表），需要重写 `CommandDesigner` 的 `GetEditorSetting` 方法。

### 代码示例
**1. Command 类：**
```csharp
[Designer("MyPlugin.Designer.MyPluginServerCommandDesigner, MyPlugin")] // 关联 Designer
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("选择打印机")]
    public string PrinterName { get; set; }
    
    // ... ExecuteAsync 实现 ...
}
```

**2. Designer 类：**
需要引用 `GrapeCity.Forguncy.Commands` 和 `GrapeCity.Forguncy.Plugin` 命名空间。

```csharp
public class MyPluginServerCommandDesigner : CommandDesigner<MyPluginServerCommand>
{
    public override EditorSetting GetEditorSetting(PropertyDescriptor property, IBuilderCommandContext builderContext)
    {
        if (property.Name == nameof(MyPluginServerCommand.PrinterName))
        {
            // 动态生成列表（示例：模拟获取数据）
            var printers = new List<string> { "Printer A", "Printer B", "Network Printer" };
            
            // 返回 ComboEditorSetting
            return new ComboEditorSetting(printers);
        }
        return base.GetEditorSetting(property, builderContext);
    }
}
```

如果需要动态列表也支持显示值与实际值分离：
```csharp
var items = new List<ComboItem>
{
    new ComboItem { Value = "p1", Display = "打印机一号" },
    new ComboItem { Value = "p2", Display = "打印机二号" }
};
return new ComboEditorSetting(items);
```
