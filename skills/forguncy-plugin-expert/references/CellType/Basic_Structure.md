# 单元格插件基础结构 (Basic Structure)

## 参考资料
[一个简单的单元格插件 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/asimplecelltypeplugin)

## 概述
单元格插件通常包含两个核心文件：
1. **C# 文件 (`MyPluginCellType.cs`)**: 定义服务端属性、设计时行为和元数据。
2. **JavaScript 文件 (`MyPluginCellType.js`)**: 定义运行时在浏览器中的渲染逻辑和交互行为。

## C# 代码结构 (`MyPluginCellType.cs`)

必须继承自 `GrapeCity.Forguncy.Plugin.CellType` 类。

```csharp
using GrapeCity.Forguncy.Plugin;
using System.ComponentModel;

namespace MyPlugin
{
    // 指定插件图标
    [Icon("pack://application:,,,/MyPlugin;component/Resources/Icon.png")]
    // 指定设计时功能类（可选）
    [Designer("MyPlugin.Designer.MyPluginCellTypeDesigner, MyPlugin")]
    public class MyPluginCellType : CellType
    {
        // 定义插件属性，可在设计器中设置
        [DisplayName("我的属性")]
        public string MyProperty { get; set; } = "默认值";

        // 定义支持命令的属性
        [DisplayName("单击命令")]
        [CustomCommandObject] // 标记该属性为命令对象
        public object ClickCommand { get; set; }

        // 重写 ToString 方法，设置在设计器单元格中显示的文本
        public override string ToString()
        {
            return "我的插件单元格";
        }
    }
}
```

### 关键点
- **[Icon]**: 指定插件图标资源路径。
- **[Designer]**: 指定自定义设计器类（如需要自定义编辑界面）。
- **属性**: 定义的公共属性会自动出现在设计器的属性面板中。
- **[CustomCommandObject]**: 用于标记属性为命令容器，允许用户绑定命令。

## JavaScript 代码结构 (`MyPluginCellType.js`)

必须继承自 `Forguncy.Plugin.CellTypeBase` 类，并注册插件。

```javascript
/// <reference path="../Declarations/forguncy.d.ts" />
/// <reference path="../Declarations/forguncy.Plugin.d.ts" />

class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        // 重要：严禁在此方法上使用 async 关键字，必须同步返回 DOM 元素
        // 1. 获取单元格模型数据（C#中定义的属性值）
        const cellType = this.CellElement.CellType;
        const propValue = cellType.MyProperty;

        // 2. 创建 DOM 元素
        // 建议使用 jQuery 创建
        const container = $("<div></div>");
        container.text(propValue);
        
        // 处理样式
        container.css("width", "100%");
        container.css("height", "100%");

        // 3. 绑定事件（如果需要）
        if (cellType.ClickCommand) {
            container.click(() => {
                // 执行绑定的命令
                this.executeCustomCommandObject(cellType.ClickCommand);
            });
        }

        // 4. 返回 DOM 元素
        return container;
    }

    onPageLoaded() {
        // 页面加载完成后调用
        // 建议在此处初始化依赖 DOM 的第三方库或绑定全局事件
    }

    destroy() {
        // 单元格销毁时调用
        // 重要：凡是涉及到 window/document 的事件绑定或定时器，必须在此处手动解绑/清除
        // 示例：window.removeEventListener('resize', this._resizeHandler);
        super.destroy();
    }
}

// 注册单元格插件
// 参数格式: "命名空间.类名, 程序集名称"
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

### 关键点
- **createContent()**: 核心方法，用于创建和返回单元格的 DOM 结构。
- **this.CellElement.CellType**: 获取服务端传递过来的属性配置对象。
- **this.executeCustomCommandObject()**: 执行 C# 中定义的命令属性。
- **registerCellType**: 必须调用此方法注册 JS 类与 C# 类的映射关系。
