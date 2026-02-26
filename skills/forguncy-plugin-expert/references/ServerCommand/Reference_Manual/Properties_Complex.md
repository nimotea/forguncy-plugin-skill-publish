# Properties Complex

## Databaseconnectionselectorproperty

# 数据库连接选择属性

## Content

<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">此特性为活字格V9.1新增功能。</span>

```
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [DatabaseConnectionSelectorProperty]
        public string Connection { get; set; }

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            var dataAccess = dataContext.DataAccess;
            var connectionStr = dataAccess.GetConnectionStringByID(Connection);

            dataAccess.BeginTransaction(connectionStr);
            try
            {
                var result = await dataAccess.ExecuteSqlAsync(Connection, "select * from 表1", null);
                dataAccess.CommitTransaction(connectionStr);
            }
            finally
            {
                dataAccess.RollbackTransaction(connectionStr);
            }
            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
```

<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">在设计器中效果如下：</span>
<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">在数据库连接管理中连接了一些外链数据库之后：</span>

<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">可以通过标注了</span><span class="ne-text">DatabaseConnectionSelectorProperty</span><span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">的属性选择特定数据库。</span>

<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">如果需要更细致的控制，可以通过</span><span class="ne-text">DatabaseConnectionSelectorProperty</span><span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">的其他属性来控制。</span>
**<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">（空）显示为内建库</span>**

1. <span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">设置</span><span class="ne-text">DatabaseConnectionSelectorProperty</span><span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">的IncludeBuiltInDatabase属性。</span>
2. 代码：

    ```
         public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [DatabaseConnectionSelectorProperty(IncludeBuiltInDatabase = true)]
            public string Connection { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                var dataAccess = dataContext.DataAccess;
                var connectionStr = dataAccess.GetConnectionStringByID(Connection);
    
                dataAccess.BeginTransaction(connectionStr);
                try
                {
                    var result = await dataAccess.ExecuteSqlAsync(Connection, "select * from 表1", null);
                    dataAccess.CommitTransaction(connectionStr);
                }
                finally
                {
                    dataAccess.RollbackTransaction(connectionStr);
                }
                return new ExecuteResult();
            }
    
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    ```
3. 效果：
    
4. 说明：<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">对于内建数据库（Sqlite）连接名称为null。</span>

<span class="ne-text" style="box-sizing: content-box; margin: 0px; padding: 0px; transition: filter 0.5s ease-in-out 0s; line-height: 25.6px;">注意：标注DatabaseConnectionSelectorProperty的属性类型必须是 string。</span>

---

## Datasourceproperty

# 数据源属性

## Content

如果属性绑定数据表的值，希望通过数据对话框编辑，可以通过标注BindingDataSourcePropertyAttribute 的方式设置。
注意，标注BindingDataSourcePropertyAttribute的属性类型必须是 object。

```auto
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [BindingDataSourceProperty]
        [DisplayName("数据源")]
        public object DataSource { get; set; }

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            var value = await dataContext.GetBindingDataSourceValueAsync(this.DataSource);
            var result = new ExecuteResult();

            result.ReturnValues.Add("结果", value);

            return result;
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
```

在设计器中效果如下：

执行结果如下：

如果需要更细致的控制，可以通过BindingDataSourcePropertyAttribute的其他属性来控制。
**1. 预置数据列**

1. 设置BindingDataSourcePropertyAttribute的 Columns 属性。
2. 代码：
    格式：列名\|列名2\.\.\.

    ```auto
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [BindingDataSourceProperty(Columns = "ID|Name")]
            [DisplayName("数据源")]
            public object DataSource { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                var value = await dataContext.GetBindingDataSourceValueAsync(this.DataSource);
                var result = new ExecuteResult();
    
                result.ReturnValues.Add("结果", value);
    
                return result;
            }
    
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    ```
3. 设计器效果：
    

**2\. 为预置数据列添加显示文本**

