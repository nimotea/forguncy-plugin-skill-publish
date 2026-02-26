# Properties Complex

## Datasourceproperty

# 数据源属性

## Content

如果属性绑定数据表的值，希望通过数据对话框编辑，可以通过标注BindingDataSourcePropertyAttribute 的方式设置。
注意，标注BindingDataSourcePropertyAttribute的属性类型必须是 object。

```auto
    public class MyPluginCellType : CellType
    {
        [BindingDataSourceProperty]
        [DisplayName("绑定数据源")]
        public object DataSource { get; set; }
    }
```

在设计器中效果如下：

对应的JavaScript处理代码：通过单元格上的getBindingDataSourceValue方法获取绑定数据。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const content = $("<div style='width:100%;height:100%;'></div>");

        const datasource = this.CellElement.CellType.DataSource;

        this.getBindingDataSourceValue(datasource, null, data => {
            for (const row of data) {
                const rowDom = $("<div/>");
                for (const colName in row) {
                    rowDom.append($("<span>" + row[colName] + ", </span>"));
                }
                content.append(rowDom);
            }
        });

        return content;
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

由于数据源查询条件可能会依赖单元格上的数据，如果单元格上的数据发生变化，需要重新获取数据源。为了处理这种情况，需要监听 onDependenceCellValueChanged 回调函数。所以改进后的JavaScript代码如下：

```auto
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const content = $("<div style='width:100%;height:100%;'></div>");

        const datasource = this.CellElement.CellType.DataSource;
        const loadBindingData = () => {
            this.getBindingDataSourceValue(datasource, null, data => {
                content.empty();
                for (const row of data) {
                    const rowDom = $("<div/>");
                    for (const colName in row) {
                        rowDom.append($("<span>" + row[colName] + ", </span>"));
                    }
                    content.append(rowDom);
                }
            });
        }

        this.onDependenceCellValueChanged(() => {
            loadBindingData();
        })
        loadBindingData();

        return content;
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

由于数据库数据可能被服务端命令或更新表命令修改，此时如果单元格希望在不重新加载页面的情况下获取最新更新的数据。需要重新 reload() 方法活字格会在服务端命令或更新表命令执行或，检测声明了 BindingDataSourceProperty 的单元格，依次调用 reload() 方法。单元格可以在 reload方法中重新从服务端获取数据。

```auto
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    loadBindingData = () => {
        const datasource = this.CellElement.CellType.DataSource;
        this.getBindingDataSourceValue(datasource, null, data => {
            this.content.empty();
            for (const row of data) {
                const rowDom = $("<div/>");
                for (const colName in row) {
                    rowDom.append($("<span>" + row[colName] + ", </span>"));
                }
                this.content.append(rowDom);
            }
        });
    }
    content = null;
    createContent() {
        this.content = $("<div style='width:100%;height:100%;'></div>");

        this.onDependenceCellValueChanged(() => {
            this.loadBindingData();
        })
        this.loadBindingData();

        return this.content;
    }
    reload() {
        this.loadBindingData();
    }
}

Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

使用onDependenceCellValueChanged有一个弊端：如果单元格上有多个公式属性，任何一个公式属性发生变化，都会触发onDependenceCellValueChanged方法的执行，并且在onDependenceCellValueChanged方法中无法区分具体是哪个属性发生了变化。在 V10.0.0.0 中新增了一个方法 getBindingDataSourceValue，方法新加了一个参数，表示数据源变化时是否重新执行数据加载回调。代码如下：

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    content = null;
    createContent() {
        this.content = $("<div style='width:100%;height:100%;'></div>");
        return this.content;
    }
    onPageLoaded() {
        this.getBindingDataSourceValue(this.CellElement.CellType.DataSource, null, data => {
            this.content.empty();
            for (const row of data) {
                const rowDom = $("<div/>");
                for (const colName in row) {
                    rowDom.append($("<span>" + row[colName] + ", </span>"));
                }
                this.content.append(rowDom);
            }
        }, true); // 最后一个参数 true，表示数据源依赖的公式变化时，重新调用回调函数。
    }
}

Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

在大部分情况下，getBindingDataSourceValue 加上reloadWhenDependenceChanged参数都可以解决单元格获取数据源的问题。但是有些特殊情况下，希望第一次加载数据源和以后加载数据源的逻辑不一样时，可以使用onBindingDataSourceDependenceCellValueChanged 方法监听数据源变更。代码如下：

