# 集成单元格插件到表格中 - 双击编辑 (Double Click to Edit)

## 参考资料
[表格中实现双击编辑 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/integrate-cell-plugin-to-listview/doubleclick-to-edit-in-listview)

## 概述
实现双击单元格进入编辑模式（显示输入框、下拉框等 DOM 元素）。编辑完成后（失去焦点），值回写到表格。

## 实现步骤

### 1. 开启编辑模式 (C#)
```csharp
public override ListViewOptions ListViewOptions
{
    get
    {
        return new ListViewOptions()
        {
            AllowEdit = true,
            AllowEnterEditMode = true // 允许进入编辑模式
        };
    }
}
```

### 2. 实现编辑相关方法 (JS)
编辑模式复用 `createContent` 创建的 DOM。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    // 创建 DOM (用于编辑模式)
    createContent() {
        this.input = $("<input>");
        return this.input;
    }

    // 初始化编辑值
    setValueToElement(_, value) {
        this.input.val(value);
    }

    // 获取编辑后的值 (关键)
    getValueFromElement() {
        return this.input.val();
    }
    
    // 编辑开始通知
    onEditStartInListView() {
        // 可选：设置焦点
        this.input.focus();
    }
    
    // 编辑结束通知
    onEditEndInListView() {
        // 可选：清理工作
    }
}
```
