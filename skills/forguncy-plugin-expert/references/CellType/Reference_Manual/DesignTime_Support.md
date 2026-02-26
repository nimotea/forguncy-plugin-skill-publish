# DesignTime Support

## Celldesignsupport

# 单元格设计时支持

## Content

*   [支持设计时预览](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/supportsdesigntimepreview)
*   [动态隐藏属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/dynamichiddenproperties)
*   [创建单元格时初始化属性值](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/initializepropertyvalueswhencreatingcells)
*   [单元格分组与排序](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/cellgroupingandsorting)
*   [重新定义单元格双击行为](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/redefinecelldoubleclickbehavior)
*   [属性分组](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/categoryheaderattribute)
*   [给属性添加说明](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/adddescriptiontoattribute)
*   [修改属性显示名](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/modifydisplaynameattribute)

---

## AdvancedCellOperationsDesignTimeSupport

# 高级单元格操作设计时支持

## Content

可以通过给单元格操作对应的方法添加 RunTimeMethodDesignerAttribute 来做一些设计时的细节控制

#### 自定义参数校验

可以通过重写Validate方法自定义参数校验。
代码如下：

```auto
    public class MyPluginCellType : CellType
    {
        [RunTimeMethod]
        [RunTimeMethodDesigner(typeof(MyRuntimeMethodDesigner))]
        public void MyOperation(bool param1 = false, bool param2 = false)
        {
        }
    }

    public class MyRuntimeMethodDesigner : RunTimeMethodDesigner
    {
        public override string Validate(IRuntimeMethodDesignerContext context)
        {
            if (!object.Equals(context.GetParameterValue("param1"), true) &&
                object.Equals(context.GetParameterValue("param2"), true))
            {
                return "param1 和 param2 必须至少勾选一个";
            }
            return base.Validate(context);
        }
    }
```

设计器效果如下：

#### 属性动态隐藏显示

可以通过重写GetDesignerParameterVisible方法自定义参数校验。
代码如下：

```auto
    public class MyPluginCellType : CellType
    {
        [RunTimeMethod]
        [RunTimeMethodDesigner(typeof(MyRuntimeMethodDesigner))]
        public void MyOperation(bool param1 = false, bool param2 = false)
        {
        }
    }

    public class MyRuntimeMethodDesigner : RunTimeMethodDesigner
    {
        public override bool GetDesignerParameterVisible(IRuntimeMethodDesignerContext context, string parameterName)
        {
            if (parameterName == "param2")
            {
                return object.Equals(context.GetParameterValue("param1"), true);
            }
            return base.GetDesignerParameterVisible(context, parameterName);
        }
    }
```

设计器效果：

如果处理逻辑中需要依赖单元格，可以通过 context.Target 获取。

```auto
var cellType = context.Target as MyPluginCellType;
```

---

## Cellgroupingandsorting

# 单元格分组与排序

## Content

默认情况下，单元格的分组是其他。

可以通过标注CategoryAttribute来自定义分组。

```
    [Category("我的分组")]
    public class MyPluginCellType : CellType
    {
    }
```

效果如下：  
  

如果分组名与既有的分组名一致，会加到已有的组里。

```
    [Category("导航")]
    public class MyPluginCellType : CellType
    {
    }
```

  

效果如下：

如果有多个插件，在同一分组，可以通过OrderWeightAttribute标注排序权重。

```
    [OrderWeight(1)]
    [Category("我的分组")]
    public class MyPluginCellType1 : CellType
    {
    }
    [OrderWeight(2)]
    [Category("我的分组")]
    public class MyPluginCellType2 : CellType
    {
    }
    [OrderWeight(3)]
    [Category("我的分组")]
    public class MyPluginCellType3 : CellType
    {
    }
```

  

设计器效果：

---

## Supportsdesigntimepreview

# 支持设计时预览

## Content

支持设计时预览通常对单元格本身的功能没有什么影响，但是好的设计时预览支持可以大幅提升单元格插件的设计时使用体验和效率。
在活字格中，设计时预览必须使用WPF技术实现，需要了解WPF窗体开发的一些知识，如XMAL，Binding等。
完善的设计时预览应该使得单元格在设计器中的样子和浏览器中尽可能的相似，并且在属性变更时，设计时预览也应该发生相应的变化。
根据经验，完善的设计时预览支持有时会占用开发单元格插件超过一半的时间，也是单元格插件开发过程中最困难的部分。如果是企业内部为了自用目的开发的单元格插件可以通过贴图，色块等方式适度简化单元格的设计时预览，以减少插件开发的时间，把更多的经历可以放到浏览器端的业务逻辑与用户交互上。

