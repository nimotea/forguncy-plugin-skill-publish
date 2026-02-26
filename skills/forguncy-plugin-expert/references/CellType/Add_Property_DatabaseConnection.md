# 添加属性 - 数据库连接选择属性 (Database Connection Selector)

## 参考资料
[数据库连接选择属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/otherproperty/databaseconnectionselectorproperty)

## 概述
用于让用户从当前应用的数据库连接列表中选择一个连接。属性类型必须为 `string`。
*(活字格 V9.1 新增)*

## 基础用法
```csharp
public class MyPluginCellType : CellType
{
    [DisplayName("目标数据库")]
    [DatabaseConnectionSelectorProperty]
    public string ConnectionName { get; set; }
}
```

## 高级用法

### 包含内建数据库 (IncludeBuiltInDatabase)
默认情况下只显示外联数据库。设置此属性可包含内建数据库（Sqlite）。
注意：内建数据库的连接名称为 `null` 或空字符串，需在代码中特殊处理。

```csharp
[DatabaseConnectionSelectorProperty(IncludeBuiltInDatabase = true)]
public string ConnectionName { get; set; }
```

## 服务端使用示例
在服务端命令或 API 中使用选中的连接名。

```csharp
public async void Execute(string connectionName, IDataAccess dataAccess)
{
    // 获取连接字符串
    // 如果 connectionName 为空，通常表示内建数据库，GetConnectionStringByID 可能有默认行为或需单独处理
    var connectionStr = dataAccess.GetConnectionStringByID(connectionName);

    dataAccess.BeginTransaction(connectionStr);
    try
    {
        await dataAccess.ExecuteSqlAsync(connectionName, "SELECT * FROM Table1", null);
        dataAccess.CommitTransaction(connectionStr);
    }
    catch
    {
        dataAccess.RollbackTransaction(connectionStr);
        throw;
    }
}
```
