# Properties Complex

## Asimplecommandplugin

# 一个简单的命令插件

## Content

开始本教程前，请确保已经仔细阅读了[快速开始](/solutions/huozige/help/docs/plugindevelopment/quickstart)章节，并已经完成了环境准备，并通过活字格插件构建器创建了默认工程。后续的文档都会基于活字格插件构建器创建的空白工程进行讲解。

  

现在，我们已经通过活字格插件构建工具开发了第一个命令插件，但是这个命令插件没有任何逻辑，我们需要编写C#和JavaScript代码来添加插件的业务逻辑。

首先，先查看代码结构。

修改单元格插件，我们重点关注两个文件：MyPluginCommand.cs 和 MyPluginCommand.js。

MyPluginCommand.cs 默认代码如下：

```
    [Icon("pack://application:,,,/MyPlugin;component/Resources/Icon.png")]
    [Designer("MyPlugin.Designer.MyPluginCommandDesigner, MyPlugin")]
    public class MyPluginCommand : Command
    {
        [DisplayName("命令属性")]
        [FormulaProperty]
        public object MyProperty { get; set; }

        public override string ToString()
        {
            return "我的插件命令";
        }
    }
```

1.  第一行代码 \[Icon("pack://application:,,,/MyPlugin;component/Resources/Icon.png")\] 用于指定图标文件的位置。
2.  第二行代码 \[Designer("MyPlugin.Designer.MyPluginCommandDesigner, MyPlugin")\] 用于指定设计时功能所在的类，刚开始开发插件时可以无视这句。
3.  第三行 public class MyPluginCommand : Command 用于定义命令类型，必须从 Command 类或其子类派生。
4.  第五行 public object MyProperty { get; set; } 定义了一个示例属性。
5.  第九行重写了 ToString() 方法指定了在设计器中命令显示的文本。

MyPluginCommand.js 默认代码如下：

```
/// <reference path="../Declarations/forguncy.d.ts" />
/// <reference path="../Declarations/forguncy.Plugin.d.ts" />
class MyPluginCommand extends Forguncy.Plugin.CommandBase{
    execute() {
        // 获取MyProperty属性值，注意，这里的MyProperty应该与 MyPluginCommand.cs 文件定义的属性名一致
        let text = this.CommandParam.MyProperty; 
        // MyProperty 属性的值可能是用户提供的公式，所以这里通过 evaluateFormula 方法计算出真实的值
        text = this.evaluateFormula(text);
        
        alert(text);
    }
}

Forguncy.Plugin.CommandFactory.registerCommand("MyPlugin.MyPluginCommand, MyPlugin", MyPluginCommand);
```

1.  第一行和第二行声明了活字格接口 ".d.ts" 文件的位置，以便在编写JavaScript代码时一个提供代码补全，提高开发效率。  
      
    
2.  第三行定义了 MyPluginCommand 类型，必须从 Forguncy.Plugin.CommandBase 派生。
3.  第4行到第11行重写了 execute 方法，获取自定义属性的值，通过evaluateFormula计算可能的公式结果，并通过 alert 方法在消息框中显示计算后的值。命令的执行逻辑都会写到这里。后续的教程中，主要是修改这个函数的实现来达成各种效果。
4.  第14行注册这个写的命令给活字格，这样活字格才知道有一个新的命令插件加入了。registerCommand方法的第一个参数格式： 【命令名字空间】.【命令名称】,【空格】【应用程序集名称】。

  

好，我们已经了解了命令插件的代码结构，让我们做一些小的修改来简单尝试一下开发一个命令插件吧。

比如，我们希望开发一个计算加法的命令。我们把 MyPluginCommand.cs 修改如下。

```
    public class MyPluginCommand : Command
    {
        [DisplayName("加数1")]
        [FormulaProperty]
        public object AddNumber1 { get; set; }

        [DisplayName("加数2")]
        [FormulaProperty]
        public object AddNumber2 { get; set; }

        public override string ToString()
        {
            return "我的加法命令";
        }
    }
```

MyPluginCellType.js 代码修改如下：

```
class MyPluginCommand extends Forguncy.Plugin.CommandBase{
    execute() {
        const add1Formula = this.CommandParam.AddNumber1; 
        const add2Formula = this.CommandParam.AddNumber2; 

        const add1 = this.evaluateFormula(add1Formula);
        const add2 = this.evaluateFormula(add2Formula);

        const result = Number(add1) + Number(add2);
        alert(add1 + "与" + add2 + "相加结果为" + result);
    }
}

Forguncy.Plugin.CommandFactory.registerCommand("MyPlugin.MyPluginCommand, MyPlugin", MyPluginCommand);
```

修改之后，编译代码，重启设计器。

在设计器中找到 “我的加法命令”命令插件，把命令添加到按钮命令上。我们可以看见在命令设置面板中多了2个设置，正好和C#代码中的2个属性对应。  
  

在页面上添加两个文本框，并通过公式设置命令的属性值与文本框绑定。

单击绿色开始按钮之后，在文本框中输入数字，单击按钮。

在单元格里设置不同的值，就可以计算不同数字的相加结果。

也许你还不理解这些代码的意思，没关系，后续的教程中对这些代码都会有详细的解释。

---

## Commandattributeindex

# 命令Attribute索引

## Content

自定义命令插件大量使用了各种Attribute来实现特定功能，此教程列举了所有的Attribute及功能简介备查

属性Attribute

| **Attribute** | **说明** | **详解** |
| --- | --- | --- |
| \[FormulaProperty\] | 标注为公式属性 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/addproperty/formulaproperty) |
| \[ResultToProperty\] | 标注为返回值属性 | [详情](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/otherfunctions/supportreturnedresults) |
| \[IntProperty\] | 标注为整数属性 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/addproperty/interproperty) |
| \[DoubleProperty\] | 标注为小数属性 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/addproperty/decimalproperty) |
| \[BoolProperty\] | 标注为布尔属性 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/addproperty/boolproperty) |
| \[ComboProperty\] | 标注为下拉列表属性 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/addproperty/comboproperty) |
| \[RadioGroupProperty\] | 标注为单选框属性 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/addproperty/radiogroupproperty) |
| \[ColorProperty\] | 标注为颜色属性 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/addproperty/colorproperty) |
| \[ImageValueProperty\] | 标注为图片属性 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/addproperty/imagevalueproperty) |
| \[CustomCommandObject\] | 标注为命令属性 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/addproperty/commandproperty) |
| \[ObjectProperty\] | 标注为对象属性 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/addproperty/objectproperty) |
| \[ListProperty\] | 标注为列表属性 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/addproperty/listproperty) |
| \[ObjectListProperty\] | 标注为对象列表属性 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/addproperty/objectlistproperty) |
| \[ListviewPropertyAttribute\] | 标注为表格名称列表属性 |     |
| \[ServerCommandNameProperty\] | 标注为服务端命令列表属性 |     |
| \[Browsable(false)\] | 标注属性在设计时不显示 |     |
| \[Description("描述")\] | 给属性添加说明 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/adddescriptionstocommandproperties) |
| \[DisplayName("我的属性")\] | 修改属性显示名 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/modifydisplaynameattribute) |
| \[DefaultValue\] | 标注属性的默认值 | [详解](/solutions/huozige/help/docs/plugindevelopment/faq/how-to-control-serialization-of-properties) |
| \[JsonIgnore\] | 控制属性是否保存或生成元数据 | [详解](/solutions/huozige/help/docs/plugindevelopment/faq/how-to-control-serialization-of-properties) |
| \[SaveJsonIgnore\] | 控制属性是否保存 | [详解](/solutions/huozige/help/docs/plugindevelopment/faq/how-to-control-serialization-of-properties) |
| \[PageMetadataJsonIgnore\] | 控制属性是否生成元数据 | [详解](/solutions/huozige/help/docs/plugindevelopment/faq/how-to-control-serialization-of-properties) |
| \[SearchableProperty\] | 标注属性可以被搜索 |     |

