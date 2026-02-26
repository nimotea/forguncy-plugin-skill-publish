# 添加属性 - 枚举属性 (Enum Property)

## 参考资料
[枚举类型属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/enumtypeproperty)

## 概述
枚举类型的属性会自动在设计器中显示为下拉列表。

## 基础用法
```csharp
public enum MyEnum
{
    [Description("选项一")]
    Option1,
    [Description("选项二")]
    Option2
}

public class MyPluginCellType : CellType
{
    public MyEnum MyProperty { get; set; }
}
```

## JS 处理逻辑
C# 枚举在 JS 中会被序列化为整数（索引）。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const value = this.CellElement.CellType.MyProperty;
        let text = "";
        
        // 处理枚举值（整数）
        switch (value) {
            case 0: text = "选项一"; break;
            case 1: text = "选项二"; break;
        }
        
        return $("<div>" + text + "</div>");
    }
}
```
