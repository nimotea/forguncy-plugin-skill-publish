# 开发表单类单元格 - 支持禁用 (Support Disable)

## 参考资料
[支持禁用 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportdisable)

## 概述
实现 `ISupportDisable` 接口，使单元格支持禁用状态。

## C# 实现
```csharp
public class MyPluginCellType : CellType, ISupportDisable
{
    [DisplayName("禁用")]
    public bool IsDisabled { get; set; }
}
```

## JS 实现
重写 `disable` 和 `enable` 方法。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    disable() {
        super.disable(); // 必须调用
        
        // 使用 this.isDisabled() 判断真实状态
        if (this.isDisabled()) {
            this.input.attr("disabled", "disabled");
        }
    }

    enable() {
        super.enable(); // 必须调用
        
        if (!this.isDisabled()) {
            this.input.removeAttr("disabled");
        }
    }
}
```
