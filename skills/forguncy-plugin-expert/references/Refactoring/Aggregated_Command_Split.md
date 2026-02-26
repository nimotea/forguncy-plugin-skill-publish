# 拆分聚合命令重构指南 (Refactor Aggregated Commands)

## 场景描述
当一个命令类（Command）通过内部的 `Enum` 属性和 `switch-case` 逻辑来处理多种不同的操作时，我们称之为“聚合命令”。随着功能增加，这类代码会变得难以维护且 UI 逻辑复杂。

本指南说明如何系统地将聚合命令拆分为多个独立的命令类。

## 重构步骤

### 1. 分析现有结构
- **识别操作类型**: 找到控制逻辑的 `Enum`。
- **识别公共属性**: 哪些属性是所有操作都需要的（如：数据源、结果存放位置）。
- **识别特有属性**: 哪些属性仅在特定 `case` 下有效。

### 2. 提取抽象基类 (Base Class)
创建一个继承自 `Command` (或 `ICommandExecutableInServerSideAsync`) 的抽象基类。
- 将公共属性移入基类。
- **推荐**：在基类中提供统一的 `ToString` 格式化辅助方法，简化子类实现。
- 保持 `GetCommandScope()` 等通用配置一致。

```csharp
using System.Reflection;

public abstract class MyPluginBaseCommand : Command, ICommandExecutableInServerSideAsync
{
    [DisplayName("结果存入变量")]
    [ResultToProperty]
    public string ResultTo { get; set; }

    public abstract Task<ExecuteResult> ExecuteAsync(IServerCommandExecuteContext context);

    public override CommandScope GetCommandScope() => CommandScope.ExecutableInServer;

    /// <summary>
    /// 统一格式化命令在列表中的显示描述
    /// </summary>
    protected string FormatDescription(object content, string descriptionPattern = "{0}")
    {
        // 自动获取当前类的 DisplayName
        var displayName = this.GetType().GetCustomAttribute<DisplayNameAttribute>()?.DisplayName 
                          ?? this.GetType().Name;
        
        if (content == null || string.IsNullOrWhiteSpace(content.ToString()))
        {
            return displayName;
        }
        
        // 自动处理 content 的显示格式并拼接前缀
        var description = string.Format(descriptionPattern, content);
        return $"{displayName}: {description}";
    }
}
```

### 3. 迁移共享定义
- **Enum/辅助类**: 如果 `Enum` 或其他辅助类被多个子类引用，将其移动到独立的 `.cs` 文件或基类命名空间下。
- **注意**: 严禁在拆分过程中遗漏枚举定义，否则会导致编译错误。

### 4. 实现独立子类
为每个操作创建一个子类，继承自基类。
- 仅保留该操作特有的属性。
- 实现 `ExecuteAsync` 逻辑，去除 `switch-case`。
- 使用 `[DisplayName]` 区分不同命令。

### 5. 处理设计时逻辑 (Designer Logic)
- **可见性控制**: 原本在聚合命令中复杂的 `GetDesignerPropertyVisible` 逻辑通常可以大幅简化，因为每个子类只包含自己需要的属性。
- **图标与分类**: 为每个子类设置合适的 `[Icon]` 和 `[Category]`。

## Checklists
- [ ] 基类是否包含了所有公共属性？
- [ ] 每个子类的 `ExecuteAsync` 是否已移除原有的 `switch` 判断？
- [ ] 共享的 `Enum` 是否已迁移到可全局访问的位置？
- [ ] 是否更新了 `ToString()` 方法以显示正确的命令名称？
- [ ] 所有的 `[FormulaProperty]` 是否依然正确应用？

## 自动化辅助 (AI Prompt 建议)
当要求 AI 执行此重构时，可以使用如下提示词：
> "请将 [ClassName] 拆分为多个独立的命令类。
> 1. 以 [EnumName] 为依据进行拆分。
> 2. 提取公共属性 [PropertyNames] 到抽象基类。
> 3. 确保 [EnumName] 定义被迁移到独立文件或共享命名空间。
> 4. 为每个分支生成独立的子类，并保持原有的逻辑不变。"
