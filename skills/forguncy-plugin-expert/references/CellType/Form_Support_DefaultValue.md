# 开发表单类单元格 - 支持默认值 (Default Value)

## 参考资料
[支持默认值 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportdefaultvalue)

## 概述
让单元格支持设置默认值。

## C# 实现
实现 `ISupportDefaultValue` 接口。

```csharp
public class MyPluginCellType : CellType, ISupportDefaultValue
{
    [FormulaProperty] // 必须支持公式
    [DisplayName("默认值")]
    public object DefaultValue { get; set; }

    // True: 尝试智能转换类型 (如 "1,234" -> 1234)
    // False: 保持原始类型 (如文本)
    public bool NeedFormatDefaultValue => false;
}
```

## 自定义默认值逻辑
如果默认值依赖其他属性计算，可以重写 JS 中的 `getDefaultValue`。

```javascript
getDefaultValue() {
    return {
        Value: "自定义计算值"
    };
}
```