在插件项目模板中找到 Designer\\MyPluginCellTypeDesigner.cs 文件。默认代码如下。

```
  public class MyPluginCellTypeDesigner : CellTypeDesigner<MyPluginCellType>
    {
        public override FrameworkElement GetDrawingControl(ICellInfo cellInfo, IDrawingHelper drawingHelper)
        {
            return new MyPluginCellTypeDrawingControl(this.CellType, cellInfo, drawingHelper);
        }
    }
```

通过重写 GetDrawingControl 方法，可以控制返回一个 WPF 的组件。模板工程中已经定义了一个 MyPluginCellTypeDrawingControl 的组件。代码在 Designer\\DrawingControl\\MyPluginCellTypeDrawingControl.xaml 中。一个WPF 组件包含两个文件

1. MyPluginCellTypeDrawingControl.xaml 用于定义显示
2. MyPluginCellTypeDrawingControl.xaml.cs 用于定义属性和逻辑

假设要开发一个显示进度的进度条单元格，那么首先如下修改 MyPluginCellTypeDrawingControl.xaml 文件。

```
<UserControl x:Class="MyPlugin.Designer.DrawingControl.MyPluginCellTypeDrawingControl"
             xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" 
             xmlns:d="http://schemas.microsoft.com/expression/blend/2008" 
             mc:Ignorable="d" 
             d:DesignHeight="40" d:DesignWidth="200">
    <Grid>
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="60*"></ColumnDefinition>
            <ColumnDefinition Width="40*"></ColumnDefinition>
            <ColumnDefinition Width="auto"></ColumnDefinition>
        </Grid.ColumnDefinitions>
        <Border Grid.ColumnSpan="2" CornerRadius="5" Height="10" Background="LightGray"></Border>
        <Border CornerRadius="5" Background="Green" Height="10"></Border>
        <TextBlock VerticalAlignment="Center" Grid.Column="2" Text="60%"></TextBlock>
    </Grid>
</UserControl>
```

代码解释：

1. 定义了一个网格布局控件（Grid），并定义了三列，第一列占60%宽度，第二列占40%宽度。最后一列自动适应内容
2. 定义两个边框控件
3. 第一个边框控件是灰色的表示背景，宽度跨了两列，高度10
4. 第二个边框控件是绿色的表示值，占第一列，高度也是10

这样，一个进度条的设计时预览就完成了，在设计器中的效果如下：

现在的设计时预览有一个问题，就是所有表现都是固定的，接下来我们改进一下，使得设计时预览可以根据单元格的属性和值发生变化。
假设改进点如下：

1. 添加进度颜色属性
2. 添加是隐藏文本属性
3. 进度条绿色块的长度随单元格的值变化，0的时候最短，100的时候填充满，文字显示进度值。

首先在 MyPluginCellType.cs 中添加相应的属性，代码如下

```
    public class MyPluginCellType : CellType
    {
        [DisplayName("进度条颜色")]
        [ColorProperty]
        public string Color { get; set; } = "Green";

        [DisplayName("隐藏文本")]
        public bool HideText { get; set; }
    }
```

找到 Designer\\DrawingControl\\MyPluginCellTypeDrawingControl.xaml.cs
使用以下代码替换原有代码

