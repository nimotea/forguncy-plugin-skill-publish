# 添加单元格操作 - 修改属性值 (Modify Property Value)

## 参考资料
[添加修改属性值操作 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addcellaction/addmodificationattributevalueoperation)

## 概述
允许用户在运行时通过“操作单元格”命令动态修改单元格的属性（例如动态改变按钮文本、颜色等）。

## 实现步骤

### 1. 标记属性 (C#)
使用 `[SupportModifyByRuntimeProperty]` 特性。

```csharp
public class MyPluginCellType : CellType
{
    [SupportModifyByRuntimeProperty]
    [DisplayName("按钮文本")]
    public string ButtonText { get; set; }
}
```

### 2. 实现修改逻辑 (JS)
在 JS 类中添加 `set_属性名(value)` 方法。
**注意**: 命名规则必须是 `set_` + 属性名。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    // ... createContent ...

    // 运行时修改 ButtonText 属性时调用
    set_ButtonText(value) {
        // 更新 UI
        this.content.text(value);
    }
}
```

## 高级用法
强制使用公式编辑器：
```csharp
[SupportModifyByRuntimeProperty(UseFormulaEditor = true)]
public string ButtonText { get; set; }
```
