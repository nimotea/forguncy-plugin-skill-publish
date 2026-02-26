# API 速查表 (API Cheatsheet)

## IDataAccess
通过 `context.DataAccess` 访问。

- `ExecuteNonQuery(string sql, object parameters)`: 执行 UPDATE, INSERT, 或 DELETE 语句。
- `ExecuteScalar(string sql, object parameters)`: 返回第一行第一列的值。
- `GetTableData(string tableName)`: 获取指定表的数据。
- `AddTableData(string tableName, Dictionary<string, object> data)`: 向表中插入一行数据。
- `UpdateTableData(string tableName, Dictionary<string, object> data, string whereClause, object parameters)`: 更新数据行。

## IUserInfo
通过 `context.UserInfo` 访问。

- `Name`: 当前用户的用户名。
- `Role`: 分配给当前用户的角色列表。
- `Email`: 当前用户的电子邮件地址。
- `TenantId`: 租户标识符（用于多租户应用）。

## IGenerateContext
- `EvaluateFormulaAsync(object propertyValue)`: 计算属性值，该属性可能包含公式或直接值。
- `Log`: 访问服务器端记录器 (logger)。

## 客户端命令 (Client Command)
- `GetExecuteJavaScript()`: 必须重写的方法，返回在浏览器端执行的 JS 代码。
- `Forguncy.Page`: (JS) 访问当前页面对象，获取单元格值等。
- `Forguncy.CommandHelper`: (JS) 用于执行其他内置命令。

## 服务端 API (Server API)
- `[HttpGet]`, `[HttpPost]`: 标记 API 方法的 HTTP 动词。
- `[Route("url")]`: 定义 API 的访问路径。
- `this.Context`: (如果有) 访问活字格上下文信息。
- `IActionResult`: 返回类型，如 `Ok()`, `Json()`, `BadRequest()`。

## 中间件 (Middleware)
- `InvokeAsync(HttpContext context)`: 处理请求的核心方法。
- `context.Request`: 读取 Header, Body, QueryString。
- `context.Response`: 写入响应内容。
- `await _next(context)`: 将请求传递给下一个中间件。