1. 设置 BindingDataSourcePropertyAttribute 的 Columns 属性。
2. 代码：
    格式：列名:显示名\|列名2:显示名\|\.\.\.

    ```auto
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [BindingDataSourceProperty(Columns = "ID|Name:姓名|Age:年龄")]
            [DisplayName("数据源")]
            public object DataSource { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                var value = await dataContext.GetBindingDataSourceValueAsync(this.DataSource);
                var result = new ExecuteResult();
    
                result.ReturnValues.Add("结果", value);
    
                return result;
            }
    
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    ```
3. 设计器效果：
    
4. 注意：设置显示文本不影响JavaScript端数据处理，只影响在设计器中的显示。
    
5. 如果在此模式下仍然需要添加自定义列，可以设置<span class="ne-text">AllowAddCustomColumns</span>属性。

    ```auto
        public class MyPluginCellType : CellType
        {
            [BindingDataSourceProperty(AllowAddCustomColumns = true, Columns = "ID|Name:姓名|Age:年龄")]
            [DisplayName("绑定数据源")]
            public object DataSource { get; set; }
        }
    ```
6. 设置AllowAddCustomColumns之后效果如下（此特性需要活字格版本大于等于9.0.100.0）。
    

**3\. 为预置数据源列添加描述信息**

1. 设置 BindingDataSourcePropertyAttribute 的 ColumnsDescription 属性。
2. 代码：
    格式：列名:描述\|列名2:描述2\.\.\.

    ```auto
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [BindingDataSourceProperty(Columns = "ID|Name|Age", ColumnsDescription = "ID:通常绑定主键列|Age:表示年龄列")]
            [DisplayName("数据源")]
            public object DataSource { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                var value = await dataContext.GetBindingDataSourceValueAsync(this.DataSource);
                var result = new ExecuteResult();
    
                result.ReturnValues.Add("结果", value);
    
                return result;
            }
    
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    ```
3. 设计器效果：
    
4. 注意，需要和Columns属性配合使用，在Columns里没有的列，设置的描述会被忽略。

**4\. 开启树结构查询配置（ID/PID 结构）**

1. 什么是ID/PID结构
    在数据库中，是用二维表保存数据的，但是现实生活中，很多数据会有父子关系，例如公司的组织机构，会在数据库中保存为如下形式，这样就可以使用二维表表示树结构了。

    | ID | 名称 | PID |
    | --- | --- | --- |
    | 1 | xx公司 |  |
    | 2 | 财务部 | 1 |
    | 3 | 销售部 | 1 |
    | 4 | 销售一组 | 3 |
    | 5 | 销售二组 | 3 |
2. 设置BindingDataSourcePropertyAttribute 的 IsIdPidStructure 属性为True声明接受树结构表。
3. 代码：

    ```auto
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [BindingDataSourceProperty(Columns = "ID|Name|PID", IsIdPidStructure = true, TreeIdColumnName = "ID", TreePidColumnName = "PID")]
            [DisplayName("数据源")]
            public object DataSource { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                var value = await dataContext.GetBindingDataSourceValueAsync(this.DataSource);
                var result = new ExecuteResult();
    
                result.ReturnValues.Add("结果", value);
    
                return result;
            }
    
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    ```
4. 设计器效果：
    会在其他标签页中增加“树形结构查询配置”的选项。
    ****

注意：开启树形结构查询配置IsIdPidStructure属性后，需要配合设置 TreeIdColumnName 和 TreePidColumnName 属性。
**5.** **支持查询子表列**

1. 活字格中的子表
    当在活字格中，设置关联关系时，可以勾选“是否有子表关联？”为True，此时，主表会增加一个虚拟列，如下图中的“订单详情表”。
    
2. 设置BindingDataSourcePropertyAttribute 的 SupportDetailTable 属性。
3. 代码：

    ```csharp
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [BindingDataSourceProperty(SupportDetailTable = true)]
            [DisplayName("数据源")]
            public object DataSource { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                var value = await dataContext.GetBindingDataSourceValueAsync(this.DataSource);
                var result = new ExecuteResult();
    
                result.ReturnValues.Add("结果", value);
    
                return result;
            }
    
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    ```
4. 设计器效果：
    