```
using GrapeCity.Forguncy.CellTypes;
using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace MyPlugin.Designer.DrawingControl
{
    public partial class MyPluginCellTypeDrawingControl : UserControl
    {
        public MyPluginCellTypeDrawingControl(MyPluginCellType cellType, ICellInfo cellInfo, IDrawingHelper drawingHelper)
        {
            this.DataContext = new MyPluginCellTypeDrawingControlViewModel(cellType, cellInfo, drawingHelper);

            InitializeComponent();
        }
        public class MyPluginCellTypeDrawingControlViewModel
        {
            MyPluginCellType _cellType;
            ICellInfo _cellInfo;
            IDrawingHelper _drawingHelper;
            double _progress = 0;
            public MyPluginCellTypeDrawingControlViewModel(MyPluginCellType cellType, ICellInfo cellInfo, IDrawingHelper drawingHelper)
            {
                _cellType = cellType;
                _cellInfo = cellInfo;
                _drawingHelper = drawingHelper;

                if (_cellInfo.Value != null && double.TryParse(_cellInfo.Value.ToString(), out var value))
                {
                    _progress = Math.Max(0, Math.Min(value, 100d)); // 把值调整到0到100之间
                }
            }
            public string Text { get => _progress + "%"; }
            public Brush Color { get => _drawingHelper.GetBrush(_cellType.Color); }
            public Visibility TextVisiblity { get => _cellType.HideText ? Visibility.Collapsed : Visibility.Visible; }
            public GridLength FirstColumn { get => new GridLength(_progress, GridUnitType.Star); }
            public GridLength SecondColumn { get => new GridLength(100 - _progress, GridUnitType.Star); }
        }
    }
}
```

MyPluginCellTypeDrawingControlViewModel 代码说明：

1. 声明了 \_progress 字段
2. 通过 \_cellInfo.Value 获取单元格的值，转为数字并把范围调整到 0 到 100 之间
3. 声明了 Text 属性，返回百分百格式文本
4. 声明了 Color属性， 通过 \_drawingHelper.GetBrush 方法把文本颜色转成WPF可用的Brush类型
5. 声明了 TextVisiblity, HideText 为True返回Visible，否则返回 Collapsed
6. 声明了 FirstColumn SecondColumn，用于调整网格布局的列宽

再次修改 MyPluginCellTypeDrawingControl.xaml 文件：

```
<UserControl x:Class="MyPlugin.Designer.DrawingControl.MyPluginCellTypeDrawingControl"
             xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" 
             xmlns:d="http://schemas.microsoft.com/expression/blend/2008" 
             mc:Ignorable="d" 
             d:DesignHeight="40" d:DesignWidth="200">
    <Grid>
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="{Binding FirstColumn}"></ColumnDefinition>
            <ColumnDefinition Width="{Binding SecondColumn}"></ColumnDefinition>
            <ColumnDefinition Width="auto"></ColumnDefinition>
        </Grid.ColumnDefinitions>
        <Border Grid.ColumnSpan="2" CornerRadius="5" Height="10" Background="LightGray"></Border>
        <Border CornerRadius="5" Background="{Binding Color}" Height="10"></Border>
        <TextBlock Visibility="{Binding TextVisiblity}" VerticalAlignment="Center" Grid.Column="2" Text="{Binding Text}"></TextBlock>
    </Grid>
</UserControl>
```

注意，原来写死的列宽，颜色文本等，都使用了 {Binding 属性名} 的方式做了替换。这样，在WPF渲染的时候这些属性就会从 MyPluginCellTypeDrawingControl.xaml.cs 文件里的 MyPluginCellTypeDrawingControlViewModel 类上取值，实现动态效果。

再次查看设计器中的效果，可以尝试修改颜色和单元格的值，看看有什么变化。

总结：
要实现设计时预览，修改以下两个文件：

1. MyPluginCellTypeDrawingControl.xaml.cs
    用于添加可变属性，属性的值可以通过单元格插件的属性或单元格本身的属性计算得来。
2. MyPluginCellTypeDrawingControl.xaml
    用于通过 XAML 语法声明界面，通过 {Binding 属性} 语法实现动态效果。

---

## DesignTimePreviewInChromium

# 使用无头浏览器实现设计时预览

## Content

此特性为V10.0.0.0新增的特性。

#### 原理

在V10之前的版本，如果单元格要在设计器中实现设计时预览，必须使用WPF技术。这样一个单元格的画法就需要用两种不同的技术实现两遍（JavaScript，WPF）。这给单元格的插件开发带来了很大的技术负担。很多情况下，单元格插件的开发者会使用一个静态图片占位的方式来实现设计时预览。这又给插件的使用者带来了困难。插件的使用者不得不在调整设置之后，反复运行去查看结果，降低了开发效率。
在V10版本，活字格提供了新的设计时预览机制。活字格设计器会启动一个无头浏览器（Chromium），使用运行时的JavaScript代码渲染插件单元格，再把渲染的结果以图片的方式传回活字格设计器。这样，活字格设计器中就可以渲染和运行时几乎一样的单元格UI了。

