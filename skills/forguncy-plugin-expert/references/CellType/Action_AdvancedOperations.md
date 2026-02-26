# 添加单元格操作 - 高级单元格操作 (Advanced Cell Operations)

## 参考资料
[添加高级单元格操作 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addcellaction/addadvancedcelloperations)

## 概述
定义自定义的方法（操作），供“操作单元格”命令调用。支持传递参数和返回值。

## 1. 基础操作 (无参)
**C#**:
```csharp
public class MyPluginCellType : CellType
{
    [RunTimeMethod]
    public void MyOperation() { }
}
```

**JS**:
```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    MyOperation() {
        alert("被调用");
    }
}
```

## 2. 带参数的操作
**C#**:
```csharp
[RunTimeMethod]
public void ShowMessage(
    [ItemDisplayName("标题")] string title,
    [ItemDisplayName("内容")] string content
) { }
```

**JS**:
```javascript
ShowMessage(title, content) {
    alert(title + ": " + content);
}
```

## 3. 带返回值的操作
**C#**:
```csharp
[RunTimeMethod]
public GetInfoResult GetInfo() { return null; }

public class GetInfoResult
{
    [DisplayName("当前值")]
    public string CurrentValue { get; set; }
}
```

**JS**:
```javascript
GetInfo() {
    return {
        CurrentValue: this.getValueFromElement()
    };
}
```

## 4. 最佳实践：状态管理与防御性校验

### 状态管理
建议在 `CellType` 实例中通过变量（如 `this._data`）存储中间状态或缓存数据，而不是每次都从 DOM 中读取。这可以提高性能并使逻辑更清晰。

**JS (CellType)**:
```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    constructor() {
        super();
        this._cache = {}; // 存储状态
    }
    
    updateState(key, value) {
        this._cache[key] = value;
        // 根据状态更新 UI...
    }
}
```

### 防御性校验 (Command 侧)
当在命令中操作特定单元格时，务必检查目标单元格是否存在及其类型。

**JS (Command)**:
```javascript
var cell = Forguncy.Page.getCell("MyCellName");
if (cell) {
    var cellType = cell.getCellType();
    // 检查方法是否存在，以防目标单元格不是预期的插件类型
    if (cellType && typeof cellType.updateState === "function") {
        cellType.updateState("status", "active");
    }
}
```

### 智能参数推断 (Intelligent Parameter Inference)
为了提升易用性，建议在 API 设计中采用“上下文感知”模式。

**反面典型 (暴露内部细节)**:
```javascript
// 用户需要理解 updateType 0 代表重置，1 代表局部更新
Refresh(updateType) { ... } 
```

**推荐做法 (智能推断)**:
```javascript
Refresh() {
    // 从设计器配置的属性中自动判断逻辑
    const isSilent = this.CellElement.CellType.SilentMode; 
    if (isSilent) {
        this.partialUpdate();
    } else {
        this.fullReload();
    }
}
```
