# 属性值联动 (Property Linkage)

在设计器中，有时需要实现当用户修改某个属性时，自动改变另一个属性的值（例如：选择“自定义模式”时，自动清空“预设选项”）。这可以通过在 Designer 类中重写 `OnPropertyEditorChanged` 方法来实现。

## 实现步骤

1. 创建或打开对应的 Designer 类（继承自 `CommandDesigner<T>`）。
2. 重写 `OnPropertyEditorChanged` 方法。
3. 判断发生变化的属性名 (`propertyName`)。
4. 通过 `properties` 字典获取目标属性的设置对象，并修改其 `Value`。

## 代码示例

假设有一个命令 `MyPluginServerCommand`，包含两个属性 `MyProperty1` (布尔值) 和 `MyProperty2` (字符串)。我们需要实现：当 `MyProperty1` 变为 `true` 时，自动将 `MyProperty2` 设置为 "真"；否则设置为 "假"。

### 1. 命令类定义

```csharp
using GrapeCity.Forguncy.Commands;
using System.ComponentModel;
using System.Threading.Tasks;

namespace MyPlugin
{
    // 关联 Designer
    [Designer("MyPlugin.Designer.MyPluginServerCommandDesigner, MyPlugin")]
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
    {
        [DisplayName("启用状态")]
        public bool MyProperty1 { get; set; }

        [DisplayName("状态描述")]
        public string MyProperty2 { get; set; }

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            return new ExecuteResult();
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

### 2. Designer 类实现

```csharp
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;
using System;
using System.Collections.Generic;

namespace MyPlugin.Designer
{
    public class MyPluginServerCommandDesigner : CommandDesigner<MyPluginServerCommand>
    {
        /// <summary>
        /// 当属性编辑器中的值发生变化时调用
        /// </summary>
        /// <param name="propertyName">发生变化的属性名</param>
        /// <param name="propertyValue">变化后的新值</param>
        /// <param name="properties">所有属性的编辑器设置字典</param>
        public override void OnPropertyEditorChanged(string propertyName, object propertyValue, Dictionary<string, IEditorSettingsDataContext> properties)
        {
            // 监听 MyProperty1 的变化
            if (propertyName == nameof(MyPluginServerCommand.MyProperty1))
            {
                // 获取 MyProperty2 的编辑器设置对象
                if (properties.TryGetValue(nameof(MyPluginServerCommand.MyProperty2), out var property2Setting))
                {
                    // 根据 MyProperty1 的新值设置 MyProperty2 的值
                    if (object.Equals(propertyValue, true))
                    {
                        property2Setting.Value = "真";
                    }
                    else
                    {
                        property2Setting.Value = "假";
                    }
                }
            }
            
            // 务必调用基类方法
            base.OnPropertyEditorChanged(propertyName, propertyValue, properties);
        }
    }
}
```

## 注意事项

1. **类型安全**：`propertyValue` 是 `object` 类型，使用时建议进行类型检查或安全转换（如 `object.Equals` 或 `as`）。
2. **属性名引用**：推荐使用 `nameof(ClassName.PropertyName)` 而不是硬编码字符串，以防重构时出错。
3. **获取目标属性**：从 `properties` 字典获取目标属性时，确保键名正确。
4. **基类调用**：不要忘记调用 `base.OnPropertyEditorChanged`，以保留默认行为。