```auto
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.content = $("<div style='width:100%;height:100%'></div>");
        return this.content;
    }
    onPageLoaded() {
        this.loadData(); //第一次
        this.onBindingDataSourceDependenceCellValueChanged(this.CellElement.CellType.DataSource, () => {
            this.loadData(); // 变更回调
        })
    }

    loadData() {
        this.getBindingDataSourceValue(this.CellElement.CellType.DataSource, null, data => {
            this.content.text(JSON.stringify(data));
        });
    }

}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

>type=note
> **说明：**
> 在V10banbanb版本以后，不再推荐使用 onDependenceCellValueChanged方法，而应该使用 getBindingDataSourceValue 方法或onBindingDataSourceDependenceCellValueChanged方法 ，以确保代码更简洁，性能更好，并且支持和组件属性绑定。

如果需要更细致的控制，可以通过BindingDataSourcePropertyAttribute的其他属性来控制。
**1\. 预置数据列：**

1. 设置BindingDataSourcePropertyAttribute 的 Columns 属性。
2. 代码：
    格式：列名\|列名2\.\.\.

    ```auto
        public class MyPluginCellType : CellType
        {
            [BindingDataSourceProperty(Columns = "ID|Name")]
            [DisplayName("绑定数据源")]
            public object DataSource { get; set; }
        }
    ```
3. 设计器效果：
    

**2.** **为预置数据列添加显示文本：**

1. 设置BindingDataSourcePropertyAttribute 的 Columns 属性。
2. 代码：
    格式：列名:显示名\|列名2:显示名\|\.\.\.

    ```auto
        public class MyPluginCellType : CellType
        {
            [BindingDataSourceProperty(Columns = "ID|Name:姓名|Age:年龄")]
            [DisplayName("绑定数据源")]
            public object DataSource { get; set; }
        }
    ```
3. 设计器效果：
    
4. 注意：设置显示文本不影响JavaScript端数据处理，只影响在设计器中的显示。
5. <span class="ne-text">如果在此模式下仍然需要添加自定义列，可以设置AllowAddCustomColumns属性。</span>

    ```auto
        public class MyPluginCellType : CellType
        {
            [BindingDataSourceProperty(AllowAddCustomColumns = true, Columns = "ID|Name:姓名|Age:年龄")]
            [DisplayName("绑定数据源")]
            public object DataSource { get; set; }
        }
    ```
6. <span class="ne-text">设置AllowAddCustomColumns之后效果如下（此特性需要活字格版本大于等于9.0.100.0）。</span>
    

**3.** **为预置数据源列添加描述信息。**

1. 设置BindingDataSourcePropertyAttribute 的 ColumnsDescription 属性。
2. 代码：

    ```auto
        public class MyPluginCellType : CellType
        {
            [BindingDataSourceProperty(Columns = "ID|Name|Age", ColumnsDescription = "ID:通常绑定主键列|Age:表示年龄列")]
            [DisplayName("绑定数据源")]
            public object DataSource { get; set; }
        }
    ```
3. 设计器效果：
    
4. 注意，需要和Columns属性配合使用，在Columns里没有的列，设置的描述会被忽略。

**4.** **开启树结构查询配置（ID/PID 结构）。**

1. 什么是ID/PID结构：
    在数据库中，是用二维表保存数据的，但是现实生活中，很多数据会有父子关系，例如公司的组织机构，会在数据库中保存为如下形式，这样就可以使用二维表表示树结构了。

    | ID | 名称 | PID |
    | --- | --- | --- |
    | 1 | xx公司 |  |
    | 2 | 财务部 | 1 |
    | 3 | 销售部 | 1 |
    | 4 | 销售一组 | 3 |
    | 5 | 销售二组 | 3 |
2. 设置BindingDataSourcePropertyAttribute 的 IsIdPidStructure 属性为True声明接受树结构表。
3. 代码。

    ```auto
        public class MyPluginCellType : CellType
        {
            [BindingDataSourceProperty(Columns = "ID|Name|PID", IsIdPidStructure = true, TreeIdColumnName = "ID", TreePidColumnName = "PID")]
            [DisplayName("绑定数据源")]
            public object DataSource { get; set; }
        }
    ```
4. 设计器效果：会在其他标签页中增加“树形结构查询配置的选项”。
    
5. 注意，开启树形结构查询配置IsIdPidStructure属性后，需要配合设置 TreeIdColumnName 和 TreePidColumnName 属性。

**5.** **支持查询子表列**

1. 活字格中的子表
    当在活字格中，设置关联关系时，可以勾选“是否有子表关联？”为True，此时，主表会增加一个虚拟列，如下图中的“订单详情表”。
    
2. 设置BindingDataSourcePropertyAttribute 的 SupportDetailTable 属性。
3. 代码：
    格式：列名:描述\|列名2:描述2\.\.\.

    ```csharp
        public class MyPluginCellType : CellType
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

