# 添加属性 - 下拉列表属性 (Dropdown/Combo Property)

## 参考资料
[下拉列表属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/dropdownlistproperty)

## 概述
用于提供字符串类型的候选列表。属性类型必须为 `string`。

## 基础用法 ([ComboProperty])
```csharp
public class MyPluginCellType : CellType
{
    [ComboProperty(ValueList = "Option1|Option2|Option3")]
    public string MyProperty { get; set; }
}
```

## 高级用法

### 1. 显示值与实际值不同 (DisplayList)
```csharp
[ComboProperty(ValueList = "val1|val2", DisplayList = "显示1|显示2")]
public string MyProperty { get; set; }
```

### 2. 允许输入自定义值 (IsSelectOnly)
设置为 `false` 时，允许用户输入列表中不存在的值。
```csharp
[ComboProperty(ValueList = "A|B", IsSelectOnly = false)]
public string MyProperty { get; set; }
```

### 3. 支持搜索 (Searchable)
```csharp
[ComboProperty(ValueList = "...", Searchable = true)]
public string MyProperty { get; set; }
```

### 4. 动态下拉列表
通过重写 `CellTypeDesigner` 的 `GetEditorSetting` 方法实现（高级）。
