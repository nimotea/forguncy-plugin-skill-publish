# 添加属性 - 字符串属性 (String Property)

## 参考资料
[字符串属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/stringproperty)

## 概述
字符串属性是最基础的属性类型。默认情况下，`string` 类型的公共属性会自动在设计器中显示为文本输入框。

## 基础用法
```csharp
public class MyPluginCellType : CellType
{
    [DisplayName("我的文本")]
    public string MyProperty { get; set; } = "默认值";
}
```

## 高级用法 ([TextProperty])
使用 `[TextProperty]` 特性可以获得更多控制选项。

### 1. 添加水印 (Watermark)
```csharp
[TextProperty(Watermark = "请输入名称...")]
public string MyProperty { get; set; }
```

### 2. 支持多行文本 (AcceptsReturn)
```csharp
[TextProperty(AcceptsReturn = true)]
public string MyProperty { get; set; }
```
*要求活字格版本 >= 10.0.0.0*

### 3. 支持多语言 (CanSelectResource)
允许用户选择应用资源中的字符串（实现国际化）。
```csharp
[TextProperty(CanSelectResource = true)]
public string MyProperty { get; set; }
```

**JS 处理多语言:**
```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        var cellParam = this.CellElement.CellType;
        // 自动处理多语言资源
        const propValue = this.getApplicationResource(cellParam.MyProperty);
        return $("<div>" + propValue + "<div>");
    }
}
```
