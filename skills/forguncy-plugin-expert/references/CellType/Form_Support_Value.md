# 开发表单类单元格 - 支持单元格值 (Support Cell Value)

## 参考资料
[支持单元格值 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportcellvalues)

## 概述
表单类单元格的核心是与数据绑定。通过 `setValueToElement`, `getValueFromElement` 和 `commitValue` 实现双向绑定。

## 基础用法
在 JS 类中实现以下方法：

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.input = $("<input>");
        
        // 当用户修改值时，提交到活字格数据模型
        this.input.change(() => {
            this.commitValue();
        });
        
        return this.input;
    }

    // 活字格 -> 单元格: 当数据模型变化时，更新 UI
    setValueToElement(_, value) {
        this.input.val(value?.toString());
    }

    // 单元格 -> 活字格: 当调用 commitValue 时，活字格会调用此方法获取新值
    getValueFromElement() {
        return this.input.val();
    }
}
```