## ImageProperty

# 图片属性

## Content

如果属性表示图片或图标，希望使用图片选择编辑器编辑属性，可以通过标注ImageValuePropertyAttribute 的方式设置。注意，标注ImageValuePropertyAttribute的属性类型必须是 object 或 ImageValue。

```auto
    public class MyPluginCellType : CellType
    {
        [ImageValueProperty]
        public object MyProperty { get; set; }
    }
```

在设计器中效果如下：

如果需要更细致的控制，需要使用 ImageValuePropertyAttribute标注来控制。
**1.** 禁止选择SVG图片

1. 设置ImageValuePropertyAttribute的 SupportSvg属性。
2. 代码：

    ```auto
         public class MyPluginCellType : CellType
        {
            [ImageValueProperty(SupportSvg = false)]
            public object MyProperty { get; set; }
        }
    ```
3. 效果：在图片选择对话框中只允许选择或上传普通图片，不能选择或上传SVG图片。
    

**2.** 设置内置图标默认值
例如内建单元格中如果没有设置图标，按钮的图标默认值是白色的，文本框的图标默认是灰色的。

1. 设置ImageValuePropertyAttribute 的 DefaultIconColor 属性。
2. 代码。关于活字格中的颜色字符串表示法，请参考 [颜色属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/colorproperty)。

    ```auto
        public class MyPluginCellType : CellType
        {
            [ImageValueProperty(DefaultIconColor = "Accent 2")]
            public object MyProperty { get; set; }
        }
    ```
3. 效果：
    

**3.** 设置默认选中的标签页。
如果该属性大部分情况下推荐用户使用内建图标应该把默认标签页设置为“内置图标”。

1. 设置ImageValuePropertyAttribute 的 DefaultActiveTabIndex 属性。
2. 代码：

    ```auto
        public class MyPluginCellType : CellType
        {
            [ImageValueProperty(DefaultActiveTabIndex = 1)]
            public object MyProperty { get; set; }
        }
    ```
3. 效果：
    
4. 说明：
    默认值为0表示默认标签页为本地图片，如果设置为 1 表示默认选中内置图标。其他值无效。

**4.** 禁止图标使用单元格字体颜色。

1. 设置ImageValuePropertyAttribute 的 SupportUseCellColor 属性。
2. 代码。

    ```auto
        public class MyPluginCellType : CellType
        {
            [ImageValueProperty(SupportUseCellColor = false)]
            public object MyProperty { get; set; }
        }
    ```

**5.** 图标默认设置为使用单元格字体颜色。

1. 设置ImageValuePropertyAttribute 的 DefaultUseCellColor 属性。
2. 代码：

    ```auto
     public class MyPluginCellType : CellType
        {
            [ImageValueProperty(DefaultUseCellColor = true)]
            public object MyProperty { get; set; }
        }
    ```
3. 效果：
    

**JavaScript 中的图片处理**
在活字格中，图片使用分为三种情况：

1. 普通图片
2. SVG图片
3. 内置SVG图标

```auto
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    content = null;
    createContent() {
        this.content = $("<div style='width:100%;height:100%'></div>");

        const image = this.CellElement.CellType.MyProperty;
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
                    this.content.append(svg);
                });
            }
            else {
                this.content.append($("<img style='width:100%;height:100%' src=" + src + ">"))
            }
        }
        return this.content;
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
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

## Objectproperty

# 对象属性

## Content

默认情况下，如果一个属性的类型是对象类型，这个类型又包含了一些子属性，那么可以通过标注ObjectPropertyAttribute，使得活字格设计器可以通过弹出二级对话框来编辑该属性。
注意，ObjType属性里声明的类型必须与属性类型一致。
自定义对象的类型应该从 ObjectPropertyBase 类派生，以确保在单元格复制的时候，子属性可以被正确的深克隆（ObjectPropertyBase实现了默认的深克隆逻辑）。

```auto
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Plugin;
using System.Collections.Generic;

