# 添加属性 - 数据库连接选择属性 (Database Connection Selector)

该属性允许用户从活字格应用的“外联数据库”列表中选择一个数据库连接。插件可以使用选中的连接执行 SQL 查询或事务操作。
*(此特性为活字格 V9.1 新增功能)*

## 1. 基础用法
要创建一个数据库连接选择属性，需要：
1.  属性类型必须为 `string`。
2.  标注 `[DatabaseConnectionSelectorProperty]` 特性。
3.  在运行时使用 `dataContext.DataAccess` 相关 API 操作数据库。

### 代码示例
```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("目标数据库")]
    [DatabaseConnectionSelectorProperty]
    public string ConnectionName { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        var dataAccess = dataContext.DataAccess;
        
        // 1. 获取连接字符串 (ConnectionName 为空时表示内建库)
        // 注意：GetConnectionStringByID 内部已处理 ConnectionName 为空的情况
        // 但通常我们会显式处理内建库逻辑
        
        // 2. 执行查询 (直接传入 ConnectionName)
        // ExecuteSqlAsync 第一个参数接受 connectionName
        var sql = "SELECT count(*) FROM MyTable";
        var result = await dataAccess.ExecuteSqlAsync(this.ConnectionName, sql, null);
        
        return new ExecuteResult() 
        { 
            Message = $"Row Count: {result[0].Values.First()}" 
        };
    }
}
```

---

## 2. 高级配置

### 2.1 包含内建数据库 (IncludeBuiltInDatabase)
默认情况下，下拉列表只显示外联数据库。如果希望列表包含“内建数据库”（即活字格自带的 SQLite 库），设置 `IncludeBuiltInDatabase = true`。

```csharp
[DisplayName("选择数据库")]
[DatabaseConnectionSelectorProperty(IncludeBuiltInDatabase = true)]
public string ConnectionName { get; set; }
```
> **注意**：当用户选择“（空）”或内建数据库时，`ConnectionName` 属性的值通常为 `null` 或空字符串。在调用 `ExecuteSqlAsync` 时，传入 `null` 即代表操作内建数据库。

## 3. 事务处理
如果需要在选定的数据库上执行事务，可以使用 `BeginTransaction`。

```csharp
public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
{
    var dataAccess = dataContext.DataAccess;
    
    // 获取实际的连接字符串（用于事务控制）
    var connectionStr = dataAccess.GetConnectionStringByID(this.ConnectionName);

    // 开启事务
    dataAccess.BeginTransaction(connectionStr);
    try
    {
        // 执行带事务的操作
        await dataAccess.ExecuteSqlAsync(this.ConnectionName, "INSERT INTO ...", null);
        
        // 提交事务
        dataAccess.CommitTransaction(connectionStr);
    }
    catch
    {
        // 回滚事务
        dataAccess.RollbackTransaction(connectionStr);
        throw;
    }
    
    return new ExecuteResult();
}
```
