# 添加属性 - 布尔属性 (Boolean Property)

## 参考资料
[布尔属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/booleanproperty)

## 概述
`bool` 类型的属性会自动识别为布尔属性（复选框）。

## 基础用法
```csharp
public class MyPluginCellType : CellType
{
    [DisplayName("启用功能")]
    [DefaultValue(true)] // 建议显式设置默认值特性
    public bool IsEnabled { get; set; } = true;
}
```

## 高级用法 ([BoolProperty])

### 控制缩进 (IndentLevel)
用于体现属性间的层级关系。
```csharp
[BoolProperty(IndentLevel = 0)]
public bool ParentOption { get; set; }

[BoolProperty(IndentLevel = 1)]
public bool ChildOption { get; set; }
```
