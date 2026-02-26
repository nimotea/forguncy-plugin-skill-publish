# System Integration

## Dropdownlistproperty

# 下拉列表属性

## Content

如果属性的类型是字符串，默认属性值是可以接受任意字符串的，如果希望提供字符串值候选列表，可以通过标注ComboPropertyAttribute 的并设置ValueList属性的方式实现。多值个值用“\|”分隔。
注意，标注ComboPropertyAttribute的属性类型必须是 string。

```auto
        public class MyPluginCellType : CellType
    {
        [ComboProperty(ValueList = "Student|Teacher|Worker")]
        public string MyProperty { get; set; }
    }
```

在设计器中效果如下：

如果需要更细致的控制，可以通过ComboPropertyAttribute的其他属性来控制。
**1\. 值与显示值不同。**

1. 设置ComboPropertyAttribute 的 DisplayList 属性。
2. 代码：

    ```auto
        public class MyPluginCellType : CellType
        {
            [ComboProperty(ValueList = "Student|Teacher|Worker", DisplayList ="学生|教师|工人")]
            public string MyProperty { get; set; }
        }
    ```
3. 效果：
    
4. 其他说明：
    此方法可以使用户在选择时选择中文选项，而单元格实际保存值为英文，方便程序处理。ValueList和DisplayList通过数量和顺序匹配。如果DisplayList数量超出ValueList数量，多出部分会被忽略；如果DisplayList数量少于ValueList数量，不足部分会使用ValueList对应的值。

**2.** **允许用户使用列表以外的值。**

1. 设置ComboPropertyAttribute 的 IsSelectOnly属性。
2. 代码：

    ```auto
        public class MyPluginCellType : CellType
        {
            [ComboProperty(ValueList = "Student|Teacher|Worker", IsSelectOnly = false)]
            public string MyProperty { get; set; }
        }
    ```
3. 效果：
    
4. 注意：
    IsSelectOnly 为 False 时，DisplayList 设置会被忽略。不填时 IsSelectOnly 属性的默认值为 True。

**3.** **支持搜索。**

1. 设置ComboPropertyAttribute 的 Searchable 属性。
2. 代码：

    ```auto
        public class MyPluginCellType : CellType
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

有时，下拉列表中的选项不是开发时决定的，而是动态生成，例如下拉打印机列表。可以通过重写CellType的Designer 通过代码动态生成列表。

```auto
    [Designer("MyPlugin.Designer.MyPluginCellTypeDesigner, MyPlugin")]
    public class MyPluginCellType : CellType
    {
        public string MyProperty { get; set; }
    }

    public class MyPluginCellTypeDesigner : CellTypeDesigner<MyPluginCellType>
    {
        public override EditorSetting GetEditorSetting(PropertyDescriptor property, IBuilderContext builderContext)
        {
            if (property.Name == nameof(MyPluginCellType.MyProperty))
            {
                var list = new string[] { "aaa", "bbb", "ccc" };
                return new ComboEditorSetting(list);
            }
            return base.GetEditorSetting(property, builderContext);
        }
    }
