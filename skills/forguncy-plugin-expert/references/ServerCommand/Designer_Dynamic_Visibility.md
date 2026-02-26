# 动态隐藏属性 (Dynamic Visibility)

在插件开发中，经常会遇到某些属性依赖于其他属性的情况。例如，只有当“开启缓存”被选中时，“缓存时间”属性才显示。
通过重写 Command 类的 `GetDesignerPropertyVisible` 方法，可以实现这种动态控制。

## 1. 基础用法
`GetDesignerPropertyVisible` 方法会在设计器渲染属性面板时被频繁调用。该方法接收当前正在判断可见性的属性名，返回 `true`（显示）或 `false`（隐藏）。

### 代码示例
```csharp
public class MyPluginServerCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("启用缓存")]
    public bool EnableCache { get; set; }

    [DisplayName("缓存时间(秒)")]
    public int CacheTime { get; set; }

    // 重写此方法控制属性可见性
    public override bool GetDesignerPropertyVisible(string propertyName, CommandScope commandScope)
    {
        // 判断是否是需要动态控制的属性
        if (propertyName == nameof(CacheTime))
        {
            // 只有当 EnableCache 为 true 时，CacheTime 才显示
            return EnableCache;
        }
        
        // 其他属性使用默认行为
        return base.GetDesignerPropertyVisible(propertyName, commandScope);
    }

    public async Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext dataContext)
    {
        return new ExecuteResult();
    }
}
```

## 2. 复杂逻辑
可以基于多个属性的状态来决定某个属性是否显示。

```csharp
public override bool GetDesignerPropertyVisible(string propertyName, CommandScope commandScope)
{
    if (propertyName == nameof(AdvancedSetting))
    {
        // 只有在 "高级模式" 开启且 "调试模式" 关闭时才显示
        return IsAdvancedMode && !IsDebugMode;
    }
    return base.GetDesignerPropertyVisible(propertyName, commandScope);
}
```

## 3. 注意事项
- **触发机制**：只要任何一个属性的值发生变化，设计器都会重新计算所有属性的可见性。因此，该方法内的逻辑应尽量保持轻量，避免耗时操作。
- **默认行为**：务必在方法的最后调用 `base.GetDesignerPropertyVisible`，以确保未显式处理的属性能够正常显示。