#### 准备代码

以下代码，实现了一个简单的列表单元格。支持设置列表的标题和内容。
设计时代码：

```csharp
    public class MyPluginCellType : CellType
    {
        [FormulaProperty]
        [DisplayName("标题")]
        public object Title { get; set; }

        [FlatListProperty]
        [DisplayName("内容")]
        public List<MyObj> Items { get; set; }
    }

    public class MyObj : ObjectPropertyBase
    {
        [FormulaProperty]
        [DisplayName("项目")]
        [ListPropertyItemSetting(DefaultName = "项目", DefaultWidth = 200)]
        public object Name { get; set; }
    }
```

运行时代码：

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.content = $("<div style='width:100%;height:100%;'></div>");
        this.title = $("<h3/>");
        this.items = $("<ul/>");
        this.content.append(this.title);
        this.content.append(this.items);
        return this.content;
    }
    onPageLoaded() {
        this.onFormulaResultChanged(this.CellElement.CellType.Title, result => {
            this.title.text(result)
        });
        for (const item of this.CellElement.CellType.Items) {
            const itemDom = $("<li>");
            this.items.append(itemDom);
            this.onFormulaResultChanged(item.Name, result => {
                itemDom.text(result)
            });
        }
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

设计器中的设置：

运行时效果：

到此，通过之前章节的内容，可以轻松实现一个插件单元格，但是有一个问题：可以看到，在设计器中，单元格区域是一片空白，不符合活字格所见即所得的设计原则。

#### 基本实现

通过添加以下代码，可以声明单元格以无头浏览器的方式实现设计时预览。

```csharp
    [Designer(typeof(MyPluginCellTypeDesigner))]
    public class MyPluginCellType : CellType
    {
        //代码不变，使用上例中相同代码，注意类型上标注的Designer......
    }

    public class MyPluginCellTypeDesigner : CellTypeDesigner<MyPluginCellType>
    {
        public override FrameworkElement GetDrawingControl(ICellInfo cellInfo, IDrawingHelper drawingHelper)
        {
            return drawingHelper.GetHeadlessBrowserPreviewControl(); // 使用无头浏览器渲染设计时预览
        }
    }
```

设计器中的效果：

可以看到，简单的几行代码，就可以得到几乎和运行时一模一样的预览效果了。

#### 更精细的控制

##### 区分设计时预览与运行时逻辑

在以上例子中，可以看到，设计时预览和运行时效果几乎是一摸一样的。但是有些情况下，可能需要设计时预览和运行时结果有一些差别。例如上例中，如果把单元格拖拽到设计器中，由于初始的标题和内容都是空，导致单元格里仍然是一片空白。这种情况下，希望能显示一段提示信息，如“请设置标题和内容”。但是这个信息又不希望影响运行时，此时可以通过**isDesignerPreview** 属性，在前端代码中判断现在的渲染是预览状态还是运行时状态。
示例代码如下：

```javascript
/// <reference path="../Declarations/forguncy.d.ts" />
/// <reference path="../Declarations/forguncy.Plugin.d.ts" />

class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.content = $("<div style='width:100%;height:100%;'></div>");
        if (this.isDesignerPreview &&
            !this.CellElement.CellType.Title &&
            !this.CellElement.CellType.Items?.length) {
            this.content.append($("<div style='color:gray'>请设置标题和内容</div>"));
        }
        this.title = $("<h3/>");
        this.items = $("<ul/>");
        this.content.append(this.title);
        this.content.append(this.items);

        return this.content;
    }
    onPageLoaded() {
        this.onFormulaResultChanged(this.CellElement.CellType.Title, result => {
            this.title.text(result)
        });
        for (const item of this.CellElement.CellType.Items) {
            const itemDom = $("<li>");
            this.items.append(itemDom);
            this.onFormulaResultChanged(item.Name, result => {
                itemDom.text(result)
            });
        }
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

设计器效果：

##### 预览绑定数据源数据

上例中，内容的设置是设计时手工输入的，如果内容需要从数据库中获取。需要设计器给无头浏览器提供数据
单元格改造如下：

```csharp
    [Designer(typeof(MyPluginCellTypeDesigner))]
    public class MyPluginCellType : CellType
    {
        [FormulaProperty]
        [DisplayName("标题")]
        public object Title { get; set; }

        [BindingDataSourceProperty(Columns = "Name:项目")]
        [DisplayName("内容")]
        public IBindingDataSource Items { get; set; }
    }

    public class MyPluginCellTypeDesigner : CellTypeDesigner<MyPluginCellType>
    {
        public override FrameworkElement GetDrawingControl(ICellInfo cellInfo, IDrawingHelper drawingHelper)
        {
            return drawingHelper.GetHeadlessBrowserPreviewControl(new GetHeadlessBrowserPreviewControlOptions()
            {
                GenerateCustomArgsAsync = async () =>
                {
                    var data = await drawingHelper.GetDataByBindingDataSourceAsync(CellType.Items);
                    return new object[] { data };
                }
            });
        }
    }
```

代码说明：
Items 属性修改为数据源属性。GetHeadlessBrowserPreviewControl 方法添加了 GetHeadlessBrowserPreviewControlOptions 参数，并在参数中使用 GetDataByBindingDataSourceAsync 方法获取数据库数据，在通过参数把数据发给无头浏览器。
前端代码修改如下：

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.content = $("<div style='width:100%;height:100%;'></div>");
        this.title = $("<h3/>");
        this.items = $("<ul/>");
        this.content.append(this.title);
        this.content.append(this.items);

        return this.content;
    }
    onPageLoaded() {
        this.onFormulaResultChanged(this.CellElement.CellType.Title, result => {
            this.title.text(result)
        });
        const loadData = (data) => {
            for (const item of data) {
                const itemDom = $("<li>");
                this.items.append(itemDom);
                this.onFormulaResultChanged(item.Name, result => {
                    itemDom.text(result)
                });
            }
        }

        if (this.isDesignerPreview) {
            loadData(this.designerPreviewCustomArgs[0])
        }
        else {
            this.getBindingDataSourceValue(this.CellElement.CellType.Items, null, data => {
                loadData(data);
            }, true);
        }
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

通过 this.isDesignerPreview 判断是否为设计时预览，如果是设计时预览，则通过 designerPreviewCustomArgs 属性获取设计时参数（参数中为设计器中获取的数据表数据）；不为设计时预览时，通过 getBindingDataSourceValue 方法获取数据。
这样，即可预览数据库中的数据了。

通过GetDataByBindingDataSourceAsync方法获取数据表数据，出于性能考虑，默认最大获取行数为 2000行，如果要修改，可以通过第二个参数来设置：

```auto
await drawingHelper.GetDataByBindingDataSourceAsync(CellType.Items, new GetDataByBindingDataSourceOptions() { MaxQueryRows = 100 });
```

##### 控制设计时预览刷新

默认情况下，任何属性变化都会触发单元格重绘。如果单元格有一些属性不会影响预览（如命令，行为控制等），修改时重绘会有不必要性能损失。可以通过设置 EffectPreviewPropertyNames 属性，声明属性列表。此时，只有在属性列表中的属性被修改才会触发重绘。

```csharp
public class MyPluginCellTypeDesigner : CellTypeDesigner<MyPluginCellType>
{
    public override FrameworkElement GetDrawingControl(ICellInfo cellInfo, IDrawingHelper drawingHelper)
    {
        return drawingHelper.GetHeadlessBrowserPreviewControl(new GetHeadlessBrowserPreviewControlOptions()
        {
            EffectPreviewPropertyNames = new string[]
            {
                    nameof(MyPluginCellType.Title),
                    nameof(MyPluginCellType.Items)
            }
        });
    }
}
```

同时，设计时预览会有缓存逻辑。影响属性的值发生变化，或者单元格大小发生变化时，会刷新缓存。如果在上述设置都没有发生变化，但是设计时预览需要刷新时（如数据源发生了变化），可以给单元格标注 SupportRefreshPreviewAttribute，来添加刷新设计时预览菜单项。

```auto
    [Designer(typeof(MyPluginCellTypeDesigner))]
    [SupportRefreshPreview]
    public class MyPluginCellType : CellType
    {
        [FormulaProperty]
        [DisplayName("标题")]
        public object Title { get; set; }

        [BindingDataSourceProperty(Columns = "Name:项目")]
        [DisplayName("内容")]
        public IBindingDataSource Items { get; set; }
    }
```

设计器效果：