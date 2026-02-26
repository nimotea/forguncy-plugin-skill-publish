# 开发表单类单元格 - 支持只读 (Support ReadOnly)

## 参考资料
[支持只读 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportreadonly)

## 概述
实现 `ISupportReadOnly` 接口，使单元格支持只读属性设置以及运行时的只读状态切换。

## C# 实现
```csharp
public class MyPluginCellType : CellType, ISupportReadOnly
{
    [DisplayName("只读")]
    public bool ReadOnly { get; set; }
}
```

## JS 实现
重写 `setReadOnly` 方法。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    // ... createContent 等方法 ...

    setReadOnly(value) {
        // 必须先调用基类方法
        super.setReadOnly(value);
        
        // 使用 this.isReadOnly() 获取最终的只读状态
        // (因为可能受权限控制影响，value 参数可能不准)
        if (this.isReadOnly()) {
            this.input.attr("readonly", "readonly");
        } else {
            this.input.removeAttr("readonly");
        }
    }
}
```
