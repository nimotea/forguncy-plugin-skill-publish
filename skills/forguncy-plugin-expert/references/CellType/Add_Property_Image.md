# 添加属性 - 图片属性 (Image Property)

## 参考资料
[图片属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/image-property)

## 概述
提供图片选择对话框（支持本地上传和内置图标）。属性类型必须为 `object` 或 `ImageValue`。

## 基础用法 ([ImageValueProperty])
```csharp
public class MyPluginCellType : CellType
{
    [ImageValueProperty]
    public object MyImage { get; set; }
}
```

## 高级用法

### 1. 禁止 SVG (SupportSvg)
```csharp
[ImageValueProperty(SupportSvg = false)]
public object MyImage { get; set; }
```

### 2. 默认选中内置图标 (DefaultActiveTabIndex)
`0`: 本地图片, `1`: 内置图标
```csharp
[ImageValueProperty(DefaultActiveTabIndex = 1)]
public object MyImage { get; set; }
```

### 3. 默认图标颜色 (DefaultIconColor)
```csharp
[ImageValueProperty(DefaultIconColor = "Accent 1")]
public object MyImage { get; set; }
```

### 4. 跟随单元格字体颜色 (SupportUseCellColor)
```csharp
[ImageValueProperty(SupportUseCellColor = true, DefaultUseCellColor = true)]
public object MyImage { get; set; }
```

## JS 处理逻辑
需要处理普通图片、内置图标和 SVG 的不同加载方式。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const image = this.CellElement.CellType.MyImage;
        const container = $("<div></div>");

        if (image && image.Name) {
            let src = "";
            // 1. 获取图片路径
            if (image.BuiltIn) {
                src = Forguncy.Helper.SpecialPath.getBuiltInImageFolderPath() + image.Name;
            } else {
                src = Forguncy.Helper.SpecialPath.getImageEditorUploadImageFolderPath() + encodeURIComponent(image.Name);
            }

            // 2. 处理 SVG
            if (Forguncy.ImageDataHelper.IsSvg(src)) {
                $.get(src, (data) => {
                    const svg = $(data.documentElement);
                    // 处理 SVG 颜色
                    const color = image.UseCellTypeForeColor ? "currentColor" : image.Color;
                    Forguncy.ImageHelper.preHandleSvg(svg, color);
                    container.append(svg);
                });
            } else {
                // 3. 处理普通图片
                container.append($("<img src='" + src + "'>"));
            }
        }
        return container;
    }
}
```
