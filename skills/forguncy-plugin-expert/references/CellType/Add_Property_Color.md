# 添加属性 - 颜色属性 (Color Property)

## 参考资料
[颜色属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/colorproperty)

## 概述
提供颜色选择器。属性类型必须为 `string`。

## 基础用法 ([ColorProperty])
```csharp
public class MyPluginCellType : CellType
{
    [ColorProperty]
    public string MyColor { get; set; }
}
```

## 高级用法

### 1. 支持无填充 (SupportNoFill)
```csharp
[ColorProperty(SupportNoFill = true)]
public string MyColor { get; set; }
```

### 2. 支持半透明 (SupportTranslucency)
```csharp
[ColorProperty(SupportTranslucency = true)]
public string MyColor { get; set; }
```

## JS 处理逻辑
活字格颜色格式（如 "Accent 1"）需转换为 CSS 颜色。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const colorStr = this.CellElement.CellType.MyColor;
        // 转换为 CSS 颜色
        const cssColor = Forguncy.ConvertToCssColor(colorStr);
        
        const div = $("<div></div>");
        div.css("background-color", cssColor);
        return div;
    }
}
```
