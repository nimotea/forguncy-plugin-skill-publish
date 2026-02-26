# 单元格设计时支持 - 属性联动与高级属性 (Property Interaction)

## 1. 属性值联动
[属性值联动 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/Attribute-value-linkage)
*(注意：此链接内容在原始请求中未详细提供，以下基于通用知识补充)*

如果需要在一个属性变化时自动修改另一个属性（例如选择“自动”模式时清空“自定义值”），通常在属性的 `set` 访问器中处理，或者在 Designer 中通过实现 `INotifyPropertyChanged` 相关逻辑（较复杂）。
对于对象属性，可以通过 `[Designer]` 特性指定对象的设计器来实现内部联动。

## 2. 折叠高级属性
[折叠高级属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/collapse-advanced-properties)

将不常用的属性隐藏在“高级”折叠区域中，简化属性面板。

使用 `[AdvancedProperty]` 特性。

```csharp
public class MyPluginCellType : CellType
{
    public string BasicProp { get; set; }

    [AdvancedProperty]
    [DefaultValue(null)] // 建议设置默认值
    public string AdvancedProp { get; set; }
}
```
**行为**:
- 如果用户未修改过高级属性，默认折叠。
- 如果用户修改了值，选中单元格时会自动展开。