5. 运行时获取数据的结果。数据库数据如下：
    订单表
    
    订单详情表
    
    执行结果

---

## Dropdownlistproperty

# 下拉列表属性

## Content

如果属性的类型是字符串，默认属性值是可以接受任意字符串的，如果希望提供字符串值候选列表，可以通过标注ComboPropertyAttribute 的并设置ValueList属性的方式实现。多个值用“\|”分隔。
注意，标注ComboPropertyAttribute的属性类型必须是 string。

```auto
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [ComboProperty(ValueList = "Student|Teacher|Worker")]
        public string MyProperty { get; set; }

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            return new ExecuteResult();
        }
        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
```

在设计器中效果如下：

如果需要更细致的控制，可以通过ComboPropertyAttribute的其他属性来控制。
**1\. 值与显示值不同**

1. 设置ComboPropertyAttribute 的 DisplayList 属性。
2. 代码：

    ```auto
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [ComboProperty(ValueList = "Student|Teacher|Worker", DisplayList = "学生|教师|工人")]
            public string MyProperty { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                return new ExecuteResult();
            }
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    ```
3. 效果：
    
4. 其他说明：
    此方法可以使用户在选择时选择中文选项，而单元格实际保存值为英文，方便程序处理。ValueList和DisplayList通过数量和顺序匹配。如果DisplayList数量超出ValueList数量，多出部分会被忽略；如果DisplayList数量少于ValueList数量，不足部分会使用ValueList对应的值。

**2\. 允许用户使用列表以外的值**

1. 设置ComboPropertyAttribute 的 IsSelectOnly属性。
2. 代码：

    ```auto
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [ComboProperty(ValueList = "Student|Teacher|Worker", IsSelectOnly = false)]
            public string MyProperty { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                return new ExecuteResult();
            }
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    ```
3. 效果：
    
4. 注意：
    IsSelectOnly 为 False 时，DisplayList 设置会被忽略；不填时 IsSelectOnly 属性的默认值为 True。

**3\. 支持搜索**

1. 设置ComboPropertyAttribute 的 Searchable 属性。
2. 代码：

    ```auto
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [ComboProperty(ValueList = "aa|bb|cc", Searchable = true)]
            public string MyProperty { get; set; }
    
            [ComboProperty(ValueList = "aa|bb|cc", Searchable = true, IsSelectOnly = false)]
            public string MyProperty2 { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                return new ExecuteResult();
            }
    
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    ```
3. 效果：
    
    
4. 策略：
    * <span class="ne-text">如果 IsSelectOnly 为 True ，则搜索框会在下拉框中。</span>
    * <span class="ne-text">如果 IsSelectOnly 为 False ，则可以直接输入，下拉框会自动按照输入的字符匹配。此模式下同样可以输入下拉框中不存在的字符串。</span>
    * <span class="ne-text">本特性要求活字格版本大于等于9.0.100.0。</span>

#### 动态下拉列表

有时，下拉列表中的选项不是开发时决定的，而是动态生成，例如下拉打印机列表。可以通过重写Command的Designer 通过代码动态生成列表。

```auto
    [Designer("MyPlugin.Designer.MyPluginServerCommandDesigner, MyPlugin")]
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        public string MyProperty { get; set; }

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }

    public class MyPluginServerCommandDesigner : CommandDesigner<MyPluginServerCommand>
    {
        public override EditorSetting GetEditorSetting(PropertyDescriptor property, IBuilderCommandContext builderContext)
        {
            if (property.Name == nameof(MyPluginServerCommand.MyProperty))
            {
                var list = new string[] { "aaa", "bbb", "ccc" };  // 代码动态生成
                return new ComboEditorSetting(list);
            }
            return base.GetEditorSetting(property, builderContext);
        }
    }
```

如果希望下拉列表的显示值和选择后保存的值不一样，可以如下修改 GetEditorSetting 方法，让List的每一项不是字符串，而是一个对象。通过设置 ComboEditorSetting 的 displayMember和valueMember来指定对象的哪个属性用于显示，哪个属性用于保存值。

