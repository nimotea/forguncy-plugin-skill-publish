# 集成单元格插件到表格中 - 鼠标交互 (Mouse Interaction)

## 参考资料
[表格中实现鼠标交互 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/integrate-cell-plugin-to-listview/mouse-interaction-in-listview)

## 概述
表格（ListView）通过 `getHitTestTypeInListView` 方法进行点击检测，结合 `onMouseMove`, `onClick` 等事件处理鼠标交互。

## 核心方法

### 1. 命中测试 (getHitTestTypeInListView)
判断鼠标坐标是否落在单元格的特定区域（如按钮、图标）。
返回自定义的字符串（Type）或对象，用于区分不同区域。

```javascript
getHitTestTypeInListView(x, y, cellRect, ctx) {
    const dotX = cellRect.x + 10;
    const dotY = cellRect.y + cellRect.height / 2;
    const radius = 5;
    
    // 检查是否点击了圆点
    const dx = x - dotX;
    const dy = y - dotY;
    if (dx * dx + dy * dy <= radius * radius) {
        return 'Dot'; // 命中圆点区域
    }
    return null; // 未命中
}
```

### 2. 鼠标移动 (onMouseMoveInListView)
处理鼠标悬停效果。
```javascript
onMouseMoveInListView(hitInfo, context) {
    if (hitInfo?.type === 'Dot') {
        context.cursor = 'pointer'; // 改变光标
        this._hoverType = 'Dot';    // 记录悬停状态
    } else {
        this._hoverType = null;
    }
    // 必须调用 super
    super.onMouseMoveInListView(hitInfo, context);
}
```

### 3. 鼠标点击 (onClickInListView)
处理点击事件。
```javascript
onClickInListView(hitInfo, context) {
    if (hitInfo?.type === 'Dot') {
        console.log("圆点被点击");
        // 执行自定义逻辑
    }
}
```

### 4. 渲染反馈 (paintInListView)
在渲染时根据悬停状态改变外观。
```javascript
paintInListView(ctx, value, cellRect, cellStyle, context) {
    // ...
    // 如果当前行被悬停且命中了圆点
    if (context.rowIndex === this._hoverRowIndex && this._hoverType === 'Dot') {
        ctx.globalAlpha = 0.6; // 改变透明度
    }
    // ...
}
```