类 Attribute

| **Attribute** | **说明** | **详解** |
| --- | --- | --- |
| \[Category("我的分组")\] | 标注命令分组 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/commandgroupingandsorting) |
| \[OrderWeight(2)\] | 自定义命令在分组中的排序 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/commandgroupingandsorting) |
| \[Icon("IconUri")\] | 声明命令类型图标 | [详解](/solutions/huozige/help/docs/plugindevelopment/publish/iconanddescription/replacecellcommandicon) |
| \[Designer("DeisgnerFullName")\] | 声明设计器类 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/supportsdesigntimepreview) |
| \[SearchTagsAttribute\] | 指定搜索关键字 |     |
| \[CommandSupportUsingScopeAttribute\] | 标注命令可见范围 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/otherfunctions/setcommandvisibilityrange) |

枚举项目Attribute

| **Attribute** | **说明** | **详解** |
| --- | --- | --- |
| \[ItemDisplayName\] | 枚举项目显示名称 | [详解](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/addproperty/enumproperty) |

---

## Supportcommanddesigntime

# 命令设计时支持

## Content

*   [自定义命令编辑器](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/customcommandeditor)
*   [属性校验](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/attributeverification)
*   [动态 隐藏属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/dynamichiddenproperties)
*   [命令的分组与排序](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/commandgroupingandsorting)
*   [给命令属性添加说明](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/adddescriptionstocommandproperties)
*   [给命令添加说明](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/adddescriptiontocommand)

---

## Comboproperty

# 下拉列表属性

## Content

如果属性的类型是字符串，默认属性值是可以接受任意字符串的，如果希望提供字符串值候选列表，可以通过标注ComboPropertyAttribute 的并设置ValueList属性的方式实现。多值个值用“\|”分隔。
注意，标注ComboPropertyAttribute的属性类型必须是 string。

```auto
    public class MyPluginCommand : Command
    {
        [ComboProperty(ValueList = "Student|Teacher|Worker")]
        public string MyProperty { get; set; }
    }
```

在设计器中效果如下：

如果需要更细致的控制，可以通过ComboPropertyAttribute的其他属性来控制。
**1\. 值与显示值不同**

1. 设置ComboPropertyAttribute 的 DisplayList 属性。
2. 代码：

    ```auto
        public class MyPluginCommand : Command
        {
            [ComboProperty(ValueList = "Student|Teacher|Worker", DisplayList = "学生|教师|工人")]
            public string MyProperty { get; set; }
        }
    ```
3. 效果：
    
4. 其他说明
    此方法可以使用户在选择时选择中文选项，而单元格实际保存值为英文，方便程序处理。ValueList和DisplayList通过数量和顺序匹配。如果DisplayList数量超出ValueList数量，多出部分会被忽略；如果DisplayList数量少于ValueList数量，不足部分会使用ValueList对应的值。

**2\. 允许用户使用列表以外的值**

1. 设置ComboPropertyAttribute 的 IsSelectOnly属性。
2. 代码：

    ```auto
        public class MyPluginCommand : Command
        {
            [ComboProperty(ValueList = "Student|Teacher|Worker", IsSelectOnly = false)]
            public string MyProperty { get; set; }
        }
    ```
3. 效果：
    
4. 注意：
    IsSelectOnly 为 False 时，DisplayList 设置会被忽略；不填时 IsSelectOnly 属性的默认值为 True。

**3\. 支持搜索**

1. 设置ComboPropertyAttribute 的 Searchable 属性。
2. 代码：

    ```auto
        public class MyPluginCommand : Command
        {
            [ComboProperty(ValueList = "aa|bb|cc", Searchable = true)]
            public string MyProperty { get; set; }
    
            [ComboProperty(ValueList = "aa|bb|cc", Searchable = true, IsSelectOnly = false)]
            public string MyProperty2 { get; set; }
        }
    ```
3. 效果：
    
    
4. 策略：
    * <span class="ne-text">如果 IsSelectOnly 为 True ，则搜索框会在下拉框中。</span>
    * <span class="ne-text">如果 IsSelectOnly 为 False ，则可以直接输入，下拉框会自动按照输入的字符匹配。此模式下同样可以输入下拉框中不存在的字符串。</span>
    * <span class="ne-text">本特性要求活字格版本大于等于9.0.100.0。</span>

#### 动态下拉列表

有时，下拉列表中的选项不是开发时决定的，而是动态生成，例如下拉打印机列表。可以通过重写Command的Designer 通过代码动态生成列表。

```csharp
    [Designer("MyPlugin.Designer.MyPluginCommandDesigner, MyPlugin")]
    public class MyPluginCommand : Command
    {
        public string MyProperty { get; set; }
    }

    public class MyPluginCommandDesigner : CommandDesigner<MyPluginCommand>
    {
        public override EditorSetting GetEditorSetting(PropertyDescriptor property, IBuilderCommandContext builderContext)
        {
            if (property.Name == nameof(MyPluginCommand.MyProperty))
            {
                var list = new string[] { "aaa", "bbb", "ccc" };  // 代码动态生成
                return new ComboEditorSetting(list);
            }
            return base.GetEditorSetting(property, builderContext);
        }
    }
```

如果希望下拉列表的显示值和选择后保存的值不一样，可以如下修改 GetEditorSetting 方法，让List的每一项不是字符串，而是一个对象。通过设置 ComboEditorSetting 的 displayMember和valueMember来指定对象的哪个属性用于显示，哪个属性用于保存值。

```csharp
    public class MyPluginCommandDesigner : CommandDesigner<MyPluginCommand>
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

## Commandproperty

# 命令属性

## Content

在命令中包含另一个命令的情况并不常见，但是有些情况确实需要它。例如：

1. 执行命令的命令时弹出通知栏，点击通知栏的时候需要跳转到表单页面。
2. 执行命令的时候需要弹出确认对话框，等点击确认或取消时又要分别执行不同的命令。

以上情况就可能用到命令属性。当然，有时也会用定义子命令功能实现相同的效果，两种方式在功能和体验上略有差别，在本章节的最后会有专门的比较。
如果希望通过命令对话框编辑，可以通过标注CustomCommandObjectAttribute 的方式设置。
注意，标注CustomCommandObjectAttribute的属性类型必须是 object。

```
    public class MyPluginCommand : Command
    {
        [CustomCommandObject]
        [DisplayName("点击通知命令")]
        public object ClickNoticeCommand { get; set; }
    }