```auto
    public class MyPluginServerCommandDesigner : CommandDesigner<MyPluginServerCommand>
    {
        public override EditorSetting GetEditorSetting(PropertyDescriptor property, IBuilderCommandContext builderContext)
        {
            if (property.Name == nameof(MyPluginCellType.MyProperty))
            {
                var list = new List<ComboItem>
                {
                    new ComboItem(null, "<空>"),
                    new ComboItem("student", "学生"),
                    new ComboItem("teacher", "教师")
                };
                return new ComboEditorSetting(list, nameof(ComboItem.Display), nameof(ComboItem.Value));
            }
            return base.GetEditorSetting(property, builderContext);
        }
    }
    
    public class ComboItem
    {
        public ComboItem(string value, string display)
        {
            Value = value;
            Display = display;
        }
        public string Value { get; set; }
        public string Display { get; set; }
    }
```

---

## Listproperty

# 列表属性

## Content

如果一个属性的类型是List类型，List的每一项又包含了子属性，那么可以通过标注ListPropertyAttribute，使得活字格设计器可以通过弹出二级对话框来编辑该属性。
注意，ObjType属性里声明的类型必须与属性类型一致。
自定义对象的类型应该从 ObjectPropertyBase 类派生，以确保在单元格复制的时候，子属性可以被正确的深克隆（ObjectPropertyBase实现了默认的深克隆逻辑）。

```auto
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [ListProperty]
        public List<MyObj> MyProperty { get; set; }

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            return new ExecuteResult();
        }
        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
    public class MyObj : ObjectPropertyBase
    {
        public string Name { get; set; }
        public string Description { get; set; }
    }
}
```

在设计器中效果如下：

列表项目的子属性也可以通过标注来控制属性编辑控件。
下面例子中，额外声明了两个属性分别使用公式编辑器和命令编辑器。具体标注的用法请参考之前的章节。

```csharp
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [ListProperty]
        public List<MyObj> MyProperty { get; set; }

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            return new ExecuteResult();
        }
        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
    public class MyObj : ObjectPropertyBase
    {
        public string Name { get; set; }

        [FormulaProperty]
        public object FormulaProperty { get; set; }

        [ComboProperty(ValueList = "选项1|选项2|选项3")]
        public string Type { get; set; }
    }
```

在设计器中效果如下：

如果需要更细致的控制，可以通过ListPropertyAttribute的其他属性来控制。
**1.控制列表最大或最小元素个数。**

1. 设置ListPropertyAttribute 的 MaxCount 和 MinCount 属性。
2. 代码：

    ```auto
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [ListProperty(MaxCount = 5, MinCount = 1)]
            public List<MyObj> MyProperty { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                return new ExecuteResult();
            }
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
        public class MyObj : ObjectPropertyBase
        {
            public string Name { get; set; }
            public string Description { get; set; }
        }
    ```

**2.指定属性的默认值。**

1. <span class="ne-text">给属性添加ListPropertyItemSettingAttribute 的 DefaultName 属性。</span>
2. <span class="ne-text">代码如下：</span>

    ```csharp
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [ListProperty]
            public List<MyObj> MyProperty { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                return new ExecuteResult();
            }
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    
        public class MyObj : ObjectPropertyBase
        {
            [ListPropertyItemSetting(DefaultName = "Node")]
            public string Name { get; set; }
            public string Description { get; set; }
        }
    ```
3. 设计器中的效果：
    
4. 此特性为10.0.0.0版本新增的特性。

**3.指定属性的默认列宽。**

1. <span class="ne-text">给属性添加ListPropertyItemSettingAttribute 的 DefaultWidth 属性（列表属性的默认列宽为150个像素）。</span>
2. <span class="ne-text">代码如下：</span>

    ```csharp
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [ListProperty]
            public List<MyObj> MyProperty { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                return new ExecuteResult();
            }
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    
        public class MyObj : ObjectPropertyBase
        {
            [ListPropertyItemSetting(DefaultWidth = 250)]
            public string Name { get; set; }
            public string Description { get; set; }
        }
    ```
3. 设计器中的效果：
    
4. 此特性为10.0.0.0版本新增的特性。

