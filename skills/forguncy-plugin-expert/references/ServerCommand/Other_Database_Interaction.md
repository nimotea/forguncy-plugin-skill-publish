# 数据库交互 (Database Interaction)

在服务端命令插件中，经常需要对活字格内置数据库进行增删改查操作。活字格通过上下文对象提供了 `IDataAccess` 接口来实现这些功能。

## 获取 DataAccess 实例

在 `ExecuteAsync` 方法中，可以通过 `dataContext.DataAccess` 获取数据库访问实例。

```csharp
public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
{
    IDataAccess dataAccess = dataContext.DataAccess;
    // ...
}
```

## 核心方法

`IDataAccess` 接口提供了以下常用方法：

### 1. 查询数据 (GetTableData)

```csharp
// 1. 获取全表数据（慎用，数据量大时会有性能问题）
// 返回 List<Dictionary<string, object>>
var allRows = dataAccess.GetTableData("表格1");

// 2. 根据主键/唯一键查询单条记录
// ColumnValuePair 用于指定查询条件（列名, 值）
var primaryKey = new ColumnValuePair("ID", 1);
// 返回 Dictionary<string, object>
var singleRow = dataAccess.GetTableData("表格1", primaryKey);
```

### 2. 添加数据 (AddTableData)

```csharp
var newRow = new Dictionary<string, object>
{
    { "姓名", "张三" },
    { "年龄", 18 },
    { "入职日期", DateTime.Now }
};

// 执行插入
dataAccess.AddTableData("表格1", newRow);
```

### 3. 更新数据 (UpdateTableData)

```csharp
// 指定要更新的记录（通常通过主键 ID）
var condition = new ColumnValuePair("ID", 1);

// 指定要更新的字段和新值
var updateValues = new Dictionary<string, object>
{
    { "年龄", 19 },
    { "状态", "已转正" }
};

// 执行更新
dataAccess.UpdateTableData("表格1", condition, updateValues);
```

### 4. 删除数据 (DeleteTableData)

```csharp
// 指定要删除的记录
var condition = new ColumnValuePair("ID", 1);

// 执行删除
dataAccess.DeleteTableData("表格1", condition);
```

### 5. 执行自定义 SQL (ExecuteSql)

如果内置方法无法满足需求（如复杂联表查询），可以执行自定义 SQL。

**注意**：为了安全起见，务必使用参数化查询，防止 SQL 注入。

```csharp
string sql = "SELECT * FROM 表格1 WHERE 年龄 > @Age";
var parameters = new Dictionary<string, object>
{
    { "@Age", 20 }
};

// ExecuteSql 返回 DataTable 或受影响行数，具体取决于具体实现和重载
// 通常用于执行查询
var result = dataAccess.ExecuteSql(sql, parameters);
```

## 事务处理

如果在插件中执行多步数据库操作，建议使用事务来保证数据一致性。

```csharp
try 
{
    dataAccess.BeginTransaction();
    
    // Step 1: 扣减库存
    dataAccess.UpdateTableData(...);
    
    // Step 2: 创建订单
    dataAccess.AddTableData(...);
    
    dataAccess.CommitTransaction();
}
catch (Exception ex)
{
    dataAccess.RollbackTransaction();
    throw; // 抛出异常让上层处理或返回错误码
}
```

## 引用数据表名

在插件属性中，可以使用 `[BindingDataSourceProperty]` 来让用户选择数据表，从而获取正确的表名字符串。

```csharp
[BindingDataSourceProperty]
[DisplayName("选择数据表")]
public string TableName { get; set; }
```