```

在设计器中效果如下：

对应的JavaScript处理代码， 使用 executeCustomCommandObject 方法执行命令属性中的命令。

```
class MyPluginCommand extends Forguncy.Plugin.CommandBase{
    execute() {
        const noticeDiv = $("<div style='width: 300px;top:-300px;right:20px;background:#FBF3DB;position:absolute;padding:10px'>有新的任务需要处理！点击处理<div>");
        $(document.body).append(noticeDiv);
        noticeDiv.animate({ top: '10px' }, 300);
        noticeDiv.click(() => {
            const command = this.CommandParam.ClickNoticeCommand;
            this.executeCustomCommandObject(command); // 执行命令中定义的单击命令
        });
        setTimeout(() => {
            noticeDiv.animate({ top: '-300px' }, 200, () => {
                noticeDiv.remove();
            });
        }, 3000);
    }
}

Forguncy.Plugin.CommandFactory.registerCommand("MyPlugin.MyPluginCommand, MyPlugin", MyPluginCommand);
```

如果需要更细致的控制，需要使用CustomCommandObjectAttribute标注来控制。
**1\. 支持上下文参数**

1. 设置CustomCommandObjectAttribute 的 InitParamValues 和 InitParamProperties 属性，多个上下文变量可以用“\|”分隔。
2. 代码：

    ```
        public class MyPluginCommand : Command
        {
            [CustomCommandObject(InitParamProperties = "context", InitParamValues = "上下文")]
            public object ClickNoticeCommand { get; set; }
        }
    ```
3. 设计器效果：
    
4. JavaScript 添加上下文参数处理。

    ```
    class MyPluginCommand extends Forguncy.Plugin.CommandBase{
        execute() {
            const noticeDiv = $("<div style='width: 300px;top:-300px;right:20px;background:#FBF3DB;position:absolute;padding:10px'>有新的任务需要处理！点击处理<div>");
            $(document.body).append(noticeDiv);
            noticeDiv.animate({ top: '10px' }, 300);
            noticeDiv.click(() => {
                const command = this.CommandParam.ClickNoticeCommand;
                const initPrarm = {};
                initPrarm[command.ParamProperties["context"]] = "MyContext";// 设置上下文值
                this.executeCustomCommandObject(command, initPrarm); // 执行命令中定义的单击命令
            });
            setTimeout(() => {
                noticeDiv.animate({ top: '-300px' }, 200, () => {
                    noticeDiv.remove();
                });
            }, 3000);
        }
    }
    
    Forguncy.Plugin.CommandFactory.registerCommand("MyPlugin.MyPluginCommand, MyPlugin", MyPluginCommand);
    ```

**2\. 上下文参数支持添加描述**

1. 设置CustomCommandObjectAttribute 的 ParameterDescriptions 属性。
2. 代码：

    ```
        public class MyPluginCommand : Command
        {
            [CustomCommandObject(InitParamProperties = "context", InitParamValues = "上下文",
                                ParameterDescriptions = "context:可以在上下文中包含了对应数据的ID")]
            public object ClickNoticeCommand { get; set; }
        }
    ```
3. 设计器效果：
    
4. 说明：
    * <span class="ne-text">添加适当的描述可以帮助用户更好的理解上下文变量的意义。</span>
    * <span class="ne-text">可以只给部分上下文变量添加注释。</span>
    * <span class="ne-text">本特性要求活字格版本大于等于9.0.100.0。</span>

---

## Datasourceproperty

# 数据源属性

## Content

如果属性绑定数据表的值，希望通过数据对话框编辑，可以通过标注BindingDataSourcePropertyAttribute 的方式设置。
注意，标注BindingDataSourcePropertyAttribute的属性类型必须是 object 。

```auto
    public class MyPluginCommand : Command
    {
        [BindingDataSourceProperty]
        [DisplayName("绑定数据源")]
        public object DataSource { get; set; }
    }
```

<span class="ne-text">在设计器中效果如下：</span>

### <span class="ne-text">对应的JavaScript处理代码</span>

<span class="ne-text">通过命令上的getBindingDataSourceValue方法获取绑定数据。</span>

```auto
class MyPluginCommand extends Forguncy.Plugin.CommandBase {
    async execute() {
        let dataSource = this.CommandParam.DataSource;

        var data = await this.getBindingDataSourceValue(dataSource);

        console.log(data);
    }
}

Forguncy.Plugin.CommandFactory.registerCommand("MyPlugin.MyPluginCommand, MyPlugin", MyPluginCommand);
```

<span class="ne-text">如果需要更细致的控制，可以通过BindingDataSourcePropertyAttribute的其他属性来控制。</span>
**1. <span class="ne-text">预置数据列</span>**

1. 设置BindingDataSourcePropertyAttribute 的 Columns 属性。
2. 代码：
    <span class="ne-text">格式：列名\|列名2\.\.\.</span>

    ```auto
         public class MyPluginCommand : Command
        {
            [BindingDataSourceProperty(Columns = "ID|Name")]
            [DisplayName("绑定数据源")]
            public object DataSource { get; set; }
        }
    ```
3. 设计器效果：
    

**2\. 为预置数据列添加显示文本**

1. 设置BindingDataSourcePropertyAttribute 的 Columns 属性。
2. 代码：
    <span class="ne-text">格式：列名:显示名\|列名2:显示名\|\.\.\.</span>

    ```auto
        public class MyPluginCommand : Command
        {
            [BindingDataSourceProperty(Columns = "ID|Name:姓名|Age:年龄")]
            [DisplayName("绑定数据源")]
            public object DataSource { get; set; }
        }
    ```
3. 设计器效果：
    
4. 注意：设置显示文本不影响JavaScript端数据处理，只影响在设计器中的显示。
5. 如果在此模式下仍然需要添加自定义列，可以设置AllowAddCustomColumns属性。

    ```auto
        public class MyPluginCommand : Command
        {
            [BindingDataSourceProperty(AllowAddCustomColumns = true, Columns = "ID|Name:姓名|Age:年龄")]
            [DisplayName("绑定数据源")]
            public object DataSource { get; set; }
        }
    ```
6. 设置AllowAddCustomColumns之后效果如下（此特性需要活字格版本大于等于9.0.100.0）。
    

**3\. 为预置数据源列添加描述信息**

1. 设置BindingDataSourcePropertyAttribute 的 ColumnsDescription 属性。
2. 代码：
    <span class="ne-text">格式：列名:描述\|列名2:描述2\.\.\.</span>

    ```auto
        public class MyPluginCommand : Command
        {
            [BindingDataSourceProperty(Columns = "ID|Name|Age", ColumnsDescription = "ID:通常绑定主键列|Age:表示年龄列")]
            [DisplayName("绑定数据源")]
            public object DataSource { get; set; }
        }
    ```
3. 设计器效果：
    
4. 注意，需要和Columns属性配合使用，在Columns里没有的列，设置的描述会被忽略。

**4\. 开启树结构查询配置（ID/PID 结构）**

1. 什么是ID/PID结构
    在数据库中，是用二维表保存数据的，但是现实生活中，很多数据会有父子关系，例如公司的组织机构，会在数据库中保存为如下形式，这样就可以使用二维表表示树结构了。

    | <span class="ne-text">ID</span> | <span class="ne-text">名称</span> | <span class="ne-text">PID</span> |
    | --- | --- | --- |
    | <span class="ne-text">1</span> | <span class="ne-text">xx公司</span> |  |
    | <span class="ne-text">2</span> | <span class="ne-text">财务部</span> | <span class="ne-text">1</span> |
    | <span class="ne-text">3</span> | <span class="ne-text">销售部</span> | <span class="ne-text">1</span> |
    | <span class="ne-text">4</span> | <span class="ne-text">销售一组</span> | <span class="ne-text">3</span> |
    | <span class="ne-text">5</span> | <span class="ne-text">销售二组</span> | <span class="ne-text">3</span> |
2. 设置BindingDataSourcePropertyAttribute 的 IsIdPidStructure 属性为True声明接受树结构表。
3. 代码：

    ```auto
        public class MyPluginCommand : Command
        {
            [BindingDataSourceProperty(Columns = "ID|Name|PID", IsIdPidStructure = true, TreeIdColumnName = "ID", TreePidColumnName = "PID")]
            [DisplayName("绑定数据源")]
            public object DataSource { get; set; }
        }
    ```
4. 设计器效果：
    <span class="ne-text">会在其他标签页中增加“树形结构查询配置”的选项。</span>
    ****
5. 注意：开启树形结构查询配置IsIdPidStructure属性后，需要配合设置 TreeIdColumnName 和 TreePidColumnName 属性。

**5.** **支持查询子表列**

1. 活字格中的子表
    <span class="ne-text">当在活字格中，设置关联关系时，可以勾选“是否有子表关联？”为True，此时，主表会增加一个虚拟列，如下图中的“订单详情表”。</span>
    
2. <span class="ne-text">设置BindingDataSourcePropertyAttribute 的 SupportDetailTable 属性。</span>
3. 代码：

    ```csharp
        public class MyPluginCommand : Command
        {
            [BindingDataSourceProperty(SupportDetailTable = true)]
            [DisplayName("绑定数据源")]
            public object DataSource { get; set; }
        }
    ```
4. 设计器效果：
    
5. 运行时获取数据的结果。数据库数据如下：
    订单表
    
    订单详情表
    
    执行结果

---

## Imagevalueproperty

# 图片属性

## Content

如果属性表示图片或图标，希望使用图片选择编辑器编辑属性，可以通过标注ImageValuePropertyAttribute 的方式设置。
注意：标注ImageValuePropertyAttribute的属性类型必须是 object 或 ImageValue。

```
    public class MyPluginCommand : Command
    {
        [ImageValueProperty]
        public object MyProperty { get; set; }
    }
