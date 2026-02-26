# 和活字格原生功能集成 - 集成单元格插件到表格中 (ListView Integration)

## 参考资料
[集成单元格插件到表格中 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/integrate-cell-plugin-to-listview)

## 概述
*(此特性为 V11.0.100.0 新增)*
活字格表格（ListView）底层使用 Canvas 渲染。为了让插件单元格在表格中正常显示，必须实现 `paintInListView` 方法，使用 Canvas API 手动绘制单元格内容。

## 实现步骤
1. 开发普通的单元格插件（用于非表格环境）。
2. 在 JS 类中添加 `paintInListView` 方法（用于表格环境）。

## 示例代码
以“状态显示单元格”为例：
- 值=1: 黄色圆点 + "警告"
- 值=2: 红色圆点 + "错误"
- 其他: 绿色圆点 + "正常"

```javascript
class StateCellType extends Forguncy.Plugin.CellTypeBase {
    // 1. 普通视图渲染 (createContent)
    createContent() {
        const container = $("<div style='display:flex;align-items:baseline;gap:3px'></div>");
        this.point = $("<div style='width:10px;height:10px;border-radius:10px;'></div>");
        this.label = $("<span>")
        container.append(this.point);
        container.append(this.label);
        return container;
    }

    setValueToElement(_, value) {
        this.updateStyle(value);
    }

    // 辅助方法：获取状态配置
    getState(value) {
        switch (value?.toString()) {
            case "1": return { color: 'yellow', text: '警告' };
            case "2": return { color: 'red', text: '错误' };
            default: return { color: 'green', text: '正常' };
        }
    }

    // 2. 表格视图渲染 (Canvas 绘制)
    paintInListView(ctx, value, cellRect, cellStyle, context) {
        const state = this.getState(value);

        // 计算坐标
        const dotRadius = 5;
        const dotX = cellRect.x + dotRadius;
        const dotY = cellRect.y + cellRect.height / 2;

        // 绘制圆点
        ctx.beginPath();
        ctx.arc(dotX, dotY, dotRadius, 0, Math.PI * 2);
        ctx.fillStyle = state.color;
        ctx.fill();

        // 绘制文字
        const textX = dotX + dotRadius + 3;
        const textY = dotY; // 垂直居中需配合 textBaseline
        
        ctx.font = '14px 微软雅黑';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = 'black'; // 或使用 cellStyle.Foreground
        ctx.fillText(state.text, textX, textY);
    }
}
```

## paintInListView 参数说明
- `ctx`: Canvas 绘图上下文 (CanvasRenderingContext2D)
- `value`: 当前单元格的值
- `cellRect`: 单元格区域 `{x, y, width, height}`
- `cellStyle`: 单元格样式信息
- `context`: 上下文信息