namespace MyPlugin
{
    public class MyPluginCellType : CellType
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

```auto
    public class MyPluginCellType : CellType
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

**1.添加描述**

1. <span class="ne-text">设置 DescriptionAttribute。</span>
2. <span class="ne-text">代码如下：</span>

    ```auto
        public class MyPluginCellType : CellType
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

**2.给对象添加自定义校验**

1. <span class="ne-text">给属性添加DesignerAttribute 重写Validate方法添加自定义校验。</span>
2. <span class="ne-text">代码如下：</span>

    ```auto
        public class MyPluginCellType : CellType
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

**3.属性变更联动**

1. <span class="ne-text">所有继承自 ObjectPropertyBase 的对象都可以在类型声明时标注 [DesignerAttribute] 特性，可以达到对象内的属性变化联动。</span>
2. 此功能同时支持 ObjectProperty、FlatObjectProperty、ObjectListProperty、ListProperty 以及 FlatListProperty。
3. <span class="ne-text">下面的示例代码中， MyObject 对象拥有两个属性，当用户编辑Data1时，Data2将改变，值为“Data1 + 1”。</span>

    ```auto
        [Icon("pack://application:,,,/Test;component/Resources/Icon.png")]
    [Designer("Test.Designer.TestCellTypeDesigner, Test")]
    public class TestCellType : CellType
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
    
5. 此特性为10.0.100.0版本新增的特性。

---

## Radioproperty

# 单选框属性

## Content

如果属性的类型是字符串，默认属性值是可以接受任意字符串的，如果希望提供字符串值候选列表，可以通过标注RadioGroupProperty 的并设置ValueList属性的方式实现单选框候选列表。多值个值用“\|”分隔。
RadioGroupProperty和ComboProperty的使用方式非常类似，主要是在设计器中的UI表现不同。
注意，标注RadioGroupProperty的属性类型必须是 string。

```auto
    public class MyPluginCellType : CellType
    {
        [RadioGroupProperty(ValueList = "Student|Teacher|Worker")]
        public string MyProperty { get; set; }
    }
```

在设计器中效果如下：

如果需要更细致的控制，可以通过RadioGroupProperty的其他属性来控制。
值与显示值不同：

1. 设置RadioGroupProperty的 DisplayList 属性。
2. 代码：

    ```auto
        public class MyPluginCellType : CellType
        {
            [RadioGroupProperty(ValueList = "Student|Teacher|Worker", DisplayList ="学生|教师|工人")]
            public string MyProperty { get; set; }
        }
    ```
3. 效果：
    
4. 其他说明：
    此方法可以使用户在选择时选择中文选项，而单元格实际保存值为英文，方便程序处理。
    ValueList和DisplayList通过数量和顺序匹配。
    如果DisplayList数量超出ValueList数量，多出部分会被忽略。
    如果DisplayList数量少于ValueList数量，不足部分会使用ValueList对应的值。

---

## Treeproperty

# 树结构属性

## Content

如果一个属性的希望保存树形结构，那么可以通过标注TreePropertyAttribute，使得活字格设计器可以通过弹出二级对话框来编辑该属性。
注意：

1. NodeType属性里声明的类型必须与结点对象类型一致；
2. 属性类型必须是List 并且通过 new List() 方法初始化；
3. 结点类型必须实现 ITreeNode接口；
4. Children属性必须通过 new List(); 初始化；
5. 自定义结点的类型应该从 ObjectPropertyBase 类派生，以确保在单元格复制的时候，子属性可以被正确的深克隆（ObjectPropertyBase实现了默认的深克隆逻辑）。

```
    public class MyPluginCellType : CellType
    {
        [TreeProperty(NodeType = typeof(NodeObj))]
        public List<ITreeNode> TreeNodes { get; set; } = new List<ITreeNode>();
    }

    public class NodeObj : ObjectPropertyBase, ITreeNode
    {
        public string Text {get;set;}
        public IEnumerable<ITreeNode> Children { get; set; } = new List<NodeObj>();
        public string SubProperty1 { get; set; }
        public string SubProperty2 { get; set; }
    }
```

在设计器中效果如下：

结点项目的子属性也可以通过标注来控制属性编辑控件。
下面例子中，额外声明了两个属性分别使用公式编辑器和命令编辑器。具体标注的用法请参考之前的章节。

```
    public class MyPluginCellType : CellType
    {
        [TreeProperty(NodeType = typeof(NodeObj))]
        public List<ITreeNode> TreeNodes { get; set; } = new List<ITreeNode>();
    }

    public class NodeObj : ObjectPropertyBase, ITreeNode
    {
        public string Text {get;set;}
        public IEnumerable<ITreeNode> Children { get; set; } = new List<NodeObj>();
        [FormulaProperty]
        public string SubProperty1 { get; set; }
        [CustomCommandObject]
        [DisplayName("点击命令")]
        public string SubProperty2 { get; set; }
    }
```

在设计器中效果如下：

如果需要更细致的控制，可以通过TreePropertyAttribute的其他属性来控制。
控制新增结点的默认名称：

1. 设置TreePropertyAttribute 的 DefaultNodeName  属性。
2. 代码：

