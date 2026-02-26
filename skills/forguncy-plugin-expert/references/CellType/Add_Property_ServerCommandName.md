# 添加属性 - 服务端命令选择属性 (Server Command Name)

## 参考资料
[服务端命令选择属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/otherproperty/servercommandnameproperty)

## 概述
用于让用户从当前应用的服务端命令列表中选择一个命令。属性类型必须为 `string`。
*(活字格 V9.1 新增)*

## 基础用法
```csharp
public class MyPluginCellType : CellType
{
    [DisplayName("调用命令")]
    [ServerCommandNameProperty]
    public string CommandName { get; set; }
}
```

## 注意事项
1. 仅用于选择命令名称，调用逻辑需自行实现（通常通过 `ExecuteServerCommand` 等 API）。
2. 属性类型必须是 `string`。
