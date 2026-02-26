# 添加属性 - 命令属性 (Command Property)

## 参考资料
[命令属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/commandproperty)

## 概述
允许用户在单元格上绑定命令（如单击命令、右键命令）。属性类型必须为 `object`。

## 基础用法 ([CustomCommandObject])
```csharp
public class MyPluginCellType : CellType
{
    [DisplayName("单击命令")]
    [CustomCommandObject]
    public object ClickCommand { get; set; }
}
```

## JS 处理逻辑
使用 `executeCustomCommandObject` 执行命令。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const btn = $("<button>点击我</button>");
        const command = this.CellElement.CellType.ClickCommand;
        
        btn.click(() => {
            // 执行绑定的命令
            // 第二个参数是命令参数（可选）
            this.executeCustomCommandObject(command, { "param1": "value" });
        });
        
        return btn;
    }
}
```