```

在设计器中效果如下：

如果需要更细致的控制，需要使用 ImageValuePropertyAttribute标注来控制。
**1\. 禁止选择SVG图片。**

1. 设置ImageValuePropertyAttribute的 SupportSvg属性。
2. 代码：

    ```
        public class MyPluginCommand : Command
        {
            [ImageValueProperty(SupportSvg = false)]
            public object MyProperty { get; set; }
        }
    ```
3. 效果：
    在图片选择对话框中只允许选择或上传普通图片，不能选择或上传SVG图片。
    

**2\. 设置内置图标默认值。**
例如内建单元格中如果没有设置图标，按钮的图标默认值是白色的，文本框的图标默认是灰色的。

1. 设置ImageValuePropertyAttribute 的 DefaultIconColor 属性。
2. 代码。关于活字格中的颜色字符串表示法，请参考 [颜色属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/addproperty/colorproperty)。

    ```
        public class MyPluginCommand : Command
        {
            [ImageValueProperty(DefaultIconColor = "Accent 2")]
            public object MyProperty { get; set; }
        }
    ```
3. 效果：
    

**3\. 设置默认选中的标签页。**
如果该属性大部分情况下推荐用户使用内建图标，应该把默认标签页设置为“内置图标”。

1. 设置ImageValuePropertyAttribute 的 DefaultActiveTabIndex 属性。
2. 代码：

    ```
        public class MyPluginCommand : Command
        {
            [ImageValueProperty(DefaultActiveTabIndex = 1)]
            public object MyProperty { get; set; }
        }
    ```
3. 效果：
    
4. 说明：
    默认值为0表示默认标签页为本地图片，如果设置为 1 表示默认选中内置图标，其他值无效。

**4\. 禁止图标使用单元格字体颜色。**

1. 设置ImageValuePropertyAttribute 的 SupportUseCellColor 属性。
2. 代码。关于活字格中的颜色字符串表示法，请参考 [颜色属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/addproperty/colorproperty)。

    ```
        public class MyPluginCommand : Command
        {
            [ImageValueProperty(SupportUseCellColor = false)]
            public object MyProperty { get; set; }
        }
    ```

**5\. 图标默认设置为使用单元格字体颜色。**

1. 设置ImageValuePropertyAttribute 的 DefaultUseCellColor 属性。
2. 代码：

    ```
        public class MyPluginCommand : Command
        {
            [ImageValueProperty(DefaultUseCellColor = true)]
            public object MyProperty { get; set; }
        }
    ```
3. 效果：
    

### JavaScript 中的图片处理

在活字格中，图片使用分为三种情况：

1. 普通图片
2. SVG图片
3. 内置SVG图标

```
class MyPluginCommand extends Forguncy.Plugin.CommandBase{
    execute() {
        const image = this.CommandParam.MyProperty;
        if (image && image.Name) {
            let src = "";
            if (image.BuiltIn) {
                // 构建内建图标URL
                src = Forguncy.Helper.SpecialPath.getBuiltInImageFolderPath() + image.Name;
            }
            else {
                // 构建用户上传图片URL
                src = Forguncy.Helper.SpecialPath.getImageEditorUploadImageFolderPath() + encodeURIComponent(image.Name);
            }
            if (Forguncy.ImageDataHelper.IsSvg(src)) {
                // 如果是SVG需要发送请求获取SVG DOM结构，因为需要修改SVG的颜色，不能直接使用Image的src属性
                $.get(src, (data) => {
                    const svg = $(data.documentElement);
                    Forguncy.ImageHelper.preHandleSvg(svg, image.UseCellTypeForeColor ? "currentColor" : image.Color);
                    svg.css("height", 100);
                    $(document.body).prepend(svg);
                });
            }
            else {
                document.body.style.backgroundImage = `url(${src})`;
            }
        }
    }
}

Forguncy.Plugin.CommandFactory.registerCommand("MyPlugin.MyPluginCommand, MyPlugin", MyPluginCommand);
```

实际上图片类型的属性会在生成一个JavaScript对象，这个JavaScript对象包含4个属性：

1. IsBuiltIn： 表示是否为内建图标。
2. Name：表示图片名称。
3. Color：SVG 图片颜色，只有图片为SVG图片并且UseCellTypeForeColor时有效。
4. UseCellTypeForeColor：SVG 图片使用单元格字体颜色，只有SVG 图片有效。

---

## Listproperty

# 列表属性

## Content

如果一个属性的类型是List类型，List的每一项又包含了子属性，那么可以通过标注ListPropertyAttribute，使得活字格设计器可以通过弹出二级对话框来编辑该属性。
注意，ObjType属性里声明的类型必须与属性类型一致。
自定义对象的类型应该从 ObjectPropertyBase 类派生，以确保在单元格复制的时候，子属性可以被正确的深克隆（ObjectPropertyBase实现了默认的深克隆逻辑）。

```csharp
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;
using System.Collections.Generic;

