# 单元格设计时支持 - 设计时预览 (Design-Time Preview)

## 参考资料
[支持设计时预览 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/supportsdesigntimepreview)

## 概述
让插件单元格在设计器中显示所见即所得的效果。
支持两种实现方式：
1. **WPF (传统方式)**: 需要编写 XAML 和 C# 代码，手动绘制 UI。
2. **无头浏览器 (推荐, V10+)**: 复用运行时的 JS 代码，自动渲染预览图。

## 1. 使用 WPF 实现 (传统)
需要重写 `CellTypeDesigner` 的 `GetDrawingControl` 方法，返回一个 WPF `UserControl`。

```csharp
public class MyPluginCellTypeDesigner : CellTypeDesigner<MyPluginCellType>
{
    public override FrameworkElement GetDrawingControl(ICellInfo cellInfo, IDrawingHelper drawingHelper)
    {
        // 返回自定义的 WPF 控件
        return new MyPluginCellTypeDrawingControl(this.CellType, cellInfo, drawingHelper);
    }
}
```

## 2. 使用无头浏览器实现 (推荐)
[使用无头浏览器实现设计时预览 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/supportsdesigntimepreview/design-time-preview-in-Chromium)

直接调用 `drawingHelper.GetHeadlessBrowserPreviewControl()`。

```csharp
public class MyPluginCellTypeDesigner : CellTypeDesigner<MyPluginCellType>
{
    public override FrameworkElement GetDrawingControl(ICellInfo cellInfo, IDrawingHelper drawingHelper)
    {
        // 使用 Chromium 无头浏览器渲染，复用 JS 代码
        return drawingHelper.GetHeadlessBrowserPreviewControl();
    }
}
```

### JS 端区分设计时与运行时
在 JS 代码中，可以通过 `this.isDesignerPreview` 判断当前是否处于设计时预览模式。

#### 最佳实践：防止预览“白屏” (Error Handling)
在开发过程中，JS 错误会导致设计器中的插件区域直接变成空白，无法调试。建议使用 `try-catch` 包裹渲染逻辑，并将错误显示在设计器中。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const container = $("<div></div>");
        
        try {
            // 核心渲染逻辑
            this.render(container);
            
            // 设计时特殊逻辑：如果属性为空，显示提示文本
            if (this.isDesignerPreview && !this.CellElement.CellType.Title) {
                container.append($("<div style='color:gray'>请设置标题</div>"));
            }
        } catch (e) {
            console.error(e);
            // 仅在设计时显示错误堆栈，方便排查
            if (this.isDesignerPreview) {
                container.css({ color: "red", padding: "5px", border: "1px solid red" })
                         .text("Preview Error: " + e.message);
            }
        }
        
        return container;
    }
}
```
