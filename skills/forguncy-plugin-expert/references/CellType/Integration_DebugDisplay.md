# 和活字格原生功能集成 - 自定义调试显示属性 (Debug Display)

## 参考资料
[自定义调试显示属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/debug-display-properties)

## 概述
活字格 V10.0.100.0+ 提供了页面元素调试功能。插件可以通过重写 `getDebugValue()` 方法，自定义在调试面板中显示的信息。
这对于像组合框这样“值”和“显示文本”分离的控件非常有用。

## 实现方法
重写 JS 类中的 `getDebugValue` 方法。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        // ...
        return $("<div>...</div>");
    }

    // 重写调试值获取方法
    getDebugValue() {
        // 获取默认的调试值（通常是 setValueToElement 设置的值）
        const value = super.getDebugValue();
        
        // 返回自定义对象
        return {
            "当前值": value,
            "显示文本": this.getTextByValue(value), // 假设有这个辅助方法
            "额外状态": "正常"
        };
    }
}
```

## 效果
在活字格运行时的调试面板中，选中该单元格时，将显示自定义的 JSON 对象结构。
