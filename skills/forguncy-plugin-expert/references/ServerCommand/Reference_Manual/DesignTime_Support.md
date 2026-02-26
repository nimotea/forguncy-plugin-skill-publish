# DesignTime Support

## Supportcommanddesigntime

# 命令设计时支持

## Content

* [自定义命令编辑器](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developservercommandplugin/supportcommanddesigntime/customcommandeditor)
* [属性校验](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developservercommandplugin/supportcommanddesigntime/attributeverification)
* [高级自定义校验](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developservercommandplugin/supportcommanddesigntime/Advanced-custom-validation)
* [动态隐藏属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developservercommandplugin/supportcommanddesigntime/dynamichiddenproperties)
* [命令的分组与排序](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developservercommandplugin/supportcommanddesigntime/commandgroupingandsorting)
* [给命令属性添加说明](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developservercommandplugin/supportcommanddesigntime/adddescriptionstocommandproperties)
* [给命令添加说明](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developservercommandplugin/supportcommanddesigntime/adddescriptiontocommand)
* [属性值联动](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developservercommandplugin/supportcommanddesigntime/Attribute-value-linkage)
* [折叠高级属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developservercommandplugin/supportcommanddesigntime/collapse-advanced-properties)

---

## AdvancedCustomValidation

# 高级自定义校验

## Content

在[属性校验](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developservercommandplugin/supportcommanddesigntime/attributeverification)章节中，我们可以通过标注一些Attribute实现简单的设计时校验逻辑。但是，有时校验逻辑会相对复杂，如几个属性间相互作用下的校验逻辑。相对复杂的校验逻辑要如何实现呢？
例如，有一个命令，有两个数字类型的属性，代码如下：

```auto
    [Designer("MyPlugin.Designer.MyPluginServerCommandDesigner, MyPlugin")]
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        public int MyProperty { get; set; }
        public int MyProperty1 { get; set; }

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

## 编辑命令时校验

如果校验逻辑要求，MyProperty 与 MyProperty1 的和必须大于100,可以重写 CommandDesigner 的 Validate 方法。 这个方法如果返回一个不为Null的字符串，表示校验失败，并且会在命令对话框中弹出错误提示。

```csharp
    public class MyPluginServerCommandDesigner : CommandDesigner<MyPluginServerCommand>
    {
        public override string Validate()
        {
            if (this.Command.MyProperty + this.Command.MyProperty1 < 100)
            {
                return "MyProperty 与 MyProperty1 的和必须大于 100";
            }
            return base.Validate();
        }
    }
```

设计器效果如下：

## 生成工程时校验时校验

如果校验逻辑要求，MyProperty 与 MyProperty1 的和必须大于100。如果小于100，应该给用户提出警告；如果小于10 ，则应该提示错误。这是一个相对复杂的校验逻辑，没有办法通过标注 Attribute 实现，只能通过代码逻辑来实现。实现的方式是让 CommandDesigner 实现 ICommandChecker接口。代码如下：

```auto
    public class MyPluginServerCommandDesigner : CommandDesigner<MyPluginServerCommand>, ICommandChecker
    {
        public IEnumerable<ForguncyErrorInfo> CheckCommandErrors(IBuilderCommandContext context)
        {
            if (this.Command.MyProperty + this.Command.MyProperty1 <= 10)
            {
                yield return new ForguncyErrorInfo()
                {
                    ErrorType = ForguncyErrorType.Error,
                    Message = "MyProperty 与 MyProperty1 的和不能小于等于 10"
                };
            }
            else if (this.Command.MyProperty + this.Command.MyProperty1 < 100)
            {
                yield return new ForguncyErrorInfo()
                {
                    ErrorType = ForguncyErrorType.Warning,
                    Message = "MyProperty 与 MyProperty1 的和小于 100 的设置是不合理的，请考虑修改"
                };
            }
        }
    }
```

效果：

* 当命令的设置为两个属性值的和大于等于 100 时，活字格不会报错；
* 当命令的设置为两个属性值的和在 10 到 99 之间时，活字格在运行时会产生一个警告；
    
* 当命令的设置为两个属性值的和小于 10 时，活字格在运行时会产生一个错误，并且不会运行应用程序。
    

>type=note
> 注意：
> 校验逻辑会在每次活字格生成工程时都会被触发。开发者应该尽量保证校验逻辑高效进行，避免IO、网络访问、大量循环等慢操作，导致活字格生成效率降低。

---

## AttributeValueLinkage

# 属性值联动

## Content

在设计器中，如果一个属性的值希望在另一个属性值变化时自动随之变化，可以通过在XXXDesigner.cs 类中重写 OnPropertyEditorChanged 方法来实现。
下面例子中假设命令上有两个属性，分别是MyProperty1和MyProperty2，实现的联动效果为 MyProperty1 的值为 true 时， 修改 MyProperty2 值为真， 否则，修改MyProperty2 值为假。
在 MyPluginServerCommand.cs 修改代码如下：

```csharp
using GrapeCity.Forguncy.Commands;
using System.ComponentModel;
using System.Threading.Tasks;

namespace MyPlugin
{
    [Designer("MyPlugin.Designer.MyPluginServerCommandDesigner, MyPlugin")]
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        public bool MyProperty1 { get; set; }

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
}
```

在 MyPluginServerCommandDesigner.cs 修改代码如下：

```csharp
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;
using System;
using System.Collections.Generic;

namespace MyPlugin.Designer
{
    public class MyPluginServerCommandDesigner : CommandDesigner<MyPluginServerCommand>
    {
        public override void OnPropertyEditorChanged(string propertyName, object propertyValue, Dictionary<string, IEditorSettingsDataContext> properties)
        {
            if (propertyName == nameof(MyPluginCellType.MyProperty1))
            {
                var property2Setting = properties[nameof(MyPluginCellType.MyProperty2)];
                if (object.Equals(propertyValue, true))
                {
                    property2Setting.Value = "真";
                }
                else
                {
                    property2Setting.Value = "假";
                }
            }
            base.OnPropertyEditorChanged(propertyName, propertyValue, properties);
        }
    }
}
```

代码说明：
OnPropertyEditorChanged 函数会在命令的任何属性被修改时被调用。可以通过参数 propertyName 判断当前被修改的属性名， 通过参数 propertyValue 获取最新被修改的值。properties 属性中包含了全部属性列。可以通过操作 properties 里的特定属性实现联动效果。
设计器中的效果：
.7da8fa.gif)

---

## Commandgroupingandsorting

# 命令的分组与排序

## Content

默认情况下，命令的分组是其他。

可以通过标注CategoryAttribute来自定义分组。

```
    [Category("我的分组")]
    public class MyPluginCommand : Command
    {
    }
```

效果如下：

如果分组名与既有的分组名一致，会加到已有的组里。

```
    [Category("数据库")]
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
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

效果如下：

如果有多个插件，在同一分组，可以通过OrderWeightAttribute标注排序权重。

```
    [OrderWeight(1)]
    [Category("我的分组")]
    public class MyPluginServerCommand1 : Command, ICommandExecutableInServerSideAsync
    {
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            return new ExecuteResult();
        }
        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
    [OrderWeight(2)]
    [Category("我的分组")]
    public class MyPluginServerCommand2 : Command, ICommandExecutableInServerSideAsync
    {
        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            return new ExecuteResult();
        }
        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
    [OrderWeight(3)]
    [Category("我的分组")]
    public class MyPluginServerCommand3 : Command, ICommandExecutableInServerSideAsync
    {
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

设计器效果：