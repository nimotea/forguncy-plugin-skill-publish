# 搜索控制 (Search Control)

活字格设计器提供了全局搜索功能，允许用户搜索命令名称、属性值等。插件开发者可以通过 Attribute 来增强插件在搜索结果中的表现。

## 1. 属性搜索 [SearchableProperty]

默认情况下，并非所有属性值都会被索引。如果你希望用户能够通过搜索属性值找到使用了该插件的单元格或命令，需要给属性添加 `[SearchableProperty]`。

### 代码示例

```csharp
public class MyPluginCommand : Command
{
    [FormulaProperty]
    [SearchableProperty] // 允许用户搜索此属性的值（如搜索 "Order123" 能找到引用了该值的命令）
    [DisplayName("订单编号")]
    public object OrderId { get; set; }
}
```

## 2. 命令关键字搜索 [SearchTags]

有时命令的类名或显示名不足以覆盖所有用户的搜索习惯。使用 `[SearchTags]` 可以为命令添加额外的搜索关键字（Tag）。

### 代码示例

```csharp
[SearchTags("HTTP", "Web", "API", "Request", "Post", "Get")]
[DisplayName("发送网络请求")]
public class HttpRequestCommand : Command
{
    // ...
}
```

### 效果
用户在设计器搜索框输入 "API" 或 "Web" 时，即使命令名称是 "发送网络请求"，该命令也会出现在搜索结果中。
