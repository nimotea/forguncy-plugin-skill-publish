# 添加属性 - 角色选择属性 (Role Selector)

## 参考资料
[角色选择属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/otherproperty/roleselectorproperty)

## 概述
用于让用户从当前应用的角色列表中选择一个或多个角色。属性类型必须为 `List<string>`。
*(活字格 V9.1 新增)*

## 基础用法
```csharp
public class MyPluginCellType : CellType
{
    [DisplayName("允许的角色")]
    [RoleSelectorProperty]
    public List<string> AllowedRoles { get; set; } = new List<string>();
}
```

## 注意事项
1. 属性类型必须是 `List<string>`。
2. 返回的是角色名称列表。