namespace MyPlugin
{
    public class MyPluginCommand : Command
    {
        [ListProperty]
        public List<MyObj> MyProperty { get; set; }
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
下面示例中，额外声明了两个属性分别使用公式编辑器和命令编辑器。具体标注的用法请参考之前的章节。

```csharp
    public class MyPluginCommand : Command
    {
        [ListProperty]
        public List<MyObj> MyProperty { get; set; }
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
2. 代码如下：

    ```csharp
        public class MyPluginCommand : Command
        {
            [ListProperty(MaxCount = 5, MinCount = 1)]
            public List<MyObj> MyProperty { get; set; }
        }
    
        public class MyObj: ObjectPropertyBase
        {
            public string Name { get; set; }
            public string Description { get; set; }
        }
    ```

**2.指定属性的默认值。**

1. <span class="ne-text">给属性添加ListPropertyItemSettingAttribute 的 DefaultName 属性。</span>
2. <span class="ne-text">代码如下：</span>

    ```csharp
        public class MyPluginCommand : Command
        {
            [ListProperty]
            public List<MyObj> MyProperty { get; set; }
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
        public class MyPluginCommand : Command
        {
            [ListProperty]
            public List<MyObj> MyProperty { get; set; }
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
        public class MyPluginCommand : Command
        {
            [ListProperty]
            public List<MyObj> MyProperty { get; set; }
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
        public class MyPluginCommand : Command
        {
            [FlatListProperty]
            public List<MyObj> MyProperty { get; set; }
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
    public class MyPluginCommand : Command
    {
        [ObjectListProperty(ItemType = typeof(MyObj))]
        public List<INamedObject> MyProperty { get; set; } = new List<INamedObject>();
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
    public class MyPluginCommand : Command
    {
        [ObjectListProperty(ItemType = typeof(MyObj))]
        public List<INamedObject> MyProperty { get; set; } = new List<INamedObject>();
    }

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

在设计器中效果如下：

如果需要更细致的控制，可以通过ObjectListPropertyAttribute的其他属性来控制

1. 控制列表最大元素个数
    1. 设置ObjectListPropertyAttribute 的 MaxCount 属性。
    2. 代码：

        ```
            public class MyPluginCommand : Command
            {
                [ObjectListProperty(ItemType = typeof(MyObj), MaxCount = 4)]
                public List<INamedObject> MyProperty { get; set; } = new List<INamedObject>();
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
2. 控制默认结点名称
    1. 设置ObjectListPropertyAttribute 的 DefaultName 属性。
    2. 代码：

        ```
            public class MyPluginCommand : Command
            {
                [ObjectListProperty(ItemType = typeof(MyObj), DefaultName = "结点")]
                public List<INamedObject> MyProperty { get; set; } = new List<INamedObject>();
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

ListPropertyAttribute和ObjectListPropertyAttribute解决的是完全相同的问题，只是表现方式不同。
ObjectListPropertyAttribute 更适合项目子属性比较多的情况，而ListProperty则在子属性比较少的时候比较适用。

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

namespace MyPlugin
{
    public class MyPluginCommand : Command
    {
        [ObjectProperty(ObjType = typeof(MyObj))]
        public MyObj MyProperty { get; set; }
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
下面例子中，额外声明了两个属性分别使用公式编辑器和命令编辑器。具体标注的用法请参考之前的章节。

```csharp
    public class MyPluginCommand : Command
    {
        [ObjectProperty(ObjType=typeof(MyObj))]
        public MyObj MyProperty { get; set; }
    }

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

在设计器中效果如下：

#### 高级配置

**1.添加描述：**

1. <span class="ne-text">设置 DescriptionAttribute。</span>
2. <span class="ne-text">代码如下：</span>

    ```auto
        public class MyPluginCommand : Command
        {
            [ObjectProperty(ObjType=typeof(MyObj))]
            public MyObj MyProperty { get; set; }
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

**2.给对象添加自定义校验：**

1. <span class="ne-text">给属性添加DesignerAttribute 重写Validate方法添加自定义校验。</span>
2. <span class="ne-text">代码如下：</span>

    ```auto
        public class MyPluginCommand : Command
        {
            [ObjectProperty(ObjType = typeof(MyObj))]
            public MyObj MyProperty { get; set; }
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
        public class MyPluginCommand : Command
        {
            [DisplayName("姓名")]
            public string Name { get; set; }
    
            [FlatObjectProperty]
            [DisplayName("地址")]
            public Address Address { get; set; } = new Address();
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

1. <span class="ne-text">给对象标注 FlatObjectProperty 实现子对象属性内嵌显示，同时通过</span>[<span class="ne-text">属性值联动</span>](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/propertyvaluelinkage)<span class="ne-text">在不同情况下显示不同的子属性。</span>
2. <span class="ne-text">代码如下：</span>

    ```auto
         [Designer(typeof(MyCommandDesigner))]
        public class MyPluginCommand : Command
        {
            [ComboProperty(ValueList = "Type1|Type2")]
            public string Type { get; set; } = "Type1";
    
            [FlatObjectProperty]
            public object SubProperty { get; set; } = new Type1SubProperty();
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
3. <span class="ne-text">下面的示例代码中， MyObject 对象拥有两个属性，当用户编辑 Data1 时，Data2 将改变，值为 Data1 + 1。</span>

    ```auto
         public class TestCommand : Command
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

## Radiogroupproperty

# 单选框属性

## Content

如果属性的类型是字符串，默认属性值是可以接受任意字符串的，如果希望提供字符串值候选列表，可以通过标注RadioGroupProperty 的并设置ValueList属性的方式实现单选框候选列表。多个值用“\|”分隔。
RadioGroupProperty和ComboProperty的使用方式非常类似，主要是在设计器中的UI表现不同。
注意，标注RadioGroupProperty的属性类型必须是 string。

```
    public class MyPluginCommand : Command
    {
        [RadioGroupProperty(ValueList = "Student|Teacher|Worker")]
        public string MyProperty { get; set; }
    }
```

在设计器中效果如下：

如果需要更细致的控制，可以通过RadioGroupProperty的其他属性来控制。

1. 值与显示值不同
    1. 设置RadioGroupProperty的 DisplayList 属性。
    2. 代码：

        ```
            public class MyPluginCommand : Command
            {
                [RadioGroupProperty(ValueList = "Student|Teacher|Worker", DisplayList ="学生|教师|工人")]
                public string MyProperty { get; set; }
            }
        ```
    3. 效果：
        
    4. 其他说明：
        此方法可以使用户在选择时选择中文选项，而单元格实际保存值为英文，方便程序处理。ValueList和DisplayList通过数量和顺序匹配。
        如果DisplayList数量超出ValueList数量，多出部分会被忽略；
        如果DisplayList数量少于ValueList数量，不足部分会使用ValueList对应的值。

---

## Servercommandnameproperty

# 服务端命令选择属性

## Content

此特性为活字格V9.1新增功能。

```auto
    public class MyPluginCommand : Command
    {
        [ServerCommandNameProperty]
        public string MyProperty { get; set; }
    }
```

在设计器中效果如下：

注意：标注ServerCommandNameProperty的属性类型必须是 string。

---

## Addsubcommand

# 添加子命令

## Content

可以通过实现 ISubListCommand 和 IContainSubCommands 实现给命令添加子命令。

```auto
using GrapeCity.Forguncy.Commands;
using System.Collections.Generic;
using System.ComponentModel;

namespace MyPlugin
{
    public class MyPluginCommand : Command, ISubListCommand, IContainSubCommands
    {
        [Browsable(false)]
        public List<Command> CommandList { get; set; } = new List<Command>();