**4.指定属性值不可重复。**

1. <span class="ne-text"> 给属性添加ListPropertyItemSettingAttribute 的 IsUnique 属性。</span>
2. <span class="ne-text">代码如下：</span>

    ```csharp
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [ListProperty]
            public List<MyObj> MyProperty { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                return new ExecuteResult();
            }
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    
        public class MyObj : ObjectPropertyBase
        {
            [ListPropertyItemSetting(IsUnique = true)]
            public string Name { get; set; }
            public string Description { get; set; }
        }
    ```
3. 设计器中的效果：
    
4. 此特性为10.0.0.0版本新增的特性。

**5.内嵌显示。**

1. <span class="ne-text">通过标注 FlatListPropertyAttribute 可以让列表在属性面板中内嵌显示。</span>
2. <span class="ne-text">代码如下：</span>

    ```auto
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [FlatListProperty]
            public List<MyObj> MyProperty { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                return new ExecuteResult();
            }
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    
        public class MyObj : ObjectPropertyBase
        {
            public string Name { get; set; }
            public string Description { get; set; }
        }
    ```
3. 设计器中的效果：
    
4. 此特性为10.0.0.0版本新增的特性。

---

## Objectlistproperty

# 对象列表属性

## Content

如果一个属性的类型是List类型，List的每一项又包含了子属性，那么可以通过标注ObjectListPropertyAttribute，使得活字格设计器可以通过弹出二级对话框来编辑该属性。
注意：

1. ItemType属性里声明的类型必须与项目属性类型一致。
2. 自定义对象必须实现 INamedObject 接口。
3. 属性的返回值必须是 List。
4. 自定义对象的类型应该从 ObjectPropertyBase 类派生，以确保在单元格复制的时候，子属性可以被正确的深克隆（ObjectPropertyBase实现了默认的深克隆逻辑）。

```
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [ObjectListProperty(ItemType = typeof(MyObj))]
        public List<INamedObject> MyProperty { get; set; } = new List<INamedObject>();

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            return new ExecuteResult();
        }
        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
    public class MyObj : ObjectPropertyBase, INamedObject
    {
        public string Name { get; set; }
        public string SubProperty1 { get; set; }
        public string SubProperty2 { get; set; }
        public string SubProperty3 { get; set; }
        public string SubProperty4 { get; set; }
    }
```

在设计器中效果如下：

列表项目的子属性也可以通过标注来控制属性编辑控件。
下面例子中，额外声明了两个属性分别使用公式编辑器和命令编辑器。具体标注的用法请参考之前的章节。

```
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [ObjectListProperty(ItemType = typeof(MyObj))]
        public List<INamedObject> MyProperty { get; set; } = new List<INamedObject>();

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            return new ExecuteResult();
        }
        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
    public class MyObj : ObjectPropertyBase, INamedObject
    {
        public string Name { get; set; }
        public string Description { get; set; }

        [FormulaProperty]
        public object FormulaProperty { get; set; }

        [ComboProperty(ValueList = "选项1|选项2|选项3")]
        public string Type { get; set; }
    }
```

在设计器中效果如下：

如果需要更细致的控制，可以通过ObjectListPropertyAttribute的其他属性来控制
**控制列表最大元素个数**

1. 设置ObjectListPropertyAttribute 的 MaxCount 属性。
2. 代码：

    ```
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [ObjectListProperty(ItemType = typeof(MyObj), MaxCount = 4)]
            public List<INamedObject> MyProperty { get; set; } = new List<INamedObject>();
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                return new ExecuteResult();
            }
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
        public class MyObj : ObjectPropertyBase, INamedObject
        {
            public string Name { get; set; }
            public string SubProperty1 { get; set; }
            public string SubProperty2 { get; set; }
            public string SubProperty3 { get; set; }
            public string SubProperty4 { get; set; }
        }
    ```

**控制默认结点名称**