    ```
        public class MyPluginCellType : CellType
        {
            [TreeProperty(NodeType = typeof(NodeObj), DefaultNodeName = "结点")]
            public List<ITreeNode> TreeNodes { get; set; } = new List<ITreeNode>();
        }
    
        public class NodeObj : ObjectPropertyBase, ITreeNode
        {
            public string Text {get;set;}
            public IEnumerable<ITreeNode> Children { get; set; } = new List<NodeObj>();
            public string SubProperty1 { get; set; }
            public string SubProperty2 { get; set; }
        }
    ```

---

## Databaseconnectionselectorproperty

# 数据库连接选择属性

## Content

<span class="ne-text">此特性为活字格V9.1新增功能。</span>

```
    public class MyPluginCellType : CellType
    {
        [DatabaseConnectionSelectorProperty]
        public string Connection { get; set; }
    }
```

<span class="ne-text">在设计器中效果如下：</span>
<span class="ne-text">在数据库连接管理中连接了一些外链数据库之后：</span>

<span class="ne-text">可以通过标注了DatabaseConnectionSelectorProperty的属性选择特定数据库。</span>

<span class="ne-text">使用数据库连接名可以在服务端代码中使用。</span>

```
        public async void ExampleForDataConnectionAsync(string connectionName, IDataAccess dataAccess)
        {
            var connectionStr = dataAccess.GetConnectionStringByID(connectionName);

            dataAccess.BeginTransaction(connectionStr);
            try
            {
                var result = await dataAccess.ExecuteSqlAsync(connectionName, "select * from 表1", null);
                dataAccess.CommitTransaction(connectionStr);
            }
            finally
            {
                dataAccess.RollbackTransaction(connectionStr);
            }
        }
```

<span class="ne-text">如果需要更细致的控制，可以通过DatabaseConnectionSelectorProperty的其他属性来控制。</span>
**<span class="ne-text">显示为内建库</span>**
<span class="ne-text">1\. 设置DatabaseConnectionSelectorProperty的IncludeBuiltInDatabase属性。</span>
2\. 代码：

```
     public class MyPluginCellType : CellType
     {
     [DatabaseConnectionSelectorProperty(IncludeBuiltInDatabase = true)]
     public string Connection { get; set; }
     }
```

3\. 效果：

4\. 说明：<span class="ne-text">对于内建数据库（Sqlite）连接名称为null。</span>
<span class="ne-text">注意：标注DatabaseConnectionSelectorProperty的属性类型必须是 string。</span>

---

## Pagenameproperty

# 页面选择属性

## Content

<span class="ne-text">此特性为活字格V9.1新增功能。</span>

```
    public class MyPluginCellType : CellType
    {
        [PageNameProperty]
        public string PageName { get; set; }
    }
```

<span class="ne-text">在设计器中效果如下：</span>

<span class="ne-text">默认情况下，内建页面是不能被选择的，如果需要选择内建页面，需要设置IncludeBuiltInPage，代码如下：</span>

```
    public class MyPluginCellType : CellType
    {
        [PageNameProperty(IncludeBuiltInPage = true)]
        public string PageName { get; set; }
    }
```

<span class="ne-text">注意：标注PageNameProperty的属性类型必须是 string。</span>

---

## Roleselectorproperty

# 角色选择属性

## Content

此特性为活字格V9.1新增功能。

```auto
    public class MyPluginCellType : CellType
    {
        [RoleSelectorProperty]
        public List<string> Roles { get; set; }
    }
```

在设计器中效果如下：

注意：标注RoleSelectorProperty的属性类型必须是 List\<string>。

---

## Servercommandnameproperty

# 服务端命令选择属性

## Content

此特性为活字格V9.1新增功能。

```auto
    public class MyPluginCellType : CellType
    {
        [ServerCommandNameProperty]
        public string MyProperty { get; set; }
    }
```

在设计器中效果如下：

注意：标注ServerCommandNameProperty的属性类型必须是 string。

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