        public IEnumerable<List<Command>> EnumSubCommands()
        {
            yield return CommandList;
        }
    }
}
```

代码说明：给 CommandList属性标注 [Browsable(false)] 避免CommandList属性出现在主命令的属性中。
效果：

JavaScript 中需要添加对于的逻辑来执行子命令

```auto
class MyPluginCommand extends Forguncy.Plugin.CommandBase{
    execute() {
        this.CommandExecutor.excuteCommand(this.CommandParam.CommandList, {
            runTimePageName: this.CommandExecutingInfo.runTimePageName,
            commandID: "myCommand",
        });
    }
}

Forguncy.Plugin.CommandFactory.registerCommand("MyPlugin.MyPluginCommand, MyPlugin", MyPluginCommand);
```

>type=note
> **命令执行防抖：**
> 为了避免相同的命令在短时间内多次执行，相同“commandID”的命令在短时间内（1秒内），只会被执行一次。如果希望命令在短时间内执行多次，可以把commandID设置为唯一值，例如
> commandID: new Date().valueOf().toString()

### 给子命令添加初始参数

如果调用子命令时需要给子命令传递初始参数，需要如下修改JS代码：

```auto
class MyPluginCommand extends Forguncy.Plugin.CommandBase{
    execute() {
        this.CommandExecutor.excuteCommand(this.CommandParam.CommandList, {
            runTimePageName: this.CommandExecutingInfo.runTimePageName,
            commandID: "myCommand",
            // 子命令初始参数
            initParams:{
                "aaa": 1,
                "bbb": 2
            },
            locationString: "我的命令" // 控制台日志中显示字符串
        });
    }
}

Forguncy.Plugin.CommandFactory.registerCommand("MyPlugin.MyPluginCommand, MyPlugin", MyPluginCommand);
```

通过执行日志，我们可以看到，在执行子命令之前会初始化上下文参数。

此时，后续命令可以使用变量 “aaa”和“bbb”了，但是，在设计器里没有办法选择相应的变量，为了让设计器中可以选择“aaa”和“bbb”变量，cs 文件需要做如下修改：

```auto
using GrapeCity.Forguncy.Commands;
using System.Collections.Generic;
using System.ComponentModel;

namespace MyPlugin
{
    public class MyPluginCommand : Command, ISubListCommand, IContainSubCommands
    {
        [ResultToProperty]
        [Browsable(false)]
        public string SubCommandParam { get; set; } = "aaa";

        [ResultToProperty]
        [Browsable(false)]
        public string SubCommandParam2 { get; set; } = "bbb";

        [Browsable(false)]
        public List<Command> CommandList { get; set; } = new List<Command>();

        public IEnumerable<List<Command>> EnumSubCommands()
        {
            yield return CommandList;
        }
    }
}
```

设计器效果：

注意：这个设计器支持初始变量的功能并不完美，“aaa”和“bbb”这两个上下文变量，不光子命令会有提示，主命令的后续命令也会提示，这是一个限制。目前没有好的方案解决。

---

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

## Setcommandvisibilityrange

# 设置命令可见范围

## Content

有些命令只应该在PC页面使用，有些只应该在手机页面上使用，通过CommandSupportUsingScope可以控制命令的可见范围。

```
    [CommandSupportUsingScope(CommandPageScope.AllPCPage)]
    public class MyPluginCommand : Command
    {
    }
```

  

CommandPageScope 值

| NormalPCPage | 普通PC页面 |
| --- | --- |
| NormalMobilePage | 普通手机页面 |
| MasterPCPage | PC 母版页 |
| MasterMobilePage | 手机母版页 |
| TemplatePCPage | PC页图文列表模板 |
| TemplateMobilePage | 手机页图文列表模板 |
| UserControlPage | 组件  |
| AllPCPage | 所有PC页 |
| AllMobilePage | 所有手机页 |
| AllNormalPage | 所有普通页 |
| AllMasterPage | 所有母版页 |
| AllTemplatePage | 所有图文列表模板 |
| AllPage | 所有页面（默认值） |

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

## Adddescriptionstocommandproperties

# 给命令属性添加说明

## Content

有时，属性的功能或用法并不能通过属性名直接被理解，此时应该给属性添加一些描述，详细说明属性的功能、用法或特殊策略。

通过标注 DescriptionAttribute 可以实现此功能。

示例代码：

```
    public class MyPluginCellType : CellType
    {
        [Description("这里可以写一些描述")]
        public string MyProperty1 { get; set; }
        [FormulaProperty]
        [Description("描述文本可以是多行的\r\n通过鼠标悬停到问号图标上查看")]
        public object MyProperty2 { get; set; }
    }
```

  

设计器中的效果：

---

## Adddescriptiontocommand

# 给命令添加说明

## Content

有时，命令的功能或用法不好理解，或者是命令有一些特别的策略需要说明。为了让使用者更好的使用命令，应该给命令添加一些描述，详细说明命令的功能、用法或特殊策略。

通过标注 DescriptionAttribute 可以实现此功能。

示例代码：

```
    [Description("描述文本可以是多行的\r\n从这里开始是第二行描述了，如果描述文本特别长，是会自动换行的，命令的描述会出现在所有属性之后")]
    public class MyPluginCommand : Command
    {
        public string MyProperty1 { get; set; }
        [FormulaProperty]
        public object MyProperty2 { get; set; }
    }
```

  

设计器中的效果：

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
    [Category("导航")]
    public class MyPluginCommand : Command
    {
    }
```

  

效果如下：

如果有多个插件，在同一分组，可以通过OrderWeightAttribute标注排序权重。

```
    [OrderWeight(1)]
    [Category("我的分组")]
    public class MyPluginCommand1 : Command
    {
    }
    [OrderWeight(2)]
    [Category("我的分组")]
    public class MyPluginCommand2 : Command
    {
    }
    [OrderWeight(3)]
    [Category("我的分组")]
    public class MyPluginCommand3 : Command
    {
    }
```

  

设计器效果：

---

## Customcommandeditor

# 自定义命令编辑器

## Content

*   [自定义命令属性编辑控件](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/customcommandeditor/customcommandpropertyeditingcontrol)
*   [自定义命令属性编辑窗体](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/customcommandeditor/customcommandpropertyeditingform)
*   [自定义命令编辑控件](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcommandplugin/supportcommanddesigntime/customcommandeditor/customcommandeditingcontrol)

---

## SupportBatchSelectionOfCommandParameters

# 支持批量选中命令参数

## Content

对于 ListProperty 和 FlatListProperty参数来说，为了提升参数选择的易用性，可以使用批量选中的功能。本章将向您介绍如何在插件中实现此功能。
如下例是一个同时拥有 ListProperty 与 FlatListProperty属性的命令：

```auto
[Icon("pack://application:,,,/Test;component/Resources/Icon.png")]
[Designer("Test.Designer.TestCommandDesigner, Test")]
public class TestCommand : Command
{
    [ListProperty]
    public List<DataObject> DataObject1 { get; set; } = new List<DataObject>();

    [FlatListProperty]
    public List<DataObject> DataObject2 { get; set; } = new List<DataObject>();
}

public class DataObject : ObjectPropertyBase
{
    [IntelligentName]
    public string Name { get; set; }

    [FormulaProperty]
    [IntelligentFormula]
    public object Value { get; set; }
}
```

您可以在模型类型 DataObject定义时，标记 IntelligentNameAttribute 与 IntelligentFormulaAttribute 特性，当标记之后，您就可以得到如下的批量选择的功能：

需要注意以下两点：
1\. IntelligentNameAttribute 与 IntelligentFormulaAttribute特性必须成对出现，一个用来标记快速选择资源的Name，一个标记Value
2\. 此特性为 10\.0\.100\.0 版本新增的特性。

---

## Customcommandeditingcontrol

# 自定义命令编辑控件

## Content

有些情况下，为了提升用户体验，会自定义整个命令编辑界面。而不是通过属性定义自定生成命令编辑界面。例如页面跳转命令，数据表操作命令就是这样的情况。

要实现完全自定义的编辑控件需要自定义WPF 控件，并让此控件实现 ICommandEditor 接口。
步骤如下：
1.添加一个自定义窗体。

1. 在插件工程中Designer文件夹点击右键，选择“添加->窗口（WPF）”。
    
2. 在弹出对话框中指定名称为 MyCommandPropertyEditor.xaml。
3. 创建成功过后分别按以下代码修改 MyPluginCommandEditor.xaml 和 MyPluginCommandEditor.xaml.cs 文件。

* MyPluginCommandEditor.xaml 文件