1. 设置ObjectListPropertyAttribute 的 DefaultName 属性。
2. 代码：

    ```
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [ObjectListProperty(ItemType = typeof(MyObj), DefaultName = "结点")]
            public List<INamedObject> MyProperty { get; set; } = new List<INamedObject>();
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                return new ExecuteResult();
            }
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
        public class MyObj : ObjectPropertyBase, INamedObject
        {
            public string Name { get; set; }
            public string SubProperty1 { get; set; }
            public string SubProperty2 { get; set; }
            public string SubProperty3 { get; set; }
            public string SubProperty4 { get; set; }
        }
    ```

### ListProperty Vs ObjectListProperty

ListPropertyAttribute和ObjectListPropertyAttribute解决的是完全相同的问题，只是表现方式不同，ObjectListPropertyAttribute 更适合项目子属性比较多的情况，而ListProperty则在子属性比较少的时候比较适用。

---

## Objectproperty

# 对象属性

## Content

默认情况下，如果一个属性的类型是对象类型，这个类型又包含了一些子属性，那么可以通过标注ObjectPropertyAttribute，使得活字格设计器可以通过弹出二级对话框来编辑该属性。
注意，ObjType属性里声明的类型必须与属性类型一致。
自定义对象的类型应该从 ObjectPropertyBase 类派生，以确保在单元格复制的时候，子属性可以被正确的深克隆（ObjectPropertyBase实现了默认的深克隆逻辑）。

```csharp
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [ObjectProperty(ObjType = typeof(MyObj))]
        public MyObj MyProperty { get; set; }

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            return new ExecuteResult();
        }
        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
    public class MyObj : ObjectPropertyBase
    {
        public string Name { get; set; }
        public string Description { get; set; }
    }
}
```

在设计器中效果如下：

对象的子属性也可以通过标注来控制属性编辑控件。
下面例子中，额外声明了一个属性使用公式编辑器。具体标注的用法请参考之前的章节。

```csharp
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [ObjectProperty(ObjType = typeof(MyObj))]
        public MyObj MyProperty { get; set; }

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            return new ExecuteResult();
        }
        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
    public class MyObj : ObjectPropertyBase
    {
        public string Name { get; set; }
        public string Description { get; set; }

        [FormulaProperty]
        public object FormulaProperty { get; set; }
    }
```

在设计器中效果如下：

#### 高级配置

**1.添加描述。**

1. <span class="ne-text">设置 DescriptionAttribute。</span>
2. <span class="ne-text">代码如下：</span>

    ```auto
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [ObjectProperty(ObjType=typeof(MyObj))]
            public MyObj MyProperty { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                return new ExecuteResult();
            }
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    
        [Description("* 添加一段描述文字，帮助使用者更好的理解这个对象的设置，如果描述文字很长，会自动折行，所以不用担心长度限制")]
        public class MyObj: ObjectPropertyBase
        {
            public string Name { get; set; }
            public string Description { get; set; }
    
            [FormulaProperty]
            public object FormulaProperty { get; set; }
    
            [CustomCommandObject]
            [DisplayName("点击命令")]
            public object ClickCommand { get; set; }
        }
    ```
3. 设计器中的效果：
    
4. 此特性为10.0.0.0版本新增的特性。

**2.给对象添加自定义校验。**

1. <span class="ne-text">给属性添加DesignerAttribute 重写Validate方法添加自定义校验。</span>
2. <span class="ne-text">代码如下：</span>

    ```auto
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [ObjectProperty(ObjType = typeof(MyObj))]
            public MyObj MyProperty { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                return new ExecuteResult();
            }
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
        [Designer(typeof(MyObjectDesigner))]
        public class MyObj : ObjectPropertyBase
        {
            [Required]
            public string Name { get; set; }
            public string Description { get; set; }
    
            [FormulaProperty]
            public object FormulaProperty { get; set; }
    
            [CustomCommandObject]
            [DisplayName("点击命令")]
            public object ClickCommand { get; set; }
        }
    
        public class MyObjectDesigner : ObjectDesigner
        {
            public override string Validate()
            {
                if (this.Obj is MyObj myObj)
                {
                    if (myObj.FormulaProperty == null && myObj.Description == null)
                    {
                        return "FormulaProperty 和 Description 属性至少有一个不能为空";
                    }
                }
                return base.Validate();
            }
        }
    ```
