# Other Functions

## Commandlog

# 命令日志

## Content

插件命令也可以和其他内置命令一样输出日志，方便命令逻辑的调试。

JavaScript 代码如下，log方法可以输出自定义日志。

```
class MyPluginCommand extends Forguncy.Plugin.CommandBase{
    execute() {
        let text = this.CommandParam.MyProperty; 

        this.log("这里是命令日志，MyProperty属性值：" + text)

        alert(text);
    }
}

Forguncy.Plugin.CommandFactory.registerCommand("MyPlugin.MyPluginCommand, MyPlugin", MyPluginCommand);
```

  

效果：

---

## Supportasyncommands

# 支持异步命令

## Content

命令执行过程中可能要发送网络请求等异步操作，而后续命令希望在异步操作完成后执行。

1.通过 async await 方法实现。

```
class MyPluginCommand extends Forguncy.Plugin.CommandBase{
    async execute() {
        const response = await fetch("http://urlYouWhatToAccess/");
        const resultText = await response.text();
        console.log(resultText);
    }
}

Forguncy.Plugin.CommandFactory.registerCommand("MyPlugin.MyPluginCommand, MyPlugin", MyPluginCommand);
```

2.通过构建Promise对象实现。

```
class MyPluginCommand extends Forguncy.Plugin.CommandBase{
    execute() {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                this.log("异步方法被执行,之后会执行后续逻辑");
                resolve();
            }, 3000);
        });
    }
}

Forguncy.Plugin.CommandFactory.registerCommand("MyPlugin.MyPluginCommand, MyPlugin", MyPluginCommand);
```

---

## Supportreturnedresults

# 支持返回结果

## Content

命令执行后，可以把命令的执行结果保持到变量里，以便后续的命令或逻辑使用。
可以通过实现ResultToPropertyAttribute来实现此效果。
示例代码：
注意：标注 ResultToProperty 的属性类型必须是 string。 推荐给属性添加默认值，以方便用户使用。

```auto
    public class MyPluginCommand : Command
    {
        [DisplayName("加数")]
        [FormulaProperty]
        public object FirstValue { get; set; }

        [DisplayName("被加数")]
        [FormulaProperty]
        public object LastValue { get; set; }

        [ResultToProperty]
        [DisplayName("结果保存至变量")]
        public string Result { get; set; } = "结果";
    }
```

设计器中的效果：

在后续命令编辑公式时，设置的变量可以直接在公式中使用。

在JavaScript 部分，通过Forguncy.CommandHelper.setVariableValue方法设置结果到结果变量。

```auto
class MyPluginCommand extends Forguncy.Plugin.CommandBase{
    execute() {
        const add1 = this.evaluateFormula(this.CommandParam.FirstValue);
        const add2 = this.evaluateFormula(this.CommandParam.LastValue);
        const res = Number(add1) + Number(add2);
        Forguncy.CommandHelper.setVariableValue(this.CommandParam.Result, res);
    }
}

Forguncy.Plugin.CommandFactory.registerCommand("MyPlugin.MyPluginCommand, MyPlugin", MyPluginCommand);
```

#### 把返回结果设置到单元格上

通过标注[FormulaProperty(OnlySupportNormalCell = true)] 可以让属性只能选择一个单元格。

```csharp
    public class MyPluginCommand : Command
    {
        [DisplayName("加数")]
        [FormulaProperty]
        public object FirstValue { get; set; }

        [DisplayName("被加数")]
        [FormulaProperty]
        public object LastValue { get; set; }

        [FormulaProperty(OnlySupportNormalCell = true)]
        [DisplayName("结果保存至单元格")]
        public object Result { get; set; } = "结果";
    }
```

设计器中的效果：

在JavaScript 部分，通过setValue方法设置单元的值。

```javascript
class MyPluginCommand extends Forguncy.Plugin.CommandBase {
    execute() {
        const add1 = this.evaluateFormula(this.CommandParam.FirstValue);
        const add2 = this.evaluateFormula(this.CommandParam.LastValue);
        const res = Number(add1) + Number(add2);
        const location = Forguncy.Helper.getCellLocation(this.CommandParam.Result, this.getFormulaCalcContext());
        Forguncy.Page.getCellByLocation(location).setValue(res);
    }
}
Forguncy.Plugin.CommandFactory.registerCommand("MyPlugin.MyPluginCommand, MyPlugin", MyPluginCommand);
```

#### 强制给结果单元格生成Dom

使用以上代码可以把命令执行结果设置到单元格上。不过有一个前提，单元格必须有对应的Dom来展示单元格的值。默认情况下，活字格是不会给空白单元格生成Dom的，如果用户选择了空白单元格来接受命令结果会导致结果无法显示。为了解决这个问题，可以通过实现 IForceGenerateCell 接口告诉活字格强制生成 Dom。

```csharp
    public class MyPluginCommand : Command, IForceGenerateCell
    {
        [DisplayName("加数")]
        [FormulaProperty]
        public object FirstValue { get; set; }

        [DisplayName("被加数")]
        [FormulaProperty]
        public object LastValue { get; set; }

        [FormulaProperty(OnlySupportNormalCell = true)]
        [DisplayName("结果保存至单元格")]
        public object Result { get; set; } = "结果";

        public IEnumerable<GenerateCellInfo> GetForceGenerateCells()
        {
            if (Result is IFormulaReferObject targetReferObject)
            {
                var cellInfo = targetReferObject.GetGenerateCellInfo();
                if (cellInfo != null)
                {
                    yield return cellInfo;
                }
            }
        }
    }
```

---