```

如果希望下拉列表的显示值和选择后保存的值不一样，可以如下修改 GetEditorSetting 方法，让List的每一项不是字符串，而是一个对象。通过设置 ComboEditorSetting 的 displayMember和valueMember来指定对象的哪个属性用于显示，哪个属性用于保存值。

```auto
    public class MyPluginCellTypeDesigner : CellTypeDesigner<MyPluginCellType>
    {
        public override EditorSetting GetEditorSetting(PropertyDescriptor property, IBuilderContext builderContext)
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

```csharp
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Plugin;
using System.Collections.Generic;

namespace MyPlugin
{
    public class MyPluginCellType : CellType
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
下面例子中，额外声明了两个属性分别使用公式编辑器和命令编辑器。具体标注的用法请参考之前的章节。

```csharp
    public class MyPluginCellType : CellType
    {
        [ListProperty]
        public List<MyObj> MyProperty { get; set; }
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

如果需要更细致的控制，可以通过ListPropertyAttribute的其他属性来控制。
**1.控制列表最大或最小元素个数。**

1. 设置ListPropertyAttribute 的 MaxCount 和 MinCount 属性。
2. 代码如下：

    ```csharp
        public class MyPluginCellType : CellType
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

    ```auto
        public class MyPluginCellType : CellType
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

    ```auto
        public class MyPluginCellType : CellType
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

1. <span class="ne-text">给属性添加ListPropertyItemSettingAttribute 的 IsUnique 属性。</span>
2. <span class="ne-text">代码如下：</span>

    ```auto
        public class MyPluginCellType : CellType
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
        public class MyPluginCellType : CellType
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

1. ItemType属性里声明的类型必须与项目属性类型一致；
2. 自定义对象必须实现 INamedObject 接口；
3. 属性的返回值必须是 List；
4. 自定义对象的类型应该从 ObjectPropertyBase 类派生，以确保在单元格复制的时候，子属性可以被正确的深克隆（ObjectPropertyBase实现了默认的深克隆逻辑）。

```
    public class MyPluginCellType : CellType
    {
        [ObjectListProperty(ItemType = typeof(MyObj))]
        public List<INamedObject> MyProperty { get; set; }
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
public class MyPluginCellType : CellType
    {
        [ObjectListProperty(ItemType = typeof(MyObj))]
        public List<INamedObject> MyProperty { get; set; }
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
**1.** 控制列表最大元素个数

1. 设置ObjectListPropertyAttribute 的 MaxCount 属性
2. 代码

    ```
        public class MyPluginCellType : CellType
        {
            [ObjectListProperty(ItemType = typeof(MyObj), MaxCount = 4)]
            public List<INamedObject> MyProperty { get; set; }
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

**2.** 控制默认结点名称

1. 设置ObjectListPropertyAttribute 的 DefaultName 属性。
2. 代码：

    ```
     public class MyPluginCellType : CellType
        {
            [ObjectListProperty(ItemType = typeof(MyObj), DefaultName = "结点")]
            public List<INamedObject> MyProperty { get; set; }
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

**ListProperty Vs ObjectListProperty**
ListPropertyAttribute和ObjectListPropertyAttribute解决的是完全相同的问题，只是表现方式不同，ObjectListPropertyAttribute 更适合项目子属性比较多的情况，而ListProperty则在子属性比较少的时候比较适用。

---

## Celllifecycle

# 单元格生命周期

## Content

每个单元格插件都包含“生命周期方法”，你可以重写这些方法，以便于在运行过程中特定的阶段执行这些方法。

单元格的生命周期调用顺序如下：

1. constructor()
2. createContent()
3. onPageLoaded()
4. destroy()

构造函数：constructor()

单元格类型被构造时调用，这个生命周期很少被使用到，偶尔用于初始化一下数据，没有特别的原因不推荐重写构造函数，如果重写，务必调用 super(...arguments) 来确保默认构造函数逻辑正确。

```
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    constructor() {
        super(...arguments);
        this.initData = "test";
    }
    createContent() {
        return $(`<div>${this.initData}</div>`);
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

构建Dom结构 createContent()
大部分单元格会使用这个生命周期函数，用于创建单元格的Dom结构。活字格页面会按顺序调用每一个单元格的 createContent(), 这个函数需要返回一个Jquery 对象表示单元格的根 Dom 节点。活字格会把这个Dom节点挂入活字格的页面上。 在这个函数中，可以通过 this.CellElement.CellType.【属性名】获取单元格在设计时设置的属性值，也可以通过 this.CellElement.StyleInfo 获取单元格的样式设置。

```
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const prop = this.CellElement.CellType.MyProperty;
        const color = this.CellElement.StyleInfo.Foreground;
        const cssColor = Forguncy.ConvertToCssColor(color);
        return $(`<div style='color:${cssColor}'>${prop}</div>`);
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

页面加载完成onPageLoaded()

页面加载完成，会在页面数据初始化完成是调用。在页面初始化完成前，使用 this.evaluateFormula() 方法计算公式值，如果公式依赖了其他单元格的名称，可能会导致公式计算结果不正确。所以如果需要使用 this.evaluateFormula() 方法应该在这个函数中使用。

有些第三方类库在初始化时要求Dom必须已经挂载到Dom树上了，这种情况也应该把初始化逻辑写到 onPageLoaded 而不是 createContent中，因为createContent创建的Dom并没有挂载到Dom树上。

```
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

单元格销毁destroy()

页面跳转导致离开当前页面，或者关闭弹出页面时，之前页面上所有单元格会调用destory()方法，常用于解除全局事件绑定。

关于 onLoad 函数

onLoad是活字格早期版本的生命周期，调用时机是所有单元格的Dom已经挂载到了Dom树上，但是页面的数据，计算引擎等没有初始化完成的时机。设计初衷是为了解决第三方类库必须在Dom挂载后才能调用初始函数的问题。在新版活字格中，这个生命周期可以完全被onPageLoaded取代，不建议继续使用。

活字格目前没有计划删除 onLoad 函数，以便于确保对旧版本插件的兼容性。

---

## IntegrateCellPluginToListview

# 集成单元格插件到表格中

## Content

此特性为V11.0.100.0新增特性。

#### 活字格的表格

在活字格中，默认表格由葡萄城 [SpreadJS](https://www.grapecity.com.cn/developer/spreadjs){:target="_blank"} 表格控件驱动，底层采用 Canvas 进行渲染。
这一架构决定了单元格扩展方式与传统 DOM 表格截然不同：

* 列级实例：SpreadJS 以“列”为粒度创建单元格类型实例。
* 行级绘制：运行时会遍历该列所有行，针对每一行调用一次 paint 方法完成渲染。

因此，想要开发可嵌入表格的自定义单元格，只需关注 paint 方法：通过解析上下文和数据，让同一实例在不同行呈现差异化外观。

#### 开发集成到表格中的单元格插件

接下来，会以状态显示单元格为例，一步一步开发一个可以嵌入到表格中的单元格插件
首先，我们先创建一个普通的单元格插件。我会创建一个状态显示单元格。需求非常简单：单元格会显示三种状态——警告、错误、正常。

1. 正常状态，单元格会显示一个绿色圆点和文本
2. 警告状态，单元格会显示一个黄色圆点和文本
3. 错误状态，单元格会显示一个红色圆点和文本

单元格值为 1 时表示警告，2 时表示错误，其他情况表示正常

1. 使用活字格插件构建器构建“State”单元格插件。
    
2. 修改 StateCellType.cs 文件如下。

```csharp
    [Designer("State.Designer.StateCellTypeDesigner, State")]
    public class StateCellType : CellType
    {
        public override string ToString()
        {
            return "状态显示单元格";
        }
    }
```

3. 修改 Resources/StateCellType.js

```javascript
/// <reference path="../Declarations/forguncy.d.ts" />
/// <reference path="../Declarations/forguncy.Plugin.d.ts" />

class StateCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const container = $("<div style='display:flex;align-items:baseline;gap:3px'></div>");
        this.point = $("<div style='width:10px;height:10px;border-radius:10px;'></div>");
        this.label = $("<span>")
        container.append(this.point)
        container.append(this.label)
        this.updateStyle()
        return container;
    }

    setValueToElement(_, value) {
        this.updateStyle(value)
    }

    updateStyle(value) {
        const state = this.getState(value)
        this.point.css("background", state.color)
        this.label.text(state.text)
    }

    getState(value) {
        switch (value?.toString()) {
            case "1":
                return {
                    color: 'yellow',
                    text: '警告'
                }
            case "2":
                return {
                    color: 'red',
                    text: '错误'
                }
            default:
                return {
                    color: 'green',
                    text: '正常'
                }
        }
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("State.StateCellType, State", StateCellType);
```

4. 查看运行时效果
    正常
    
    警告
    
    错误
    

到此，准备工作结束，我们已经用之前的支持开发了一个普通单元格插件。此时，如果放到表格中。你会发现，这个单元格没有显示预期的状态

接下来，改写 Resources/StateCellType.js 如下，核心是添加了paintInListView 方法。

```javascript
/// <reference path="../Declarations/forguncy.d.ts" />
/// <reference path="../Declarations/forguncy.Plugin.d.ts" />

class StateCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const container = $("<div style='display:flex;align-items:baseline;gap:3px'></div>");
        this.point = $("<div style='width:10px;height:10px;border-radius:10px;'></div>");
        this.label = $("<span>")
        container.append(this.point)
        container.append(this.label)
        this.updateStyle()
        return container;
    }

    setValueToElement(_, value) {
        this.updateStyle(value)
    }

    updateStyle(value) {
        const state = this.getState(value)
        this.point.css("background", state.color)
        this.label.text(state.text)
    }

    getState(value) {
        switch (value?.toString()) {
            case "1":
                return {
                    color: 'yellow',
                    text: '警告'
                }
            case "2":
                return {
                    color: 'red',
                    text: '错误'
                }
            default:
                return {
                    color: 'green',
                    text: '正常'
                }
        }
    }

    paintInListView(ctx, value, cellRect, cellStyle, context) {
        const state = this.getState(value);

        const dotRadius = 5;
        const dotX = cellRect.x + dotRadius;  
        const dotY = cellRect.y + cellRect.height / 2;

        // 画圆点
        ctx.beginPath();
        ctx.arc(dotX, dotY, dotRadius, 0, Math.PI * 2);
        ctx.fillStyle = state.color;
        ctx.fill();

        // 画文字（右边 3 像素间距）
        const textX = dotX + dotRadius + 3;
        const textY = dotY;
        ctx.font = '14px 微软雅黑';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = '#000';
        ctx.fillText(state.text, textX, textY);
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("State.StateCellType, State", StateCellType);
```

此时，再次运行，效果如下：

到此，我们已经成功实现了一个可以在表格中使用的单元格插件。
当然，在表格中的单元格插件远不止于此，接下来的章节将逐一介绍单元格更多功能。

1. [表格中实现鼠标交互](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/integrate-cell-plugin-to-listview/mouse-interaction-in-listview)
2. [表格中实现直接点击编辑](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/integrate-cell-plugin-to-listview/click-to-edit-in-listview)
3. [表格中实现双击编辑](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/integrate-cell-plugin-to-listview/doubleclick-to-edit-in-listview)
    1. [表格编辑常见问题及解决方案](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/integrate-cell-plugin-to-listview/doubleclick-to-edit-in-listview/issues-and-solutions)

---

## SupportImageUpload

# 支持图片上传

## Content

如果单元需要支持图片上传，需要添加代码。
1.在UploadImageDemoCellType.cs 文件中添加如下代码：

```csharp
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Plugin;
using System.ComponentModel;

namespace UploadImageDemo
{
    [Designer("UploadImageDemo.Designer.UploadImageDemoCellTypeDesigner, UploadImageDemo")]
    public class UploadImageDemoCellType : CellType
    {
        [DisplayName("上传的文件类型")]
        public string accept { get; set; }

        [Browsable(false)]
        [SaveJsonIgnore]
        [ServerProperty]
        public UploadLimit UploadLimit
        {
            get
            {
                return new UploadLimit()
                {
                    ExtensionFilter = this.accept,
                };
            }
        }
    }
    public class UploadLimit : IUploadLimit
    {
        public UploadLimit()
        {
            ExtensionFilter = "";
            SizeLimit = 0;
        }
        [DefaultValue("")]
        public string ExtensionFilter { get; set; }

        [DefaultValue(0d)]
        public double SizeLimit { get; set; }
    }
}
```

2.在UploadImageDemoCellTypeDesigner.cs 文件中添加如下代码：

```auto
using GrapeCity.Forguncy.CellTypes;
namespace UploadImageDemo.Designer
{
    public class UploadImageDemoCellTypeDesigner : CellTypeDesigner<UploadImageDemoCellType>, ISupportPropertyInitialize
    {
        public void InitDefaultPropertyValues(IBuilderContext context)
        {
            this.CellType.accept = ".jpg,.jpeg,.png";
        }
    }
}
```

>type=note
> 说明：
> 处于安全性能考虑，上传文件必须限制文件的扩展名。通过添加属性 UploadLimit 实现，属性 UploadLimit 必须添加 [ServerProperty] 标注，并且类型必须是实现了 IUploadLimit 接口的类。

在设计器中效果如下：

3.UploadImageDemoCellType.js 代码如下：

```javascript
/// <reference path="../Declarations/forguncy.d.ts" />
/// <reference path="../Declarations/forguncy.Plugin.d.ts" />
class UploadImageDemoCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        // 获取MyProperty属性值，注意，这里的MyProperty应该与 UploadImageDemoCellType.cs 文件定义的属性名一致
        const accept = this.CellElement.CellType.accept;
        const uploadLimitId = this.CellElement.ServerPropertiesId.UploadLimit;

        const div = $("<div style='width:100%;height:100%'></div>")
        const file = $("<input type='file'>");
        const img = $("<img style='width:100px;height:100px'/>");

        file.on("change", e => {
            const value = file.val();
            if (value) {
                const files = file[0].files;
                const fileData = files[0];
                const successCallback = (fileName) => {
                    const root = Forguncy.Helper.SpecialPath.getBaseUrl();
                    img[0].src = root + Forguncy.ModuleLoader.getCdnUrl("FileDownloadUpload/Download?file=" + encodeURIComponent(fileName));
                };
                const errorCallback = (e) => {
                    alert(e);
                };
                Forguncy.Common.uploadImageToServer(fileData, null, accept, successCallback, errorCallback, undefined, uploadLimitId);
            }
        });

        div.append(file);
        div.append(img);

        return div;
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("UploadImageDemo.UploadImageDemoCellType, UploadImageDemo", UploadImageDemoCellType);
```

>type=note
> 代码说明：
> 使用 Forguncy.Common.uploadImageToServer 方法可以上传图片。参数如下:
> uploadImageToServer(file: File, uploadImageLimit: UploadImageLimit, extensionFilter: string, successCallback: Function, errorCallback?: Function, beginUpload?: Function, uploadImageLimitId?: string)
> 通过 successCallback 成功回调，可以获取上传后，在服务器端的文件名。这个文件名可以保持到数据的附件或图片列中。
> 注意：返回的图片需要保存到数据库中。如果上传的文件没有被保存到数据库中，图片会被临时保存，并在24小时内被清除。

在浏览器中的效果：

---

## SupportcellTypeStyleRoot

# 支持单元格样式

## Content

*   [支持 单元格样式](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/supportcell-type-style-root/supportcelltypestyle)
*   [支持单元格模板样式](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/supportcell-type-style-root/supportcelltemplatestyle)

---

## ClickToEditInListview

# 表格中实现直接点击编辑

## Content

插件单元格可以实现点击特定位置的时候修改表格单元格的值。
首先，需要单元格在 C# 定义中声明支持编辑。示例代码如下：

```csharp
    public class StateCellType : CellType
    {
        public override ListViewOptions ListViewOptions
        {
            get
            {
                return new ListViewOptions()
                {
                    AllowEdit = true
                };
            }
        }

        public override string ToString()
        {
            return "状态显示单元格";
        }
    }
```

修改 [表格中实现鼠标交互](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/integrate-cell-plugin-to-listview/mouse-interaction-in-listview) 例子中的JavaScript的代码的 onClickInListView 函数如下：

```javascript
onClickInListView(hitInfo, context) {
  if (context.cellState.isReadOnly ||
      context.cellState.isDisabled) {
    return;
  }
  if (hitInfo?.type === 'Dot') {
    context.value = (Number(context.value ?? 0) + 1) % 3;
    return;
  }
}
```

在设计器中，开启Listview 允许编辑：

效果如下：

---

## DoubleclickToEditInListview

# 表格中实现双击编辑

## Content

除了[直接点击编辑](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/integrate-cell-plugin-to-listview/click-to-edit-in-listview)，很多情况下，在表格中的编辑是用户首先要通过双击单元格，此时单元格会从显示模式切换到编辑模式。编辑模式通常为输入框、选择器等。用户可以在编辑模式下，修改编辑框的值。当用户点击单元格外切换焦点或选择时，原单元格会切换回显示模式，并使用编辑框值替换单元格的值，完成一次编辑。

1. 显示状态：通过 paintInListView 方法实现
2. 编辑状态：通过复用普通模式下的 createContent 方法实现
    1. 生命周期如下
        1. 用户选择单元格
            1. createContent ，创建 DOM
            2. setValueToElement ，用单元格的值初始化编辑状态 DOM 的值
            3. onPageLoaded ，处理加载后逻辑
            4. setFocus ，初始化焦点
            5. moveCursorToEnd 控制光标初始位置
            6. selectAll 控制初始全选状态
    2. 用户双击或 F2 等切换到编辑模式
        1. setBackColor， 初始化编辑器的背景色
        2. setFontStyle，初始化编辑器的字体设置
        3. onEditStartInListView，编辑开始通知
        4. setValueToElement，用单元格的值初始化编辑状态 DOM 的值
        5. setFocus，初始化焦点
        6. moveCursorToEnd，控制光标初始位置
    3. 用户点击表格外或其他单元格值时，开始退出编辑状态
        1. getValueFromElement，获取用户修改的值，校验并保存到表格中
        2. onEditEndInListView，编辑结束通知
        3. onDestroyInListView，销毁DOM

要实现通过编辑模式编辑，首先需要在 C# 代码中声明支持编辑模式及各种细节的配置。
示例代码如下：

```csharp
    public class StateCellType : CellType
    {
        public override ListViewOptions ListViewOptions
        {
            get
            {
                return new ListViewOptions()
                {
                    AllowEdit = true,
                    AllowEnterEditMode = true,
                };
            }
        }

        public override string ToString()
        {
            return "状态显示单元格";
        }
    }
```

JavaScript 代码：

```javascript
/// <reference path="../Declarations/forguncy.d.ts" />
/// <reference path="../Declarations/forguncy.Plugin.d.ts" />

class StateCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const container = $("<div style='display:flex;align-items:baseline;gap:6px'></div>");
        this.point = $("<div style='width:10px;height:10px;border-radius:10px;'></div>");
        this.select = $(`
<select>
  <option value="0">正常</option>
  <option value="1">警告</option>
  <option value="2">错误</option>
</select > `)
        this.select.attr('id', this.ID); 
        this.select.on('change', () => {
            this.updateStyle(this.select.val())
        })
        container.append(this.point)
        container.append(this.select)
        this.updateStyle()
        return container;
    }

    setValueToElement(_, value) {
        this.updateStyle(value)
    }

    getValueFromElement() {
        return this.select.val()
    }

    updateStyle(value) {
        const state = this.getState(value)
        this.point.css("background", state.color)
        this.select.val(value ?? 0)
    }

    getState(value) {
        switch (value?.toString()) {
            case "1":
                return {
                    color: 'yellow',
                    text: '警告'
                }
            case "2":
                return {
                    color: 'red',
                    text: '错误'
                }
            default:
                return {
                    color: 'green',
                    text: '正常'
                }
        }
    }

    paintInListView(ctx, value, cellRect, cellStyle, context) {
        const state = this.getState(value);

        let dotRadius = 5;
        const dotX = cellRect.x + dotRadius;
        const dotY = cellRect.y + cellRect.height / 2;

        // 画圆点
        ctx.beginPath();
        ctx.arc(dotX, dotY, dotRadius, 0, Math.PI * 2);

        ctx.fillStyle = state.color;

        ctx.fill();

        // 画文字（右边 3 像素间距）
        const textX = dotX + dotRadius + 6;
        const textY = dotY;
        ctx.font = '14px 微软雅黑';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = '#000';
        ctx.fillText(state.text, textX, textY);
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("State.StateCellType, State", StateCellType);
```

代码说明：

1. 添加 getValueFromElement 方法，允许表格获取编辑状态下单元格编辑后的值
2. this.select.attr('id', this.ID); 给最主要的 DOM 设置 ID，表格会根据这个ID自动执行一些逻辑。例如设置焦点到默认 ID 的 DOM 上。

运行时效果如下：

---

## MouseInteractionInListview

# 表格中实现鼠标交互

## Content

<span class="ne-text">处理表格中的单元格交互行为，核心是处理单元格的 onMouseMoveInListView，onMouseLeaveInListView, onMouseDownInListView，onMouseUpInListView，onClickInListView 以及 getHitTestTypeInListView 方法来定制鼠标键盘行为。</span>
<span class="ne-text">工作原理：</span>
<span class="ne-text">在 onMouseMoveInListView，onMouseDownInListView 等函数执行前会执行 getHitTestTypeInListView 方法用当前鼠标位置进行点击检测。可以通过返回字符串或者JSON对象来区分单元格中不同的位置。如果 getHitTestTypeInListView 返回值不同，会触发 paintInListView 方法，从而重新渲染。</span>
<span class="ne-text">示例代码：</span>

```javascript
/// <reference path="../Declarations/forguncy.d.ts" />
/// <reference path="../Declarations/forguncy.Plugin.d.ts" />

class StateCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const container = $("<div style='display:flex;align-items:baseline;gap:3px'></div>");
        this.point = $("<div style='width:10px;height:10px;border-radius:10px;'></div>");
        this.label = $("<span></span>")
        container.append(this.point)
        container.append(this.label)
        this.updateStyle()
        return container;
    }

    setValueToElement(_, value) {
        this.updateStyle(value)
    }

    updateStyle(value) {
        const state = this.getState(value)
        this.point.css("background", state.color)
        this.label.text(state.text)
    }

    getState(value) {
        switch (value?.toString()) {
            case "1":
                return {
                    color: 'yellow',
                    text: '警告'
                }
            case "2":
                return {
                    color: 'red',
                    text: '错误'
                }
            default:
                return {
                    color: 'green',
                    text: '正常'
                }
        }
    }

    paintInListView(ctx, value, cellRect, cellStyle, context) {
        const state = this.getState(value);

        let dotRadius = 5;
        const dotX = cellRect.x + dotRadius;
        const dotY = cellRect.y + cellRect.height / 2;

        // 画圆点
        ctx.beginPath();
        ctx.arc(dotX, dotY, dotRadius, 0, Math.PI * 2);

        ctx.fillStyle = state.color;

        if (context.rowIndex === this._hoverRowIndex && this._hoverType === 'Dot') {
            ctx.globalAlpha = 0.4
        }

        ctx.fill();

        ctx.globalAlpha = 1

        // 画文字（右边 3 像素间距）
        const textX = dotX + dotRadius + 3;
        const textY = dotY;
        ctx.font = '14px 微软雅黑';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = '#000';
        ctx.fillText(state.text, textX, textY);
    }

    getHitTestTypeInListView(x, y, cellRect, ctx) {
        const dotRadius = 5;
        const dotX = cellRect.x + dotRadius;
        const dotY = cellRect.y + cellRect.height / 2;
        const dx = x - dotX;
        const dy = y - dotY;
        if (dx * dx + dy * dy <= dotRadius * dotRadius) {
            return 'Dot';
        }
        return null;   // 未命中
    }
    onMouseMoveInListView(hitInfo, context) {
        if (hitInfo?.type === 'Dot') {
            context.cursor = 'pointer';
            this._hoverRowIndex = context.rowIndex;
            this._hoverType = hitInfo.type;
        }
        else {
            this._hoverType = null;
            this._hoverRowIndex = undefined;
        }
        super.onMouseMoveInListView(hitInfo, context);
    }
    onMouseLeaveInListView(hitInfo, context) {
        this._hoverType = null;
        this._hoverRowIndex = undefined;
        super.onMouseLeaveInListView(hitInfo, context);
    }

    onClickInListView(hitInfo, context) {
        if (hitInfo?.type === 'Dot') {
            console.log("表示状态的圆点被点击")
            return;
        }
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("State.StateCellType, State", StateCellType);
```

<span class="ne-text">效果如下：</span>

<span class="ne-text">代码说明：</span>

1. <span class="ne-text">getHitTestTypeInListView 方法检查指定坐标位置是否落在了圆点上；</span>
2. <span class="ne-text">onMouseMoveInListView 缓存最近一次 HitTest 的结果；</span>
3. <span class="ne-text">paintInListView 判断 hoverIndex 是否与当前渲染行一致且鼠标悬停在圆点上，则使用 40% 透明度重新渲染圆点，以提供用户反馈；</span>
4. <span class="ne-text">onMouseLeaveInListView 方法清空悬停信息；</span>
5. <span class="ne-text">onClickInListView 做自定义处理。</span>

>type=warning
> **<span class="ne-text">注意：</span>**
> <span class="ne-text">getHitTestTypeInListView 返回空的部分是不响应 onClickInListView 事件的。</span>

---

## SupportComplexCellStyles

# 支持复杂类型的单元格格式

## Content

对于文本输入框、按钮等普通的单元格类型，您可以直接使用 [支持单元格样式](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/supportcell-type-style-root/supportcelltypestyle) 功能实现单元格样式功能。
但是有些复杂类型的单元格，比如表格、树等同一个单元格类型内，需要对不同的模块分别设置单元格样式，就需要使用到本章方式了。
本例以一个表格单元格的Demo代码为例，说明如何在表格上，分别为列头和列以及其他列设置单元格格式。

如上图所示，单元格类型可以为多个列以及同一个列的列头和列内容分别设置单元格格式，上述示例的代码如下所示：

```auto
[Icon("pack://application:,,,/Test;component/Resources/Icon.png")]
[Designer("Test.Designer.TestTableCellTypeDesigner, Test")]
public class TestTableCellType : CellType
{
    [DisplayName("列设置")]
    [ObjectListProperty(ItemType = typeof(TestTableColumnConfig), DefaultName = "列")]
    public List<INamedObject> Columns { get; set; } = new List<INamedObject>();
}

public class TestTableColumnConfig : ObjectPropertyBase, INamedObject
{
    public string Name { get; set; }

    [DisplayName("列头样式")]
    [CellFormatSetting]
    public ForguncyStyleInfo HeaderStyleFormat { get; set; }

    [DisplayName("列样式")]
    [CellFormatSetting]
    public ForguncyStyleInfo StyleFormat { get; set; }
}
```

您可以使用 ObjectListProperty类型的属性作为表格的列定义，然后在属性内，使用 ForguncyStyleInfo类型的子属性定义每一个列的单元格格式信息，从而实现为一个复杂类型的单元格类型中的不同模块分别设置单元格格式功能。
1.FormatTabType：表示单元格格式设置所支持的Tab栏类型，默认为 PluginFormatDialogTabType.Normal 表示全部开启。您可以如下配置所示隐藏 数字Tab栏：

```csharp
[Icon("pack://application:,,,/Test;component/Resources/Icon.png")]
[Designer("Test.Designer.TestTableCellTypeDesigner, Test")]
public class TestTableCellType : CellType
{
    [DisplayName("列设置")]
    [ObjectListProperty(ItemType = typeof(TestTableColumnConfig), DefaultName = "列")]
    public List<INamedObject> Columns { get; set; } = new List<INamedObject>();
}

public class TestTableColumnConfig : ObjectPropertyBase, INamedObject
{
    public string Name { get; set; }

    [DisplayName("列头样式")]
    [CellFormatSetting(
        FormatTabType = PluginFormatDialogTabType.Normal ^ PluginFormatDialogTabType.Number)]
    public ForguncyStyleInfo HeaderStyleFormat { get; set; }
}
```

2.AlignmentFormatOptions：表示对齐设置Tab栏中支持的配置项，默认值为 PluginAlignmentFormatOptions.All 表示全部开启。您可以如下配置所示隐藏 水平对齐设置项：

```csharp
[Icon("pack://application:,,,/Test;component/Resources/Icon.png")]
[Designer("Test.Designer.TestTableCellTypeDesigner, Test")]
public class TestTableCellType : CellType
{
    [DisplayName("列设置")]
    [ObjectListProperty(ItemType = typeof(TestTableColumnConfig), DefaultName = "列")]
    public List<INamedObject> Columns { get; set; } = new List<INamedObject>();
}

public class TestTableColumnConfig : ObjectPropertyBase, INamedObject
{
    public string Name { get; set; }

    [DisplayName("列头样式")]
    [CellFormatSetting(
        AlignmentFormatOptions = PluginAlignmentFormatOptions.All ^ PluginAlignmentFormatOptions.HorizontalAlignment)]
    public ForguncyStyleInfo HeaderStyleFormat { get; set; }
}
```

单元格格式的返回值最终会保存在 ForguncyStyleInfo类型的属性中，此类型的各个字段的意思分别是：

| **属性名** | **说明** | **类型** |
| --- | --- | --- |
| BackgroundStr | 背景颜色 | string 类型 |
| BorderLeft | 左边框 | @rows=4:ForguncyBorderLine类型，包含两个属性：<ol><li>ColorStr，字符串类型，表示边框颜色</li><li>ForguncyBorderLineStyle，枚举类型，表示边框线性</li></ol> |
| BorderTop | 上边框 |
| BorderRight | 右边框 |
| BorderBottom | 下边框 |
| FontFamily | 字体 | string 类型 |
| FontSize | 字号 | string 类型 |
| FontStyle | 字体倾斜 | string 类型 |
| FontWeight | 字体加粗 | string 类型 |
| ForegroundStr | 字体颜色 | string 类型 |
| FormatString | 数字格式字符串 | string 类型 |
| Strikethrough | 是否右删除线 | bool 类型 |
| TextIndent | 缩进 | int 类型 |
| Underline | 是否有下划线 | bool 类型 |
| WordWrap | 是否可以自动换行 | bool 类型 |
| ShrinkToFit | 是否自动字体缩小填充 | bool 类型 |
| Ellipsis | 超出文本是否展示省略号 | bool 类型 |
| HorizontalAlignment | 水平对齐方式 | @rows=2:ForguncyCellHorizontalAlignment枚举类型 |
| VerticalAlignment | 垂直对齐方式 |
| DisplayTab | 打开后默认的展示Tab栏 | PluginFormatDialogTabType枚举类型 |

通过上述配置，您在运行时就可得到如下所示的配置对象。

```javascript
{
"backgroundStr": "Accent 6 40",
"fontFamily": "Body",
"fontSize": 18.666666666666664,
"fontWeight": "bold",
"strikethrough": false,
"textIndent": 0,
"underline": false,
"wordWrap": false,
"shrinkToFit": false,
"ellipsis": false,
"horizontalAlignment": 1,
"verticalAlignment": 1
}
```

在运行时，您需要将上述设置时的参数自行解析为前端的样式，根据前端的框架不同，设置的方式可能各有不同。
需要注意以下三点：
1\. 格式设置的属性必须为 ForguncyStyleInfo 类型；
2\. 运行时的参数是以小驼峰的形式传递的；
3\. 此特性为 10\.0\.100\.0 版本新增。

---

## Supportcelltemplatestyle

# 支持单元格模板样式

## Content

单元格模板样式是值单元格类型提前配置好的一组样式以方便使用者配置或复用。如下图：

单元格插件可以通过实现 IStyleTemplateSupport 接口和自定义 CellTypeStyleTemplateSupportAttribute 来实现。

修改MyPluginCellType.cs文件：

```
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Plugin;
using System;
using System.Collections.Generic;
using System.ComponentModel;

namespace MyPlugin
{
    [Icon("pack://application:,,,/MyPlugin;component/Resources/Icon.png")]
    [Designer("MyPlugin.Designer.MyPluginCellTypeDesigner, MyPlugin")]
    [MyPluginStyleTemplateSupport]
    public class MyPluginCellType : CellType, IStyleTemplateSupport
    {
        public string TemplateKey { get; set; }
    }

    public class MyPluginStyleTemplateSupportAttribute : CellTypeStyleTemplateSupportAttribute
    {
        public override List<TemplatePart> TemplateParts => new List<TemplatePart>() { new TemplatePart()
        {
            Name= "主体",
            SupportStates = CellStates.Normal | CellStates.Hover | CellStates.Active,
            SupportStyles = SupportStyles.BackgroundColor | SupportStyles.ForegroundColor | SupportStyles.RoundedCorner | SupportStyles.Border | SupportStyles.Opacity
        }};

        public override List<CellTypeStyleTemplate> PresetTemplates => new List<CellTypeStyleTemplate>()
        {
            new CellTypeStyleTemplate()
            {
                Key = "主要",
                Category = "预置样式",
                Styles = new Dictionary<string, TemplatePartStyle>()
                {
                    {
                        "主体", new TemplatePartStyle()
                        {
                            NormalStyle = new PartStyleUnit()
                            {
                                Background = "Accent 1",
                                FontColor = "Background 1",
                                BorderRadiusString = "4px 4px 4px 4px"
                            },
                            HoverStyle = new PartStyleUnit()
                            {
                                Background = "Accent 1 20"
                            },
                            ActiveStyle = new PartStyleUnit()
                            {
                                Background = "Accent 1 -20"
                            },
                        }
                    }
                }
            },
            new CellTypeStyleTemplate()
            {
                Key = "成功",
                Category = "预置样式",
                Styles = new Dictionary<string, TemplatePartStyle>()
                {
                    {
                        "主体", new TemplatePartStyle()
                        {
                            NormalStyle = new PartStyleUnit()
                            {
                                Background = "Accent 2",
                                FontColor = "Background 1",
                                BorderRadiusString = "4px 4px 4px 4px"
                            },
                            HoverStyle = new PartStyleUnit()
                            {
                                Background = "Accent 2 20"
                            },
                            ActiveStyle = new PartStyleUnit()
                            {
                                Background = "Accent 2 -20"
                            },
                        }
                    }
                }
            },            
            new CellTypeStyleTemplate()
            {
                Key = "错误",
                Category = "预置样式",
                Styles = new Dictionary<string, TemplatePartStyle>()
                {
                    {
                        "主体", new TemplatePartStyle()
                        {
                            NormalStyle = new PartStyleUnit()
                            {
                                Background = "Accent 5",
                                FontColor = "Background 1",
                                BorderRadiusString = "4px 4px 4px 4px"
                            },
                            HoverStyle = new PartStyleUnit()
                            {
                                Background = "Accent 5 20"
                            },
                            ActiveStyle = new PartStyleUnit()
                            {
                                Background = "Accent 5 -20"
                            },
                        }
                    }
                }
            },
            new CellTypeStyleTemplate()
            {
                Key = "取消",
                Category = "预置样式",
                Styles = new Dictionary<string, TemplatePartStyle>()
                {
                    {
                        "主体", new TemplatePartStyle()
                        {
                            NormalStyle = new PartStyleUnit()
                            {
                                BorderRadiusString = "4px 4px 4px 4px",
                                BorderString = "1px solid Background_1_60",
                            },
                            HoverStyle = new PartStyleUnit()
                            {
                                Background = "Background 1 -25"
                            },
                            ActiveStyle = new PartStyleUnit()
                            {
                                Background = "Background 1 -15"
                            },
                        }
                    }
                }
            }
        };

        public override string DefaultTemplateKey => "主要";
    }
}
```

  

代码说明：

1.  MyPluginStyleTemplateSupportAttribute 文件中，通过TemplateParts可以定义一个或者多个部分的样式设置，本里中假设有一个部分，取名为“主体”。
2.  通过TemplateParts 可以定义单元格支持的状态已经支持的具体样式属性。
3.  PresetTemplates 可以声明一组预置样式。

为了方便实现设计时预览，活字格提供了使用预置样式生成WPF容器控件的工具方法，添加快速样式的设计时预览如下：

```
using MyPlugin.Designer.DrawingControl;
using GrapeCity.Forguncy.CellTypes;
using System.Windows;

namespace MyPlugin.Designer
{
    public class MyPluginCellTypeDesigner : CellTypeDesigner<MyPluginCellType>
    {
        public override FrameworkElement GetDrawingControl(ICellInfo cellInfo, IDrawingHelper drawingHelper)
        {
            var control = new MyPluginCellTypeDrawingControl(this.CellType, cellInfo, drawingHelper);
            if (cellInfo.StyleTemplateInfo != null && cellInfo.StyleTemplateInfo.TryGetValue("主体", out var style))
            {
                var previewControl = drawingHelper.CreateStylePreviewControl(style.NormalStyle);
                previewControl.Child = control;
                return previewControl as FrameworkElement;
            }
            return control; ;
        }
    }
}
```

  

设计器中的效果：

运行时：

活字格会自动为使用到的单元格生成 CSS Class。

命名规则如下：

【名字空间】+【单元格类型名称】+【-】+【styleTemplate.Key】+【-】+【样式部分名称】

JavaScript 代码如下：

```
MyPluginCellTypeStyleClassCache = {};
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const button = $("<button style='width:100%;height:100%;'>");
        if (this.CellElement.StyleTemplate) {
            const styleTemplate = this.CellElement.StyleTemplate;
            const styleName = "MyPluginMyPluginCellType" + "-" + styleTemplate.Key + "-" + "主体";
            button.addClass(styleName);
        }
        this.content = button;
        return button;
    }

    setValueToElement(_, value) {
        this.content.text(value?.toString());
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

---

## Supportcelltypestyle

# 支持单元格样式

## Content

活字格的单元格可以通过 Ribbon 设置样式，包括背景颜色、字体、字体颜色、字号、对齐方式、缩进等。
本章节将介绍如何让这些样式设置对插件单元格起作用。
支持样式不需要修改C#代码，只需要在 JavaScript 类中添加相应的处理，在设计器中的样式设置可以通过this.CellElement.StyleInfo属性获取，通过转化为指定Dom元素的Css样式发生效果。

```
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
  createContent() {
    const div = $("<div style='width:100%;height:100%;display:flex'>");
    const style = this.CellElement.StyleInfo;

    // 文字样式
    const cssStyle = {
      "color": Forguncy.ConvertToCssColor(style.Foreground),
      "font-size": style.FontSize > 0 ? style.FontSize : undefined,
      "font-family": style.FontFamily ? '"' + style.FontFamily + '"' : undefined,
      "font-style": style.FontStyle?.toLowerCase(),
      "font-weight": style.FontWeight?.toLowerCase(),
      "word-wrap": style.WordWrap ? "break-word" : undefined,
      "word-break": style.WordWrap ? "break-word" : undefined,
      "white-space": style.WordWrap ? "pre-wrap" : "pre",
    };

    // 下划线与删除线
    if (style.Underline || style.Strikethrough) {
      const textDecoration = [];
      if (style.Underline) {
        textDecoration.push("underline");
      }
      if (style.Strikethrough) {
        textDecoration.push("line-through");
      }
      cssStyle["text-decoration"] = textDecoration.join(" ");
    }

    // 对齐方式
    if (style.VerticalAlignment === Forguncy.Plugin.CellVerticalAlignment.Center) {
      cssStyle["align-items"] = "center";
    }
    else if (style.VerticalAlignment === Forguncy.Plugin.CellVerticalAlignment.Bottom) {
      cssStyle["align-items"] = "end";
    }
    if (style.HorizontalAlignment === Forguncy.Plugin.CellHorizontalAlignment.Center) {
      cssStyle["justify-content"] = "center";
    }
    else if (style.HorizontalAlignment === Forguncy.Plugin.CellHorizontalAlignment.Right) {
      cssStyle["justify-content"] = "end";
    }
    div.css(cssStyle);
    this.content = div;
    return div;
  }
  setValueToElement(_, value) {
    this.content.text(value?.toString());
  }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

上例子中，所有样式都是在 createContent 中设置的，这样做会有一个问题，活字格单元格的样式是可以通过设置单元格属性命令或者条件格式在运行时修改的。如果需要支持运行时修改样式，需要重写setFontStyle方法。
修改后代码如下：

```
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const div = $("<div style='width:100%;height:100%;display:flex'>");
        const style = this.CellElement.StyleInfo;

        const cssStyle = this.createFontStyleCss(style);

        // 下划线与删除线
        if (style.Underline || style.Strikethrough) {
            const textDecoration = [];
            if (style.Underline) {
                textDecoration.push("underline");
            }
            if (style.Strikethrough) {
                textDecoration.push("line-through");
            }
            cssStyle["text-decoration"] = textDecoration.join(" ");
        }

        // 对齐方式
        if (style.VerticalAlignment === Forguncy.Plugin.CellVerticalAlignment.Center) {
            cssStyle["align-items"] = "center";
        }
        else if (style.VerticalAlignment === Forguncy.Plugin.CellVerticalAlignment.Bottom) {
            cssStyle["align-items"] = "end";
        }
        if (style.HorizontalAlignment === Forguncy.Plugin.CellHorizontalAlignment.Center) {
            cssStyle["justify-content"] = "center";
        }
        else if (style.HorizontalAlignment === Forguncy.Plugin.CellHorizontalAlignment.Right) {
            cssStyle["justify-content"] = "end";
        }
        div.css(cssStyle);
        this.content = div;
        return div;
    }
    setValueToElement(_, value) {
        this.content.text(value?.toString());
    }

    createFontStyleCss(style) {
        // 文字样式
        return {
            "color": Forguncy.ConvertToCssColor(style.Foreground),
            "font-size": style.FontSize > 0 ? style.FontSize : undefined,
            "font-family": style.FontFamily ? '"' + style.FontFamily + '"' : undefined,
            "font-style": style.FontStyle?.toLowerCase(),
            "font-weight": style.FontWeight?.toLowerCase(),
            "word-wrap": style.WordWrap ? "break-word" : undefined,
            "word-break": style.WordWrap ? "break-word" : undefined,
            "white-space": style.WordWrap ? "pre-wrap" : "pre",
        };
    }

    setFontStyle(style) {
        const cssStyle = this.createFontStyleCss(style);
        this.content.css(cssStyle);
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```