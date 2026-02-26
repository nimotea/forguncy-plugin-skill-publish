# 添加属性 - 对象列表属性 (Object List Property)

对象列表属性允许用户配置一个包含多个对象的列表。适用于需要用户添加多条相似配置的场景（例如：添加多个HTTP请求头、定义多个数据列映射）。

## 1. 基础用法
要创建一个对象列表属性，需要：
1.  定义一个类，继承 `ObjectPropertyBase` 并实现 `INamedObject` 接口。
2.  在 Command 中定义 `List<INamedObject>` 类型的属性。
3.  使用 `[ObjectListProperty]` 特性关联 Item 类型。

### 代码示例

**1. 定义列表项类 (MyListItem)：**

> **重要提示**：列表项类**必须**同时满足以下两个条件：
> 1. 继承 `ObjectPropertyBase`（提供对象的基础序列化能力）。
> 2. 实现 `INamedObject` 接口（必须显式定义 `public string Name { get; set; }` 属性）。

```csharp
using System.ComponentModel;
using GrapeCity.Forguncy.Plugin;

// 1. 必须继承 ObjectPropertyBase
// 2. 必须实现 INamedObject 接口
public class MyListItem : ObjectPropertyBase, INamedObject
{
    // INamedObject 接口强制要求实现 Name 属性
    // 该属性的值将直接作为设计器中列表左侧导航栏的显示标题
    [DisplayName("名称")]
    public string Name { get; set; }

    [DisplayName("值")]
    public string Value { get; set; }

    // 支持任意子属性类型，如公式
    [DisplayName("动态参数")]
    [FormulaProperty]
    public object DynamicParam { get; set; }
}
```

**2. 在 Command 中引用：**
```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("请求头列表")]
    [ObjectListProperty(ItemType = typeof(MyListItem))]
    public List<INamedObject> Headers { get; set; } = new List<INamedObject>(); // 务必初始化

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        foreach (var item in Headers)
        {
            var headerItem = item as MyListItem;
            if (headerItem != null)
            {
                // 处理逻辑...
            }
        }
        return new ExecuteResult();
    }
}
```

---

## 2. 高级配置

### 2.1 限制数量 (MaxCount)
设置 `MaxCount` 可以限制用户最多添加多少个列表项。

```csharp
[ObjectListProperty(ItemType = typeof(MyListItem), MaxCount = 5)]
public List<INamedObject> Items { get; set; }
```

### 2.2 设置默认名称 (DefaultName)
设置 `DefaultName` 可以指定新添加的列表项的默认名称前缀（如 "参数1", "参数2"）。

```csharp
[ObjectListProperty(ItemType = typeof(MyListItem), DefaultName = "参数")]
public List<INamedObject> Items { get; set; }
```

## 3. ObjectListProperty vs ListProperty
活字格提供了两种列表属性特性：
- **`[ObjectListProperty]`**（推荐）：点击编辑后弹出二级对话框，左侧是列表导航，右侧是当前项的属性面板。适合**子属性较多**的复杂对象。
- **`[ListProperty]`**：点击编辑后弹出二级对话框，直接以表格（Grid）形式显示列表。适合**子属性较少**（通常小于3个）的简单对象。

## 4. 常见问题
- **Q: 为什么代码里要用 `List<INamedObject>` 而不是 `List<MyListItem>`？**
  A: 这是活字格 SDK 的约束。属性类型必须声明为 `List<INamedObject>`，但在运行时（ExecuteAsync）您可以将其元素转换为具体的 `MyListItem` 类型进行使用。