## Supportsstructuretypereturnresults

# 支持结构类型的返回结果

## Content

<span class="ne-text">从上一节</span>[支持返回结果](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/otherfunctions/supportreturnedresults)<span class="ne-text">中，我们已经了解到，通过给属性标注ResultToPropertyAttribute，可以在命令执行后生成一个或多个返回结果，以便后续命令使用。</span>
<span class="ne-text">如果希望生成复杂的对象类型返回结果，或者生成数组类型的返回结果，通过标注ResultToPropertyAttribute，也是可以实现的。但是再后续的属性提示中，用户无法快捷的了解返回的对象有哪些子属性。只能通过点操作符硬取值。</span>
<span class="ne-text">例如以下代码：</span>

```csharp
using GrapeCity.Forguncy.Commands;
using System.ComponentModel;

namespace MyPlugin
{
    public class MyPluginCommand : Command
    {
        [ResultToProperty]
        [DisplayName("学生信息")]
        public string StudentInfo { get; set; }
    }
}
```

### <span class="ne-text">对象类型返回值</span>

<span class="ne-text">假设命令执行后，返回学生对象，包含姓名和年龄属性。但是再后续命令使用结果时只会提示学生信息变量，而如果需要获取子属性值，必须用户手动准确输入，用户体验较差。</span>

<span class="ne-text">如果希望同时提示子属性，可以通过实现 IServerCommandParamGenerator 接口实现。</span>

```csharp
using GrapeCity.Forguncy.Commands;
using System.Collections.Generic;
using System.ComponentModel;

namespace MyPlugin
{
    public class MyPluginCommand : Command, IServerCommandParamGenerator
    {
        [ResultToProperty]
        [DisplayName("学生信息")]
        public string StudentInfo { get; set; }

        public IEnumerable<GenerateParam> GetGenerateParams()
        {
            yield return new GenerateObjectParam()
            {
                ParamName = this.StudentInfo,
                Description = "查询学生的详细信息结果",
                ParamScope = CommandScope.All,
                SubPropertiesDescription = new Dictionary<string, string>() {
                    { "Name","学生姓名"},
                    { "Age","学生年龄"},
                    { "Address.Country","住址（国家）"},
                    { "Address.City","住址（城市）"}
                }
            };
        }
    }
}
```

<span class="ne-text">效果如下：</span>

### <span class="ne-text">数组类型返回值</span>

<span class="ne-text">如果返回值是列表类型，同样可以通过实现IServerCommandParamGenerator解决。</span>

```csharp
using GrapeCity.Forguncy.Commands;
using System.Collections.Generic;
using System.ComponentModel;

namespace MyPlugin
{
    public class MyPluginCommand : Command, IServerCommandParamGenerator
    {
        [ResultToProperty]
        [DisplayName("学生信息")]
        public string StudentInfo { get; set; }

        public IEnumerable<GenerateParam> GetGenerateParams()
        {
            yield return new GenerateListParam()
            {
                ParamName = this.StudentInfo,
                Description = "查询学生结果列表",
                ParamScope = CommandScope.All,
                ItemProperties = new List<string>() {
                    { "Name"},
                    { "Age"},
                    { "Address.Country"},
                    { "Address.City"}
                }
            };
        }
    }
}
```

<span class="ne-text">效果如下。</span>
<span class="ne-text">在普通命令中使用时：</span>

<span class="ne-text">在循环命令的子命令中使用时：</span>

### <span class="ne-text">数组与对象嵌套混合类型返回值</span>

<span class="ne-text">如果返回值是列表或对象多级嵌套的复杂类型，同样可以通过实现IServerCommandParamGenerator解决，需要使用 GenerateObjectParam 类型的 SubGenerateProperties 属性和 GenerateListParam 的 ItemGenerateProperties 属性。</span>

>type=note
> **说明：**
> <span class="ne-text">多级混合嵌套特性为 V11.0.100.0 新增特性。</span>

```javascript
using GrapeCity.Forguncy.Commands;
using System.Collections.Generic;
using System.ComponentModel;

namespace MyPlugin
{
    public class MyPluginCommand : Command, IServerCommandParamGenerator
    {
        [ResultToProperty]
        [DisplayName("学生信息")]
        public string StudentInfo { get; set; }

        public IEnumerable<GenerateParam> GetGenerateParams()
        {
            yield return new GenerateObjectParam()
            {
                ParamName = this.StudentInfo,
                ParamScope = CommandScope.All,
                SubGenerateProperties = new List<GenerateParam>()
                {
                    new GenerateNormalParam("姓名", "学生姓名"),
                    new GenerateNormalParam("年龄", "学生年龄"),
                    new GenerateListParam("更新历史", "更新历史记录")
                    {
                        ItemGenerateProperties = new List<GenerateParam>()
                        {
                            new GenerateNormalParam("日期", "更新日期"),
                            new GenerateNormalParam("更新人", "更新人")
                        }
                    },
                    new GenerateObjectParam("地址", "地址信息")
                    {
                        SubGenerateProperties = new List<GenerateParam>()
                        {
                            new GenerateNormalParam("国家", "国家"),
                            new GenerateNormalParam("省", "省份"),
                            new GenerateNormalParam("市", "城市"),
                            new GenerateNormalParam("街道", "街道")
                        }
                    }
                 }
            };
        }
    }
}
```

<span class="ne-text">可以看到二级属性地址，下的有三级属性省，市等，效果如下：</span>

<span class="ne-text">此时，如果在循环命令中循环 “学生信息.更新历史”可以在 更新项目 中使用列表的二级属性“日期”“更新人”。</span>