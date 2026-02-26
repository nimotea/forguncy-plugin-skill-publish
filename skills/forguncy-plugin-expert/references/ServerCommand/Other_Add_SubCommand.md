# 添加子命令 (Add Sub-Command)

在服务端命令插件中，有时需要像“循环命令”或“条件命令”一样，包含并执行一系列子命令。这可以通过实现 `ISubListCommand` 和 `IContainSubCommands` 接口来实现。

## 接口说明

- **`ISubListCommand`**：标识该命令包含一个子命令列表属性。通常需要定义一个 `List<Command>` 类型的属性。
- **`IContainSubCommands`**：用于告诉设计器和运行时，该命令内部包含子命令，需要通过 `EnumSubCommands` 方法暴露出来。

## 代码示例

```csharp
using GrapeCity.Forguncy.Commands;
using System.Collections.Generic;
using System.ComponentModel;
using System.Threading.Tasks;

namespace MyPlugin
{
    public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync, ISubListCommand, IContainSubCommands
    {
        // 1. 定义存储子命令的列表属性
        // [Browsable(false)] 必不可少，防止该属性直接显示在右侧属性面板中，
        // 而是作为子节点显示在命令树中。
        [Browsable(false)]
        public List<Command> CommandList { get; set; } = new List<Command>();

        // 2. 实现 IContainSubCommands 接口，返回所有子命令列表
        // 设计器会使用此方法来查找和管理子命令
        public IEnumerable<List<Command>> EnumSubCommands()
        {
            yield return CommandList;
        }

        public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
        {
            dataContext.Log.AppendLine("开始执行子命令容器...");

            // 3. 执行子命令
            // 使用上下文提供的 ExecuteCommandsAsync 方法来按顺序执行子命令列表
            var result = await dataContext.ExecuteCommandsAsync(this.CommandList);

            dataContext.Log.AppendLine("子命令容器执行结束");
            
            // 返回子命令的执行结果（通常直接返回 result 即可，除非有特殊处理逻辑）
            return result;
        }

        public override CommandScope GetCommandScope()
        {
            return CommandScope.ExecutableInServer;
        }
    }
}
```

## 关键点

1.  **`[Browsable(false)]`**：必须给 `CommandList` 属性添加此特性。如果忽略，设计器会尝试在属性面板中渲染该列表，导致显示异常。
2.  **`ExecuteCommandsAsync`**：这是运行时执行子命令的标准方式，它会自动处理异步等待和上下文传递。
3.  **UI 表现**：实现上述接口后，在活字格设计器中，该命令下方会出现一个可展开的区域（类似于“如果”命令的“Then”块），用户可以将其他命令拖入其中。