3. 设计器中的效果：
    
4. 此特性为10.0.0.0版本新增的特性。

**3.内嵌显示。**

1. <span class="ne-text"> 给对象标注 FlatObjectProperty 可以实现对象的内嵌显示。</span>
2. <span class="ne-text">代码如下：</span>

    ```auto
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [DisplayName("姓名")]
            public string Name { get; set; }
    
            [FlatObjectProperty]
            [DisplayName("地址")]
            public Address Address { get; set; } = new Address();
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                return new ExecuteResult();
            }
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    
        public class Address : ObjectPropertyBase
        {
            [DisplayName("省份")]
            public string Province { get; set; }
            [DisplayName("城市")]
            public string City { get; set; }
        }
    ```
3. 设计器中的效果：
    

**4.内嵌显示联动。**

1. <span class="ne-text">给对象标注 FlatObjectProperty 实现子对象属性内嵌显示，同时通过</span>[<span class="ne-text">属性值联动</span>](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developservercommandplugin/supportcommanddesigntime/Attribute-value-linkage)<span class="ne-text">在不同情况下显示不同的子属性。</span>
2. <span class="ne-text">代码如下：</span>

    ```csharp
        [Designer(typeof(MyCommandDesigner))]
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [ComboProperty(ValueList = "Type1|Type2")]
            public string Type { get; set; } = "Type1";
    
            [FlatObjectProperty]
            public object SubProperty { get; set; } = new Type1SubProperty();
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                return new ExecuteResult();
            }
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
        public class Type1SubProperty : ObjectPropertyBase
        {
            public string SubProperty1 { get; set; }
        }
        public class Type2SubProperty : ObjectPropertyBase
        {
            public string SubProperty2 { get; set; }
            [ColorProperty]
            public string SubProperty3 { get; set; }
        }
        public class MyCommandDesigner : CommandDesigner
        {
            public override void OnPropertyEditorChanged(string propertyName, object propertyValue, Dictionary<string, IEditorSettingsDataContext> properties)
            {
                if (propertyName == nameof(MyPluginCommand.Type))
                {
                    if (Equals(propertyValue, "Type1"))
                    {
                        properties[nameof(MyPluginCommand.SubProperty)].Value = new Type1SubProperty();
                    }
                    else
                    {
                        properties[nameof(MyPluginCommand.SubProperty)].Value = new Type2SubProperty();
                    }
                }
                base.OnPropertyEditorChanged(propertyName, propertyValue, properties);
            }
        }
    ```
3. 设计器中的效果：
    

**5.属性变更联动。**

1. <span class="ne-text">所有继承自 ObjectPropertyBase 的对象都可以在类型声明时标注 [DesignerAttribute] 特性，可以达到对象内的属性变化联动。</span>
2. 此功能同时支持 ObjectProperty、FlatObjectProperty、ObjectListProperty、ListProperty 以及 FlatListProperty。
3. <span class="ne-text">下面的示例代码中， MyObject 对象拥有两个属性，当用户编辑 Data1 时，Data2 将改变，值为“Data1 + 1”。</span>

    ```csharp
      public class TestServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [ObjectProperty(ObjType = typeof(MyObject))]
        public MyObject MyObject1 { get; set; }
    
        [FlatObjectProperty]
        public MyObject MyObject2 { get; set; } = new MyObject();
    
        [ObjectListProperty(ItemType = typeof(MyObject))]
        public List<INamedObject> MyObject3 { get; set; } = new List<INamedObject>();
    
        [ListProperty]
        public List<MyObject> MyObject4 { get; set; } = new List<MyObject>();
    
        [FlatListProperty]
        public List<MyObject> MyObject5 { get; set; } = new List<MyObject>();
    
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            return new ExecuteResult();
        }
        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
    
    [Designer(typeof(MyObjectDesigner))]
    public class MyObject : ObjectPropertyBase, INamedObject
    {
        [Browsable(false)]
        public string Name { get; set; }
    
        public int Data1 { get; set; }
    
        public int Data2 { get; set; }
    }
    
    public class MyObjectDesigner : ObjectDesigner
    {
        public override void OnPropertyEditorChanged(string propertyName, object propertyValue, Dictionary<string, IEditorSettingsDataContext> properties)
        {
            if (propertyName == nameof(MyObject.Data1))
            {
                properties[nameof(MyObject.Data2)].Value = (int)propertyValue + 1;
            }
            base.OnPropertyEditorChanged(propertyName, propertyValue, properties);
        }
    }
    ```