    代码说明：在控件中添加了一个多行文本框（可以根据需求加入其它控件）。

```
<UserControl x:Class="MyPlugin.Designer.MyPluginCommandEditor"
             xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" 
             xmlns:d="http://schemas.microsoft.com/expression/blend/2008" 
             xmlns:local="clr-namespace:MyPlugin.Designer"
             mc:Ignorable="d" 
             MinHeight="100" d:DesignWidth="800">
    <StackPanel x:Name="root">
        <TextBlock>完全自定义的命令编辑界面</TextBlock>
        <TextBlock>可以使用任何组件布局</TextBlock>
        <TextBox Width="300" Height="200" HorizontalAlignment="Left" AcceptsReturn="True" Text="{Binding Text}"></TextBox>
    </StackPanel>
</UserControl>
```

* MyPluginCommandEditor.xaml.cs 文件

    代码说明：实现 ICommandEditor 接口，使用 Command 属性和 Validate 方法实现编辑。

```
using GrapeCity.Forguncy.Commands;
using System.ComponentModel;
using System.Windows;
using System.Windows.Controls;

namespace MyPlugin.Designer
{
    /// 
    /// MyPluginCommandEditor.xaml 的交互逻辑
    /// 
    public partial class MyPluginCommandEditor : UserControl, ICommandEditor
    {
        public MyPluginCommandEditor()
        {
            InitializeComponent();
            this.root.DataContext = new MyCommandPropertyEditorViewModel();
        }

        public MyCommandPropertyEditorViewModel ViewModel
        {
            get
            {
                return this.root.DataContext as MyCommandPropertyEditorViewModel;
            }
        }
        // 初始化时会调用属性的 set 方法，在set方法中可以初始化UI控件的值
        // 在Validate()函数校验通过后会调用属性的 get 方法，可以通过 UI 控件 编辑后的值生成一个命令保存
        public Command Command
        {
            get
            {
                return new MyPluginCommand() { MyProperty = this.ViewModel.Text };
            }
            set
            {
                var command = value as MyPluginCommand;
                this.ViewModel.Text = command.MyProperty;
            }
        }

        // 自定义校验逻辑，提交编辑的时候会被调用，返回false表示校验失败
        public bool Validate()
        {
            if (string.IsNullOrEmpty(this.ViewModel.Text))
            {
                MessageBox.Show("XXX属性值不能为空", "错误", MessageBoxButton.OKCancel, MessageBoxImage.Error);
                return false;
            }
            return true;
        }

        public class MyCommandPropertyEditorViewModel : INotifyPropertyChanged
        {

            private string _text;
            public string Text
            {
                get
                {
                    return this._text;
                }
                set
                {
                    if (_text != value)
                    {
                        this._text = value;
                        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(Text)));
                    }
                }
            }

            public event PropertyChangedEventHandler PropertyChanged;
        }
    }
}
```

2.修改MyPluginCommandDesigner.cs文件，让控件和属性关联。

```
    public class MyPluginCommandDesigner : CommandDesigner<MyPluginCommand>
    {
        public override ICommandEditor GetCommandEditor()
        {
            return new MyPluginCommandEditor();
        }
    }
```

3.修改 MyPluginCommand.cs 文件，通过DesignerAttribute 和 MyPluginCommandDesigner 关联。

```
using GrapeCity.Forguncy.Commands;
using System.ComponentModel;

namespace MyPlugin
{
    [Designer("MyPlugin.Designer.MyPluginCommandDesigner, MyPlugin")]
    public class MyPluginCommand : Command
    {
        public string MyProperty { get; set; }
    }
}
```

4.效果如下：

---

## Customcommandpropertyeditingcontrol

# 自定义命令属性编辑控件

## Content

大部分情况下，通过标注不同的Attribute给属性，可以指定使用不同的内置属性编辑器。
但是如果希望命令通过更复杂的方式编辑就需要通过自定义一个WPF的用户组件来实现了。
**1.** 在MyPluginCommand中定义一个属性。

```
    [Designer("MyPlugin.Designer.MyPluginCommandDesigner, MyPlugin")]
    public class MyPluginCommand : Command
    {
        [DisplayName("说明：")]
        public string MyProperty { get; set; }
    }
```

**2.** 添加一个自定义窗体。

1. 在插件工程中Designer文件夹点击右键，选择“添加->用户控件（WPF）”。
    
2. 在弹出对话框中指定名称为 MyCommandPropertyEditor.xaml。
    
3. 创建成功过后分别按以下代码修改 MyCommandPropertyEditor.xaml 和 MyCommandPropertyEditor.xaml.cs 文件。
    * MyCommandPropertyEditor.xaml 文件代码说明：在控件中添加了一个多行文本框（可以根据需求加入其它控件）。

```
<UserControl x:Class="MyPlugin.Designer.MyCommandPropertyEditor"
             xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" 
             xmlns:d="http://schemas.microsoft.com/expression/blend/2008" 
             xmlns:local="clr-namespace:MyPlugin.Designer"
             mc:Ignorable="d" 
             MinHeight="100" d:DesignWidth="800">
    <Grid x:Name="root">
        <TextBox VerticalContentAlignment="Stretch"  Margin="9,0,0,0" AcceptsReturn="True" Text="{Binding Text}"></TextBox>
    </Grid>
</UserControl>
```

* MyCommandPropertyEditor.xaml.cs 文件代码说明：MyCommandPropertyEditor\_DataContextChanged 通过 DataContext 属性可以和属性值互操作。

```
using GrapeCity.Forguncy.Plugin;
using System.ComponentModel;
using System.Windows;
using System.Windows.Controls;

namespace MyPlugin.Designer
{
    public partial class MyCommandPropertyEditor : UserControl
    {
        public MyCommandPropertyEditor()
        {
            InitializeComponent();
            this.root.DataContext = new MyCommandPropertyEditorViewModel();
            this.DataContextChanged += MyCommandPropertyEditor_DataContextChanged;
        }

        private void MyCommandPropertyEditor_DataContextChanged(object sender, DependencyPropertyChangedEventArgs e)
        {
            if (this.DataContext is IEditorSettingsDataContext editorSettingsDataContext)
            {
                this.ViewModel.Text = editorSettingsDataContext.Value?.ToString();
                this.ViewModel.PropertyChanged += (o, e2) =>
                {
                    editorSettingsDataContext.Value = this.ViewModel.Text;
                };
            }
        }

        public MyCommandPropertyEditorViewModel ViewModel
        {
            get
            {
                return this.root.DataContext as MyCommandPropertyEditorViewModel;
            }
        }

        public class MyCommandPropertyEditorViewModel : INotifyPropertyChanged
        {

            private string _text;
            public string Text
            {
                get
                {
                    return this._text;
                }
                set
                {
                    if (_text != value)
                    {
                        this._text = value;
                        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(Text)));
                    }
                }
            }

            public event PropertyChangedEventHandler PropertyChanged;
        }
    }
}
```

**3.** 修改MyPluginCommandDesigner.cs文件，让控件和属性关联。

```
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;
using System;
using System.ComponentModel;
using System.Windows;

namespace MyPlugin.Designer
{
    public class MyPluginCommandDesigner : CommandDesigner<MyPluginCommand>
    {
        public override EditorSetting GetEditorSetting(PropertyDescriptor property, IBuilderCommandContext builderContext)
        {
            if(property.Name == nameof(MyPluginCommand.MyProperty))
            {
                return new MyEditorSetting();
            }
            return base.GetEditorSetting(property, builderContext);
        }
    }

    class MyEditorSetting : EditorSetting
    {
        public override DataTemplate GetDataTemplate()
        {
            DataTemplate template = new DataTemplate();
            FrameworkElementFactory spFactory = new FrameworkElementFactory(typeof(MyCommandPropertyEditor));
            template.VisualTree = spFactory;
            return template;
        }
        public override VerticalAlignment LabelVerticalAlignment => VerticalAlignment.Top;
    }
}
```

**4.** 效果：

---

## Customcommandpropertyeditingform

# 自定义命令属性编辑窗体

## Content

大部分情况下，通过标注不同的Attribute给属性，可以指定使用不同的内置属性编辑器。
但是如果希望命令通过自定义的对话框编辑，就需要自定义一个WPF的窗体来实现了。
1.在MyPluginCommand中定义一个属性。

```
    [Designer("MyPlugin.Designer.MyPluginCommandDesigner, MyPlugin")]
    public class MyPluginCommand : Command
    {
        public string MyProperty { get; set; }
    }
```

2.添加一个自定义窗体。

1. 在插件工程中Designer文件夹点击右键，选择“添加->窗口（WPF）”。
    
2. 在弹出对话框中指定名称为 MyCommandPropertyEditor.xaml。
3. 创建成功过后分别按以下代码修改 MyCommandEditorWindow.xaml 和 MyCommandEditorWindow.xaml.cs 文件。

* MyCommandEditorWindow.xaml 文件

