# Runtime Behavior

## Developformcell

# 开发表单类单元格

## Content

*   [支持单元格值](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportcellvalues)
*   [支持默认值](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportdefaultvalue)
*   [支持值变更命令](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportvaluechangecommand)
*   [支持数据校验](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportdataverification)
*   [支持只读](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportreadonly)
*   [支持禁用](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportdisable)
*   [支持单元格权限](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportcellpermissions)
*   [支持Tab键顺序](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportstaborder)
*   [支持离开页面时检查是否有未提交的数据](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportcheckuncommitteddatawhenleavingpage)

---

## Addmodificationattributevalueoperation

# 添加修改属性值操作

## Content

在上一章节中，我们了解了如何定义单元格的属性。这些属性有一个小小的缺憾，就是属性的值是在设计时决定的。在网站构建好之后就没有办法修改了。如果属实的值希望根据不同的情况进行修改，该怎么做呢？

单元格操作可以很方便的实现这个需求。

  

在MyPluginCellType.cs文件中做如下修改：

```
public class MyPluginCellType : CellType
    {
        [SupportModifyByRuntimeProperty]
        [DisplayName("按钮文本")]
        public string ButtonText { get; set; }
    }
```

  

设计器效果：  
  

修改 文件中的JavaScript代码，注意，这里添加了 “set\_ButtonText”方法，在这个方法中修改了按钮的文本。“set\_属性名”是一个固定的命名规则，如果一个属性标注了“SupportModifyByRuntimeProperty”特性，就表示这个属性在运行时，可以通过操作单元格命令修改。修改时，活字格会调用单元格插件的 “set\_指定属性名”方法，在方法中添加相应的变更逻辑即可。

```
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    content = null;
    createContent() {
        this.content = $("<button style='width:100%;height:100%;'></button>");
        this.content.text(this.CellElement.CellType.ButtonText);
        return this.content;
    }
    set_ButtonText(value) {
        this.content.text(value);
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

  

测试

在设计器中添加一个按钮，按照下图配置按钮命令。  
  

运行后，单击“设置按钮文本按钮”可以发现插件按钮的文本变了。

  

我们可以注意到，在操作单元格命令中，按钮文本属性是文本框。这个编辑控件实际上默认会使用属性标注的控件，例如，如果属性按照如下标注：

```
    public class MyPluginCellType : CellType
    {
        [SupportModifyByRuntimeProperty]
        [DisplayName("按钮文本")]
        [ComboProperty(ValueList ="确认|取消|关闭")]
        public string ButtonText { get; set; }
    }
```

  

设计器中的效果：  
  

  

如果希望不使用属性标注的编辑控件，而强制使用公式编辑框，可以通过设置 UseFormulaEditor 属性为 True来实现。

```
    public class MyPluginCellType : CellType
    {
        [SupportModifyByRuntimeProperty(UseFormulaEditor = true)]
        [DisplayName("按钮文本")]
        public string ButtonText { get; set; }
    }
```

  

设计器中效果如下：

---

## Formulaproperty

# 公式属性

## Content

如果属性值需要依赖公式的计算结果动态变化，可以通过标注FormulaPropertyAttribute 的方式设置。注意，标注FormulaPropertyAttribute的属性类型必须是 object。

```auto
    public class MyPluginCellType : CellType
    {
        [FormulaProperty]
        public object MyProperty { get; set; }
    }