4. 设计器中的效果：
    
5. 此特性为 10.0.100.0 版本新增的特性。

---

## Radioproperty

# 单选框  属性

## Content

如果属性的类型是字符串，默认属性值是可以接受任意字符串的，如果希望提供字符串值候选列表，可以通过标注RadioGroupProperty 的并设置ValueList属性的方式实现单选框候选列表。多个值用“\|”分隔。
RadioGroupProperty和ComboProperty的使用方式非常类似，主要是在设计器中的UI表现不同。
注意，标注RadioGroupProperty的属性类型必须是 string。

```
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [RadioGroupProperty(ValueList = "Student|Teacher|Worker")]
        public string MyProperty { get; set; }

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            return new ExecuteResult();
        }
        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
```

在设计器中效果如下：

如果需要更细致的控制，可以通过RadioGroupProperty的其他属性来控制。
**值与显示值不同**

1. 设置RadioGroupProperty的 DisplayList 属性。
2. 代码：

    ```
        public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
        {
            [RadioGroupProperty(ValueList = "Student|Teacher|Worker", DisplayList = "学生|教师|工人")]
            public string MyProperty { get; set; }
    
            public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
            {
                return new ExecuteResult();
            }
            public override CommandScope GetCommandScope()
            {
                return CommandScope.ExecutableInServer;
            }
        }
    ```
3. 效果：
    
4. 其他说明：
    此方法可以使用户在选择时选择中文选项，而单元格实际保存值为英文，方便程序处理。ValueList和DisplayList通过数量和顺序匹配。如果DisplayList数量超出ValueList数量，多出部分会被忽略；如果DisplayList数量少于ValueList数量，不足部分会使用ValueList对应的值。

---

## Servercommandnameproperty

# 服务端命令选择属性

## Content

此特性为活字格V9.1新增功能。
在服务端命令中通过名字调用另一个服务端命令。

```auto
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [ServerCommandNameProperty]
        public string MyServerCommandName { get; set; }

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            await dataContext.ExecuteServerCommandsAsync(this.MyServerCommandName, dataContext);
            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
```

在设计器中效果如下：

注意：标注ServerCommandNameProperty的属性类型必须是 string。

---

## Databaseinteraction

# 数据库交互

## Content

在服务端命令中，可以通过 dataContext.DataAccess 属性对数据库进行增删改查。
本例中使用的示例数据库如下：

### **获取数据示例代码**

参数为OData字符串：

```
using GrapeCity.Forguncy.Commands;
using Newtonsoft.Json;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            var data = dataContext.DataAccess.GetTableData("表1?$select=ID,字段1,小数");

            return new ExecuteResult() { Message = JsonConvert.SerializeObject(data) };
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

效果如下：

### 新增数据示例代码

```
using GrapeCity.Forguncy.Commands;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            dataContext.DataAccess.AddTableData("表1", new Dictionary<string, object>
            {
                {"字段1", "xxx" },
                {"小数", "1.5" }
            });

            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

执行结果：

### 删除数据示例代码

```
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.ServerApi;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            dataContext.DataAccess.DeleteTableData("表1", new ColumnValuePair()
            {
                ColumnName = "ID",
                Value = 2
            });

            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

执行结果：

### 更新数据示例代码

```
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.ServerApi;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            dataContext.DataAccess.UpdateTableData("表1", new ColumnValuePair()
            {
                ColumnName = "ID",
                Value = 2
            },
            new Dictionary<string, object>()
            {
                {"字段1", "xxx" },
                {"小数", "1.5" }
            });

            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

执行结果：