    代码说明：在窗体中添加了一个标签控件、一个多行文本框控件（文本属性和.cs文件中的文本属性绑定）、一个确定按钮、一个取消按钮。

```
<Window x:Class="MyPlugin.Designer.MyCommandEditorWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        xmlns:local="clr-namespace:MyPlugin.Designer"
        mc:Ignorable="d"
        WindowStartupLocation="CenterScreen"
        Title="MyCommandEditorWindow" Height="400" Width="500">
    <Grid Margin="10">
        <Grid.RowDefinitions>
            <RowDefinition Height="auto"></RowDefinition>
            <RowDefinition></RowDefinition>
            <RowDefinition Height="auto"></RowDefinition>
        </Grid.RowDefinitions>
        <TextBlock>我的注释</TextBlock>
        <TextBox VerticalContentAlignment="Stretch"  Margin="0,5,0,5" Grid.Row="1" AcceptsReturn="True" Text="{Binding Text}"></TextBox>
        <StackPanel Orientation="Horizontal" Grid.Row="2" HorizontalAlignment="Right">
            <Button x:Name="OkButton" Click="OKButton_Click"  Height="30" Width="70" Margin="0,0,10,0">确定</Button>
            <Button Click="CancelButton_Click"  Height="30" Width="70">取消</Button>
        </StackPanel>
    </Grid>
</Window>
```

* MyCommandEditorWindow.xaml.cs 文件代码说明：添加了确定按钮，取消按钮的点击逻辑，在ViewModel类上声明了 Text 属性与控件绑定。

```
using System.ComponentModel;
using System.Windows;

namespace MyPlugin.Designer
{
    /// 
    /// Interaction logic for MyCommandEditorWindow.xaml
    /// 
    public partial class MyCommandEditorWindow : Window
    {
        public MyCommandEditorWindow()
        {
            this.DataContext = new MyCommandEditorWindowViewModel();
            InitializeComponent();
        }

        public MyCommandEditorWindowViewModel ViewModel
        {
            get
            {
                return this.DataContext as MyCommandEditorWindowViewModel;
            }
        }

        public class MyCommandEditorWindowViewModel: INotifyPropertyChanged
        {

            private string _text;
            public string Text
            {
                get
                {
                    return this._text;
                }
                set
                {
                    if (_text != value)
                    {
                        this._text = value;
                        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(Text)));
                    }
                }
            }

            public event PropertyChangedEventHandler PropertyChanged;
        }

        private void OKButton_Click(object sender, RoutedEventArgs e)
        {
            this.OkButton.Focus();
            this.DialogResult = true;
            this.Close();
        }

        private void CancelButton_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }
    }
}
```

3.修改MyPluginCommandDesigner.cs文件，让窗体和属性关联。

```
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;
using System;
using System.ComponentModel;

namespace MyPlugin.Designer
{
    public class MyPluginCommandDesigner : CommandDesigner<MyPluginCommand>
    {
        public override EditorSetting GetEditorSetting(PropertyDescriptor property, IBuilderCommandContext builderContext)
        {
            if(property.Name == nameof(MyPluginCommand.MyProperty))
            {
                return new HyperlinkEditorSetting(new ShowDialogCommand());
            }
            return base.GetEditorSetting(property, builderContext);
        }
    }

    class ShowDialogCommand : System.Windows.Input.ICommand
    {
        public event EventHandler CanExecuteChanged;

        public bool CanExecute(object parameter)
        {
            return true;
        }

        public void Execute(object parameter)
        {
            if(parameter is IEditorSettingsDataContext dataContext)
            {
                var editWindow = new MyCommandEditorWindow();
                editWindow.ViewModel.Text = dataContext.Value?.ToString();
                if(editWindow.ShowDialog() == true)
                {
                    dataContext.Value = editWindow.ViewModel.Text;
                }
            }
        }
    }
}
```

4.效果：