```

在设计器中效果如下：

为支持公式属性，单元格对应的JavaScript类也需要对应的处理，可以通过evaluateFormula方法计算公式的值。

```auto
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    content = null;
    createContent() {
        this.content = $("<div style='width:100%;height:100%;'></div>");
        return this.content;
    }
    onPageLoaded() {
        const prop = this.CellElement.CellType.MyProperty;
        const result = this.evaluateFormula(prop)
        this.content.text(result)
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

相信看了以上示例代码之后一定会有小伙伴有所疑惑，为什么不在createContent函数里计算公式的值，而是在onPageLoaded函数中呢？
因为createContent函数是用来构建当前单元格的，页面上的每一个单元格都会一个一个的调用一个方法来构建，如果在createContent函数中计算公式值，如公式又刚好依赖了还没有被构建好的单元格，会导致计算结果不正确。解决方案就是吧计算逻辑延后到 onPageLoaded 函数中。这个函数会在所有单元格被构建完成后调用。
另外，我们注意到，使用了上述的JavaScript代码，单元格属性的初始值经过了计算，但是如果依赖单元格的值发生了变化，不会重新计算公式属性值。为了解决这个问题，需要监听onDependenceCellValueChanged回调函数，这个回调函数会自动分析当前单元格依赖的其他单元格，当依赖的单元格值发生变化时会触发这个回调。所以JavaScript代码的改进版如下：

```auto
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    content = null;
    createContent() {
        this.content = $("<div style='width:100%;height:100%;'></div>");
        return this.content;
    }
    onPageLoaded() {
        const calcFormulaProps = () => {
            const prop = this.CellElement.CellType.MyProperty;
            const result = this.evaluateFormula(prop)
            this.content.text(result)
        }
        calcFormulaProps();
        this.onDependenceCellValueChanged(() => {
            calcFormulaProps();
        })
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

<span class="ne-text">使用onDependenceCellValueChanged有一个弊端：如果单元格上有多个公式属性，任何一个公式属性发生变化，都会触发onDependenceCellValueChanged方法的执行，并且在onDependenceCellValueChanged方法中无法区分具体是哪个属性发生了变化。在活字格 V10.0.0.0 中新增了一个方法onFormulaResultChanged 可以解决上述问题。</span>

```csharp
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    content = null;
    createContent() {
        this.content = $("<div style='width:100%;height:100%;'></div>");
        return this.content;
    }
    onPageLoaded() {
        this.onFormulaResultChanged(this.CellElement.CellType.MyProperty, result => {
            this.content.text(result)
        });
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

>type=warning
> 在V10以后，不再推荐使用 onDependenceCellValueChanged方法，而应该使用 onFormulaResultChanged 方法。代码更简洁，性能更好，并且支持和组件属性绑定。

如果需要更细致的控制，可以通过FormulaPropertyAttribute的其他属性来控制。
**1.提供备选列表。**

1. 设置FormulaPropertyAttribute 的 RecommendedValues 属性。使用“\|”分隔多个候选项。
2. 代码如下：

    ```auto
    public class MyPluginCellType : CellType
        {
            [FormulaProperty(RecommendedValues = "学生|教师|工人")]
            public object MyProperty { get; set; }
        }
    ```
3. 效果如下：
    

**2.支持输入多行文本。**

1. 设置FormulaPropertyAttribute 的 AcceptsReturn 属性。
2. 代码如下：

    ```auto
     public class MyPluginCellType : CellType
        {
            [FormulaProperty(AcceptsReturn = true)]
            public object MyProperty { get; set; }
        }
    ```
3. 效果如下：
    

**3.支持多语言。**

1. 所有公式属性，默认会开启多语言支持，可以通过设置FormulaPropertyAttribute 的 CanSelectResource 属性关闭多语言支持。
2. 代码如下：

    ```csharp
        public class MyPluginCellType : CellType
        {
            [FormulaProperty(CanSelectResource = false)]
            public object MyProperty { get; set; }
        }
    ```
3. 此特性为 10.0.0.0 新增特性。

---

## AttributeValueLinkage

# 属性值联动

## Content

<span class="ne-text">在设计器中，如果一个属性的值希望在另一个属性值变化时自动随之变化，可以通过在XXXDesigner.cs 类中重写 OnPropertyEditorChanged 方法来实现。</span>
<span class="ne-text">下面例子中假设单元格上有两个属性，分别是MyProperty1和MyProperty2，实现的联动效果为 MyProperty1 的值为 true 时， 修改 MyProperty2 值为真， 否则，修改MyProperty2 值为假。</span>
<span class="ne-text">在 MyPluginCellType.cs 修改代码如下：</span>

```auto
using GrapeCity.Forguncy.CellTypes;
using System.ComponentModel;

namespace MyPlugin
{
    [Designer("MyPlugin.Designer.MyPluginCellTypeDesigner, MyPlugin")]
    public class MyPluginCellType : CellType
    {
        public bool MyProperty1 { get; set; }

        public string MyProperty2 { get; set; }
    }
}
```

<span class="ne-text">在 MyPluginCellTypeDesigner.cs 修改代码如下：</span>

```auto
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Plugin;
using System.Collections.Generic;

namespace MyPlugin.Designer
{
    public class MyPluginCellTypeDesigner : CellTypeDesigner<MyPluginCellType>
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

<span class="ne-text">代码说明：</span>
<span class="ne-text">OnPropertyEditorChanged 函数会在单元格的任何属性被修改时被调用。可以通过参数 propertyName 判断当前被修改的属性名， 通过参数 propertyValue 获取最新被修改的值。properties 属性中包含了全部属性列。可以通过操作 properties 里的特定属性实现联动效果。</span>
<span class="ne-text">设计器中的效果：</span>

---

## Initializepropertyvalueswhencreatingcells

# 创建单元格时初始化属性值

## Content

如果单元格的属性只有在新建的时候需要初始化部分属性值（通常用于初始列表、对象、树等复杂结构），可以通过让CellTypeDesigner实现ISupportPropertyInitialize方法。

假设MyPluginCellType 有一个Items属性是一个列表，代码如下：

```
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Plugin;
using System.Collections.Generic;
using System.ComponentModel;

namespace MyPlugin
{
    [Icon("pack://application:,,,/MyPlugin;component/Resources/Icon.png")]
    [Designer("MyPlugin.Designer.MyPluginCellTypeDesigner, MyPlugin")]
    public class MyPluginCellType : CellType
    {
        [ListProperty]
        public List<Item> Items { get; set; } = new List<Item>();
    }
    public class Item : ObjectPropertyBase
    {
        public string Name { get; set; }
    }
}
```

  

在MyPluginCellTypeDesigner，可以通过实现ISupportPropertyInitialize来初始化 Items属性。

```
    public class MyPluginCellTypeDesigner : CellTypeDesigner<MyPluginCellType>, ISupportPropertyInitialize
    {
        public override FrameworkElement GetDrawingControl(ICellInfo cellInfo, IDrawingHelper drawingHelper)
        {
            return new MyPluginCellTypeDrawingControl(this.CellType, cellInfo, drawingHelper);
        }
        public void InitDefaultPropertyValues(IBuilderContext context)
        {
            this.CellType.Items.Add(new Item() { Name = "项目1" });
            this.CellType.Items.Add(new Item() { Name = "项目2" });
            this.CellType.Items.Add(new Item() { Name = "项目3" });
        }
    }
```

---

## Supportcellpermissions

# 支持单元格权限

## Content

可以通过实现 ISupportUIPermission 接口支持单元格权限，支持单元格的可编辑权限需要和 ISupportReadOnly 接口配合， 支持单元格的禁用权限需要和 ISupportDisable 配合。

C#示例代码如下：

```
public class MyPluginCellType : CellType, ISupportDisable, ISupportReadOnly, ISupportUIPermission
    {
        [DisplayName("只读")]
        public bool ReadOnly { get; set; }

        [DisplayName("禁用")]
        public bool IsDisabled { get; set; }

        [DisplayName("单元格权限")]
        public List<UIPermission> UIPermissions { get; set; } = GetDefaultPermission();

        public static List<UIPermission> GetDefaultPermission()
        {
            var defaultAllowRoles = new List<string>() { "FGC_Anonymous" };
            return new List<UIPermission>
            {
                new UIPermission(){ Scope = UIPermissionScope.Enable, AllowRoles = defaultAllowRoles },
                new UIPermission(){ Scope = UIPermissionScope.Editable, AllowRoles = defaultAllowRoles },
                new UIPermission(){ Scope = UIPermissionScope.Visible, AllowRoles = defaultAllowRoles },
            };
        }
    }
```

  

JavaScript 代码可分别参考 [支持只读](第五十四章 活字格插件开发/开发插件/开发单元格插件/开发表单类单元格/支持只读) 和 [支持禁用](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportdisable) 章节。

---

## Supportcellvalues

# 支持单元格值

## Content

表单类单元格一般包含各类输入框，如文本框、选择框、文件上传框等，最主要的目的是通过鼠标键盘交互输入特定类型的值。
这类单元格的最重要功能是与单元格的值双向绑定。
示例代码：
修改 MyPluginCellType.js 文件实现一个简单的输入框。

```auto
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.input = $("<input style='width:100%;height:100%'>");
        this.input.change(() => {
            this.commitValue();
        })
        return this.input;
    }
    setValueToElement(_, value) {
        this.input.val(value?.toString());
    }
    getValueFromElement() {
        return this.input.val();
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

这个双向绑定主要依赖 setValueToElement, getValueFromElement, commit 方法来实现，流程如下图：

1. 当用户通过单元格类型的用户界面键盘输入或鼠标选择后，希望修改单元格的值，以便触发页面公式值重算、数据绑定值更新等。
    
2. 当单元格的值被修改时（通过命令、公式或数据绑定等），单元格类型需要根据新值重新渲染。

---

## Supportdefaultvalue

# 支持默认值

## Content

开发者可以自己添加一个默认值属性，自己处理默认值逻辑，不过这个方法并不推荐。活字格为表单类插件提供了默认值支持。只需让单元格的类型实现 ISupportDefaultValue 接口即可。

```
    public class MyPluginCellType : CellType, ISupportDefaultValue
    {
        [FormulaProperty]
        [DisplayName("默认值")]
        public object DefaultValue { get; set; }

        public bool NeedFormatDefaultValue => false;
    }
```

注意，DefaultValue属性必须标注 \[FormulaProperty\]。

NeedFormatDefaultValue 属性是做什么的？

NeedFormatDefaultValue 返回True，活字格会做智能类型转换，例如DefaultValue输入 111，会保存数字 111，智能转换不一定总是对的，例如用户输入 111,222， 会被自动转为数字 111222 ，因为活字格认为这个逗号是数字的千分位。但是如果多选框多选时，会认为逗号是字符串的分隔符。这种情况让NeedFormatDefaultValue属性返回False是更好的选择。

NeedFormatDefaultValue 返回False，活字格不会做智能类型转换，如果DefaultValue输入111，会保存字符串“111”。

什么时候应该返回 True，什么时候应该返回False？

如果单元格的功能是输入文本的，应该返回False，而用于输入数字、日期时间等，应该返回True。

自定义获取单元格默认值逻辑

有时，单元格的默认值需要根据其他属性来决定。例如单元格有两个属性，默认单位和默认数量。用户需要分别配置，而单元格的默认值需要把默认单位和默认数量拼接起来。

此时，通过实现 ISupportDefaultValue 接口的方式无法实现动态效果。可以通过重写 getDefaultValue 方法实现自定义的默认值逻辑。

C# 代码：

```
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Plugin;

namespace MyPlugin
{
    public class MyPluginCellType : CellType
    {
        [FormulaProperty]
        public object DefaultCount { get; set; } = 10;

        [ComboProperty(ValueList = "个|包|捆|箱")]
        public object DefaultUnit { get; set; } = "包";
    }
}
```

JavaScript 代码：

```
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.input = $("<input style='width:100%;height:100%'>");
        this.input.change(() => {
            this.commitValue();
        })
        return this.input;
    }
    setValueToElement(_, value) {
        this.input.val(value?.toString());
    }
    getValueFromElement() {
        return this.input.val();
    }
    getDefaultValue() {
        const value = this.evaluateFormula(this.CellElement.CellType.DefaultCount) +
            this.evaluateFormula(this.CellElement.CellType.DefaultUnit);
        return {
            Value: value
        };
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

---

## Supportdisable

# 支持禁用

## Content

可以通过实现 ISupportDisable 支持禁用。实现禁用属性的单元格可以和[单元格权限](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportcellpermissions)或设置单元格属性命令集成。

C# 示例代码如下：

```
 public class MyPluginCellType : CellType, ISupportDisable
    {
        [DisplayName("禁用")]
        public bool IsDisabled { get; set; }
    }
```

  

JavaScript 通过重写 disable 与 enable 函数实现禁用效果。

示例代码如下：

```
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.input = $("<input style='width:100%;height:100%'>");
        this.input.change(() => {
            this.commitValue();
        })
        return this.input;
    }
    setValueToElement(_, value) {
        this.input.val(value?.toString());
    }
    getValueFromElement() {
        return this.input.val();
    }
    disable() {
        super.disable();  // 这里必须调用基类方法
        if (this.isDisabled()) { // 这里必须通过isDisabled方法判断是否真正禁用，否则支持单元格权限时会有问题
            this.input.attr("disabled", "disabled")
        }
    }
    enable() {
        super.enable();  // 这里必须调用基类方法
        if (!this.isDisabled()) {  // 这里必须通过isDisabled方法判断是否真正禁用，否则支持单元格权限时会有问题
            this.input.removeAttr("disabled");
        }
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

  

重写 disable enable 方法需要注意：

1.  必须调用 super.disable/enable 方法。
2.  使用 this.isDisabled() 获取真实的禁用状态。

---

## Supportreadonly

# 支持只读

## Content

可以通过实现 ISupportReadOnly 支持只读。实现只读属性的单元格可以和[单元格权限](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportcellpermissions)或设置单元格属性命令集成。

C# 示例代码如下：

```auto
    public class MyPluginCellType : CellType, ISupportReadOnly
    {
        [DisplayName("只读")]
        public bool ReadOnly { get; set; }
    }
```

JavaScript 通过重写 setReadOnly函数实现只读效果。

示例代码如下：

```auto
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.input = $("<input style='width:100%;height:100%'>");
        this.input.change(() => {
            this.commitValue();
        })
        return this.input;
    }
    setValueToElement(_, value) {
        this.input.val(value?.toString());
    }
    getValueFromElement() {
        return this.input.val();
    }
    setReadOnly(value) {
        super.setReadOnly(value); // 这里必须调用基类方法
        if (this.isReadOnly()) { // 这里使用 isReadOnly 方法，而不是 value, 因为有可能因为单元格权限的原因，isReadOnly() 永远为 true
            this.input.attr("readonly", "readonly");
        }
        else {
            this.input.removeAttr("readonly");
        }
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

重写 setReadOnly方法需要注意：

1. 必须调用 super.setReadOnly(value) 方法。
2. 使用 this.isReadOnly() 获取最新的只读状态，而不是通过 value 参数。

---

## Supportvaluechangecommand

# 支持值变更命令

## Content

虽然单元格插件可以通过声明[命令属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/commandproperty)也可以实现值变更命令的效果。但是对于表单类单元格来说，推荐使用更简便的方法，即实现 ICommandCellType接口来实现值变更命令。  
C#示例代码如下。

```
    public class MyPluginCellType : CellType, ICommandCellType
    {
        [DisplayName("值变更命令")]
        public List<Command> CommandList { get; set; }

        public CommandExcuteKind CommandExcuteKind => CommandExcuteKind.OnValueChanged;
    }
```

  

实现了ICommandCellType，并且CommandExcuteKind 返回OnValueChanged，活字格会在单元格值变更时主动调用用户设置的命令，JavaScript不需要为此命令写任何额外的代码，只需[支持单元格值](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportcellvalues)即可。

```
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.input = $("<input style='width:100%;height:100%'>");
        this.input.change(() => {
            this.commitValue();
        })
        return this.input;
    }
    setValueToElement(_, value) {
        this.input.val(value?.toString());
    }
    getValueFromElement() {
        return this.input.val();
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

  

[命令属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/commandproperty) Vs ICommandCellType实现值变更命令。

1.  使用ICommandCellType实现值变更命令无需额外的JavaScript代码。
2.  使用ICommandCellType实现值变更命令原生支持在条件命令中获取“值变更原因”上下文变量。

---

## Converttoformcell

# 改造为表单单元格

## Content

表单单元格可以把编辑的值与数据库的值绑定，进而更新到数据库中。通常表单类单元格需要具备以下功能。详见[开发表单类单元格](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell)。

*   [支持单元格值](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportcellvalues)
*   [支持默认值](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportdefaultvalue)
*   [支持值变更命令](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportvaluechangecommand)
*   [支持数据校验](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportdataverification)
*   [支持只读](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportreadonly)
*   [支持禁用](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportdisable)
*   [支持单元格权限](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportcellpermissions)
*   [支持Tab键顺序](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportstaborder)
*   [支持离开页面时检查是否有未提交的数据](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportcheckuncommitteddatawhenleavingpage)

修改 TinymcePluginCellType.cs 文件：

```
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;
using System.Collections.Generic;
using System.ComponentModel;

namespace TinymcePlugin
{
    [Icon("pack://application:,,,/TinymcePlugin;component/Resources/Icon.png")]
    [Designer("TinymcePlugin.Designer.TinymcePluginCellTypeDesigner, TinymcePlugin")]
    public class TinymcePluginCellType : CellType, ISupportDefaultValue, ICommandCellType, ISupportDataValidation, ISupportUIPermission, ISupportDisable
    {
        [DisplayName("值变更命令")]
        public List<Command> CommandList { get; set; }
        public CommandExcuteKind CommandExcuteKind => CommandExcuteKind.OnValueChanged;

        [DisplayName("数据验证")]
        public DataValidationLink DataValidationLink { get; set; }

        [DisplayName("单元格权限")]
        public List<UIPermission> UIPermissions { get; set; } = GetDefaultPermission();
        public static List<UIPermission> GetDefaultPermission()
        {
            var defaultAllowRoles = new List<string>() { "FGC_Anonymous" };
            return new List<UIPermission>
            {
                new UIPermission(){ Scope = UIPermissionScope.Enable, AllowRoles = defaultAllowRoles },
                new UIPermission(){ Scope = UIPermissionScope.Editable, AllowRoles = defaultAllowRoles },
                new UIPermission(){ Scope = UIPermissionScope.Visible, AllowRoles = defaultAllowRoles },
            };
        }

        [FormulaProperty]
        [DisplayName("默认值")]
        public object DefaultValue { get; set; }
        public bool NeedFormatDefaultValue => false;

        [DisplayName("模式")]
        [RadioGroupProperty(ValueList = "classic|inline|distraction-free", DisplayList = "经典模式|内联模式|沉浸无干扰模式")]
        public string Mode { get; set; } = "classic";

        [CategoryHeader("其他")]
        [DisplayName("禁用")]
        public bool IsDisabled { get; set; }

        public override SupportFeatures SupportFeatures
        {
            get
            {
                return SupportFeatures.ShouldCheckDirtyWhenLeavePage | SupportFeatures.AllowSetTabOrder;
            }
        }

        public override string ToString()
        {
            return "富文本编辑（Tinymce）单元格";
        }
    }
}
```

  

修改TinymcePluginCellType.js如下：

```
/// <reference path="../Declarations/forguncy.d.ts" />
/// <reference path="../Declarations/forguncy.Plugin.d.ts" />

class TinymcePluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.content = $("<div style='width:100%;height:100%'></div>");
        this.content.attr("id", this.ID);
        return this.content;
    }
    async onPageLoaded() {
        const config = {
            target: this.content[0],
            language: 'zh_CN',
            plugins: 'print preview searchreplace autolink directionality visualblocks visualchars fullscreen image link media template code codesample table charmap hr pagebreak nonbreaking anchor insertdatetime advlist lists wordcount textpattern help emoticons',
            toolbar: 'code undo redo | cut copy paste pastetext | forecolor backcolor bold italic underline strikethrough link anchor | alignleft aligncenter alignright alignjustify outdent indent | styleselect formatselect fontselect fontsizeselect | bullist numlist | blockquote subscript superscript removeformat | image media charmap emoticons hr pagebreak insertdatetime print preview | fullscreen | bdmap indent2em lineheight formatpainter axupimgs',
            branding: false,
            setup: (editor) => {
                this.editor = editor;
                editor.on('blur', ()=> {
                    this.commitValue();
                    this.validate();
                });
                editor.on('input', () => {
                    this.hideValidateTooltip();
                });
            }
        };

        if (this.CellElement.CellType.Mode === "inline") {
            config.inline = true;
        }
        else if (this.CellElement.CellType.Mode === "distraction-free") {
            config.inline = true;
            config.toolbar = false;
            config.menubar = false;
        }
        this.tinymce = await tinymce.init(config);
        this.editor.setContent(this.initValue);
        this.content.parent().css("overflow", "");
    }

    setValueToElement(_, value) {
        value = value?.toString() ?? "";
        if (this.editor && this.tinymce) {
            this.editor.setContent(value);
        }
        else {
            this.initValue = value;
        }
    }
    getValueFromElement() {
        return this.editor.getContent();
    }
    disable() {
        super.disable();  
        this.updateDisableReadOnly();
    }
    enable() {
        super.enable(); 
        this.updateDisableReadOnly();
    }
    updateDisableReadOnly() {
        if (!this.editor) {
            return;
        }
        if (this.isDisabled() || this.isReadOnly()) {
            this.editor.mode.set('readonly');
        }
        else {
            this.editor.mode.set('design');
        }
    }
    destroy() {
        if (this.editor) {
            this.editor.destroy();
        }
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("TinymcePlugin.TinymcePluginCellType, TinymcePlugin", TinymcePluginCellType);
```

  

设计器效果：

---

## Vueintegratedcellvalue

# Vue 集成单元格值

## Content

本章节将介绍如何把单元格的值和Vue集成。

### 如果仅用于显示

在data上定义一个普通属性，重写setValueToElement方法，在setValueToElement设置这个属性即可。

```
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.content = $("<div/>");
        return this.content;
    }
    onPageLoaded() {
        const uid = "uid-" + new Date().valueOf();
        const self = this;
        this.content.attr("id", uid);
        const option = {
            template:
  `<button>{{text}}</button>`,
            data() {
                return {
                    text: ""
                }
            }
        };
        option.beforeCreate = function () {
            self.vue = this;
        };
        this.vueApp = Vue.createApp(option);
        this.vueApp.mount(`#${uid}`);
    }
    setValueToElement(_, value) {
        this.vue.text = value?.toString();
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

### 双向绑定实现编辑

VUE 支持通过 v-model 双向绑定受控组件（通常是表单控件），对于此类组件，可以实现对单元格值的编辑。代码如下：

```
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.content = $("<div/>");
        return this.content;
    }
    onPageLoaded() {
        const uid = "uid-" + new Date().valueOf();
        const self = this;
        this.content.attr("id", uid);
        const option = {
            template:
  `<input v-model="text" @change="handleChange">`,
            data() {
                return {
                    text: ""
                }
            },
            methods: {
                handleChange() {
                    self.commitValue();
                }
            }
        };
        option.beforeCreate = function () {
            self.vue = this;
        };
        this.vueApp = Vue.createApp(option);
        this.vueApp.mount(`#${uid}`);
    }
    setValueToElement(_, value) {
        this.vue.text = value?.toString();
    }
    getValueFromElement() {
        return this.vue.text;
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```