# 开发表单类单元格 - 支持数据校验 (Data Verification)

## 参考资料
[支持数据校验 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportdataverification)

## 概述
集成活字格原生的数据校验功能（如必填、数值范围等）。

## C# 实现
实现 `ISupportDataValidation` 接口。

```csharp
public class MyPluginCellType : CellType, ISupportDataValidation
{
    // 用于存储校验规则链接
    public DataValidationLink DataValidationLink { get; set; }
}
```

## JS 实现
在适当的时机（如 blur）调用 `validate()`，在输入时调用 `hideValidateTooltip()`。
**关键点**: DOM 元素必须设置 ID。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.input = $("<input>");
        
        // 1. 必须设置 ID，否则 Tooltip 无法显示
        this.input.attr("id", this.ID);
        
        this.input.blur(() => {
            // 2. 触发校验
            this.validate();
        });
        
        this.input.on("input", () => {
            // 3. 隐藏之前的错误提示
            this.hideValidateTooltip();
        });
        
        return this.input;
    }
}
```
