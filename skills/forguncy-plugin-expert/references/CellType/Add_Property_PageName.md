# 添加属性 - 页面选择属性 (Page Name)

## 参考资料
[页面选择属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/otherproperty/pagenameproperty)

## 概述
用于让用户从当前应用的页面列表中选择一个页面。属性类型必须为 `string`。
*(活字格 V9.1 新增)*

## 基础用法
```csharp
public class MyPluginCellType : CellType
{
    [DisplayName("跳转页面")]
    [PageNameProperty]
    public string TargetPage { get; set; }
}
```

## 高级用法

### 包含内建页面 (IncludeBuiltInPage)
默认情况下内建页面不可选。
```csharp
[PageNameProperty(IncludeBuiltInPage = true)]
public string TargetPage { get; set; }
```
