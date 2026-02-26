# 开发表单类单元格 - 支持单元格权限 (Cell Permissions)

## 参考资料
[支持单元格权限 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportcellpermissions)

## 概述
支持针对不同角色设置单元格的可见、编辑、启用权限。通常需要同时实现 `ISupportReadOnly` 和 `ISupportDisable`。

## C# 实现
实现 `ISupportUIPermission` 接口。

```csharp
public class MyPluginCellType : CellType, ISupportDisable, ISupportReadOnly, ISupportUIPermission
{
    public bool ReadOnly { get; set; }
    public bool IsDisabled { get; set; }

    [DisplayName("单元格权限")]
    public List<UIPermission> UIPermissions { get; set; } = GetDefaultPermission();

    public static List<UIPermission> GetDefaultPermission()
    {
        var roles = new List<string>() { "FGC_Anonymous" };
        return new List<UIPermission>
        {
            new UIPermission(){ Scope = UIPermissionScope.Enable, AllowRoles = roles },
            new UIPermission(){ Scope = UIPermissionScope.Editable, AllowRoles = roles },
            new UIPermission(){ Scope = UIPermissionScope.Visible, AllowRoles = roles },
        };
    }
}
```
*JS 端无需额外代码，活字格会自动调用 setReadOnly/disable/enable 等方法。*
