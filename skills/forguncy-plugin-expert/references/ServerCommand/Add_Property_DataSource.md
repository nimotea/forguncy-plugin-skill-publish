# 添加属性 - 数据源属性 (Data Source Property)

数据源属性允许插件直接绑定活字格中的数据表，并支持用户选择需要使用的列。插件在运行时可以获取该数据表（或视图）中的数据。

## 1. 基础用法
要创建一个数据源属性，需要：
1.  属性类型必须为 `object`。
2.  标注 `[BindingDataSourceProperty]` 特性。
3.  在运行时使用 `dataContext.GetBindingDataSourceValueAsync()` 获取数据。

### 代码示例
```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("绑定数据源")]
    [BindingDataSourceProperty]
    public object DataSource { get; set; }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        // 获取数据源数据（返回类型通常是 List<Dictionary<string, object>> 或类似结构）
        var data = await dataContext.GetBindingDataSourceValueAsync(this.DataSource);
        
        // 处理数据...
        return new ExecuteResult();
    }
}
```

---

## 2. 高级配置

### 2.1 预置列 (Columns)
可以通过 `Columns` 属性指定插件期望用户绑定的列名。多个列用 `|` 分隔。

```csharp
[BindingDataSourceProperty(Columns = "ID|Name|Age")]
public object DataSource { get; set; }
```

### 2.2 自定义列显示名称
如果希望设计器中显示的列名与内部使用的列名不同，可以使用 `内部名:显示名` 的格式。

```csharp
[BindingDataSourceProperty(Columns = "ID|Name:姓名|Age:年龄")]
public object DataSource { get; set; }
```

### 2.3 列描述信息 (ColumnsDescription)
为列添加更详细的说明文本，帮助用户理解每一列的用途。

```csharp
[BindingDataSourceProperty(
    Columns = "ID|PID", 
    ColumnsDescription = "ID:唯一标识符|PID:父级ID(用于构建树)")]
public object DataSource { get; set; }
```

### 2.4 允许添加自定义列 (AllowAddCustomColumns)
默认情况下，如果指定了 `Columns`，用户只能看到这些预置列。如果希望允许用户额外添加其他列，设置 `AllowAddCustomColumns = true`。
*(要求活字格版本 >= 9.0.100.0)*

```csharp
[BindingDataSourceProperty(AllowAddCustomColumns = true, Columns = "ID|Name")]
public object DataSource { get; set; }
```

### 2.5 树形结构支持 (IsIdPidStructure)
如果插件需要处理树形数据（如组织架构），可以开启 `IsIdPidStructure`，并指定 ID 和 PID 列的名称。

```csharp
[BindingDataSourceProperty(
    Columns = "ID|Name|PID", 
    IsIdPidStructure = true, 
    TreeIdColumnName = "ID", 
    TreePidColumnName = "PID")]
public object TreeDataSource { get; set; }
```

## 3. 运行时数据获取
`GetBindingDataSourceValueAsync` 方法返回的数据结构包含了用户在设计器中绑定的所有行和列的数据。通常是一个包含字典的列表，其中键是列名，值是单元格数据。
