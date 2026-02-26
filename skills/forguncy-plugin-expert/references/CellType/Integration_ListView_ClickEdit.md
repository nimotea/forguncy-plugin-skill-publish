# 集成单元格插件到表格中 - 直接点击编辑 (Click to Edit)

## 参考资料
[表格中实现直接点击编辑 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/integrate-cell-plugin-to-listview/click-to-edit-in-listview)

## 概述
实现点击单元格（或特定区域）时直接修改值，而不需要进入完全的编辑模式（输入框模式）。适用于复选框、状态切换等场景。

## 实现步骤

### 1. 开启编辑权限 (C#)
```csharp
public override ListViewOptions ListViewOptions
{
    get
    {
        return new ListViewOptions()
        {
            AllowEdit = true // 允许编辑
        };
    }
}
```

### 2. 处理点击事件 (JS)
在 `onClickInListView` 中直接修改 `context.value`。

```javascript
onClickInListView(hitInfo, context) {
    // 检查只读或禁用状态
    if (context.cellState.isReadOnly || context.cellState.isDisabled) {
        return;
    }

    // 如果命中了特定区域
    if (hitInfo?.type === 'Dot') {
        // 修改值：例如在 0, 1, 2 之间循环
        const newValue = (Number(context.value ?? 0) + 1) % 3;
        context.value = newValue; // 表格会自动保存并重绘
    }
}
```
