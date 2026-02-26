# 添加属性 - 枚举属性 (Enum Property)

在服务端命令插件开发中，枚举属性会自动在设计器中渲染为下拉列表（ComboBox），供用户从预设选项中选择。

## 1. 默认枚举属性
定义一个枚举类型（`enum`），并将属性类型设置为该枚举，即可实现下拉选择。
默认情况下，下拉列表中显示的是枚举项的代码名称（如 `Student`, `Teacher`）。

### 代码示例
```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("用户角色")]
    public UserType Role { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        if (Role == UserType.Teacher) 
        {
            // ...
        }
        return new ExecuteResult();
    }
}

public enum UserType
{
    Student,
    Teacher,
    Worker
}
```

---

## 2. 自定义显示名称 ([Description])
为了让设计器中的下拉列表显示更友好的中文名称，需要在枚举项上添加 `[Description]` 特性。

### 代码示例
```csharp
public enum UserType
{
    [Description("在校学生")]
    Student,
    
    [Description("授课教师")]
    Teacher,
    
    [Description("企业职工")]
    Worker
}
```

## 3. 常见问题
- **Q: 枚举值可以存整数吗？**
  A: 枚举本质上是整数。在数据库或序列化时，它们通常以整数形式存储（除非做了特殊配置）。默认第一个项是 0，第二个是 1，以此类推。
- **Q: 如果我想让下拉框支持“多选”怎么办？**
  A: 标准枚举属性不支持多选。如果需要多选，请考虑使用 `[Flags]` 枚举配合自定义编辑器，或使用 `ComboProperty` 配合字符串存储。
