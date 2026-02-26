# 集成单元格插件到表格中 - 常见问题 (FAQ)

## 参考资料
[表格编辑常见问题及解决方案 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/integrate-cell-plugin-to-listview/doubleclick-to-edit-in-listview/issues-and-solutions)

## 1. 直接键盘输入进入编辑模式
用户无需双击，选中单元格后直接打字即可进入编辑模式。

**C# 配置**:
```csharp
new ListViewOptions() { 
    AllowEdit = true, 
    AllowEnterEditMode = true,
    AcceptsTextInput = true // 开启
}
```

## 2. 下拉菜单点击导致退出编辑
如果下拉菜单 DOM 挂载在 Body 上（游离于单元格 DOM 之外），点击时会被误判为点击了表格外部。

**解决**: 使用 `setDropDownAttributeInListView` 标记下拉 DOM。
```javascript
onPageLoaded(info) {
    if (this.isInListView) {
        this.setDropDownAttributeInListView(this.getDropDownElement());
    }
    super.onPageLoaded(info);
}
```

## 3. 点击按钮直接进入编辑模式（无需双击）
**解决**: 命中测试 + 手动触发 `startEdit`。

```javascript
onClickInListView(hitInfo, context) {
    if (hitInfo?.type === 'DropDownButton') {
        // 1. 触发编辑模式
        this.parentListView.startEdit();
        // 2. 立即显示下拉框
        // 注意：此时 createContent 已执行，DOM 已创建
        this.showDropDown(); 
    }
}
```

## 4. 显示值与实际值不同 (Lookup)
如：值为 ID，显示为 Name。表格未加载所有数据时无法获取对应文本。

**解决**: 开启 `AutoCacheTextOnDemand`。
```csharp
new ListViewOptions() {
    BindingDataSource = DataSource,
    ValueFieldName = "ID",
    TextFieldName = "Name",
    AutoCacheTextOnDemand = true // 自动按需缓存文本
}
```

**JS**:
```javascript
paintInListView(ctx, value, ...) {
    const text = this.getTextByValue(value); // 使用此方法获取显示文本
    // 绘制 text ...
}
```
