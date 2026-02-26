# 添加属性 - 公式属性 (Formula Property)

## 参考资料
[公式属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/formulaproperty)

## 概述
公式属性允许用户输入固定值或公式（以 `=` 开头）。属性类型必须为 `object`。

## 基础用法
```csharp
public class MyPluginCellType : CellType
{
    [FormulaProperty]
    [DisplayName("计算值")]
    public object MyProperty { get; set; }
}
```

## JS 处理逻辑
需要在 JS 中计算公式的值。

### 推荐写法 (V10.0+)
使用 `onFormulaResultChanged` 监听公式变化，性能更好且能区分不同属性。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.content = $("<div></div>");
        return this.content;
    }
    
    onPageLoaded() {
        // 监听公式计算结果变化
        this.onFormulaResultChanged(this.CellElement.CellType.MyProperty, result => {
            this.content.text(result);
        });
    }
}
```

### 旧版写法 (不推荐)
使用 `evaluateFormula` 和 `onDependenceCellValueChanged`。

```javascript
onPageLoaded() {
    const calc = () => {
        const result = this.evaluateFormula(this.CellElement.CellType.MyProperty);
        this.content.text(result);
    };
    calc();
    this.onDependenceCellValueChanged(calc);
}
```

## 高级用法

### 1. 提供备选列表 (RecommendedValues)
```csharp
[FormulaProperty(RecommendedValues = "选项A|选项B|选项C")]
public object MyProperty { get; set; }
```

### 2. 支持多行输入 (AcceptsReturn)
```csharp
[FormulaProperty(AcceptsReturn = true)]
public object MyProperty { get; set; }
```

### 3. 关闭多语言支持 (CanSelectResource)
默认开启多语言。
```csharp
[FormulaProperty(CanSelectResource = false)]
public object MyProperty { get; set; }
```
