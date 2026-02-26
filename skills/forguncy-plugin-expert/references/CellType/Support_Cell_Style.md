# 和活字格原生功能集成 - 支持单元格样式 (Support Cell Style)

## 参考资料
[支持单元格样式 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/supportcell-type-style-root/supportcelltypestyle)

## 概述
让插件单元格支持活字格原生的样式设置（如背景色、字体、对齐等）。
**不需要修改 C# 代码**，只需在 JS 中处理样式。

## 基础用法
在 `createContent` 中获取 `this.CellElement.StyleInfo` 并应用到 DOM 元素。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const div = $("<div style='width:100%;height:100%;display:flex'></div>");
        const style = this.CellElement.StyleInfo;
        
        // 转换样式信息为 CSS 对象
        const cssStyle = this.createFontStyleCss(style);
        
        // 处理特殊样式（下划线、删除线）
        if (style.Underline || style.Strikethrough) {
            const textDecoration = [];
            if (style.Underline) textDecoration.push("underline");
            if (style.Strikethrough) textDecoration.push("line-through");
            cssStyle["text-decoration"] = textDecoration.join(" ");
        }

        // 处理对齐方式 (Flex布局示例)
        if (style.VerticalAlignment === Forguncy.Plugin.CellVerticalAlignment.Center) {
            cssStyle["align-items"] = "center";
        } else if (style.VerticalAlignment === Forguncy.Plugin.CellVerticalAlignment.Bottom) {
            cssStyle["align-items"] = "end";
        }
        
        if (style.HorizontalAlignment === Forguncy.Plugin.CellHorizontalAlignment.Center) {
            cssStyle["justify-content"] = "center";
        } else if (style.HorizontalAlignment === Forguncy.Plugin.CellHorizontalAlignment.Right) {
            cssStyle["justify-content"] = "end";
        }

        div.css(cssStyle);
        this.content = div;
        return div;
    }

    // 辅助方法：创建基础字体 CSS
    createFontStyleCss(style) {
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

    // 支持运行时样式修改（如条件格式）
    setFontStyle(style) {
        const cssStyle = this.createFontStyleCss(style);
        this.content.css(cssStyle);
    }
    
    setValueToElement(_, value) {
        this.content.text(value?.toString());
    }
}
```
