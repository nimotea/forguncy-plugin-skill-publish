# 自定义命令编辑器 (Custom Command Editor)

活字格提供了三种级别的自定义编辑能力，用于满足不同复杂度的 UI 交互需求：
1.  **自定义属性编辑控件**：将某个属性的编辑器替换为自定义的 WPF 控件（嵌入在属性面板中）。
2.  **自定义属性编辑窗体**：为某个属性提供一个弹出的 WPF 窗体进行编辑（通常表现为属性旁边的一个“...”按钮）。
3.  **自定义命令编辑控件**：完全接管整个命令的编辑界面，替代默认生成的属性列表。

---

## 1. 自定义属性编辑控件 (Inline Property Editor)
适用于：仅需对单个属性进行简单的自定义编辑，且界面可以嵌入在属性面板中。

### 核心步骤
1.  **创建 UserControl**：编写 WPF 控件。
2.  **实现数据绑定**：通过 `IEditorSettingsDataContext` 读写属性值。
3.  **关联 Designer**：在 `CommandDesigner` 中重写 `GetEditorSetting`，返回自定义的 `EditorSetting`。

### 代码示例

**UserControl (XAML):**
```xml
<UserControl x:Class="MyPlugin.Designer.MyPropertyEditor" ...>
    <Grid>
        <TextBox Text="{Binding Value}" />
    </Grid>
</UserControl>
```

**UserControl (Code-Behind):**
```csharp
public partial class MyPropertyEditor : UserControl
{
    public MyPropertyEditor()
    {
        InitializeComponent();
        this.DataContextChanged += (s, e) =>
        {
            if (this.DataContext is IEditorSettingsDataContext context)
            {
                // 读取初始值
                // 监听 ViewModel 变化并写回 context.Value
            }
        };
    }
}
```

**CommandDesigner:**
```csharp
public class MyDesigner : CommandDesigner<MyCommand>
{
    public override EditorSetting GetEditorSetting(PropertyDescriptor property, IBuilderCommandContext builderContext)
    {
        if (property.Name == nameof(MyCommand.MyProperty))
        {
            // 返回自定义控件的配置
            return new MyEditorSetting();
        }
        return base.GetEditorSetting(property, builderContext);
    }
}

class MyEditorSetting : EditorSetting
{
    public override DataTemplate GetDataTemplate()
    {
        // 创建并返回包含 MyPropertyEditor 的 DataTemplate
        return ...;
    }
}
```

---

## 2. 自定义属性编辑窗体 (Dialog Property Editor)
适用于：属性编辑逻辑较复杂，需要独立弹窗（例如代码编辑器、复杂对象配置）。

### 核心步骤
1.  **创建 Window**：编写 WPF 窗体。
2.  **关联 Designer**：在 `GetEditorSetting` 中返回 `HyperlinkEditorSetting`，并绑定一个打开窗体的 `ICommand`。

### 代码示例

**CommandDesigner:**
```csharp
public class MyDesigner : CommandDesigner<MyCommand>
{
    public override EditorSetting GetEditorSetting(PropertyDescriptor property, IBuilderCommandContext builderContext)
    {
        if (property.Name == nameof(MyCommand.MyProperty))
        {
            // 使用超链接编辑器，点击触发 ShowDialogCommand
            return new HyperlinkEditorSetting(new ShowDialogCommand());
        }
        return base.GetEditorSetting(property, builderContext);
    }
}

class ShowDialogCommand : ICommand
{
    public void Execute(object parameter)
    {
        // parameter 通常是 IEditorSettingsDataContext
        var context = parameter as IEditorSettingsDataContext;
        
        // 实例化并显示窗体
        var dialog = new MyEditorWindow();
        dialog.ViewModel.Text = context.Value?.ToString();
        
        if (dialog.ShowDialog() == true)
        {
            context.Value = dialog.ViewModel.Text;
        }
    }
    // ...
}
```

---

## 3. 自定义命令编辑控件 (Full Command Editor)
适用于：需要完全重写命令编辑界面，例如复杂的向导式配置、多步骤配置。

### 核心步骤
1.  **创建 UserControl**：实现 `ICommandEditor` 接口。
2.  **实现接口**：
    *   `Command` 属性 (Get/Set)：负责 UI 与 Command 对象之间的数据转换。
    *   `Validate()` 方法：负责自定义校验逻辑。
3.  **关联 Designer**：在 `CommandDesigner` 中重写 `GetCommandEditor`。

### 代码示例

**UserControl:**
```csharp
public partial class MyFullEditor : UserControl, ICommandEditor
{
    public Command Command
    {
        get
        {
            // 从 UI 生成 Command 对象
            return new MyCommand { Prop1 = txt1.Text, Prop2 = txt2.Text };
        }
        set
        {
            // 将 Command 对象填充到 UI
            var cmd = value as MyCommand;
            txt1.Text = cmd.Prop1;
            txt2.Text = cmd.Prop2;
        }
    }

    public bool Validate()
    {
        if (string.IsNullOrEmpty(txt1.Text)) return false;
        return true;
    }
}
```

**CommandDesigner:**
```csharp
public class MyDesigner : CommandDesigner<MyCommand>
{
    // 重写此方法以接管整个编辑界面
    public override ICommandEditor GetCommandEditor()
    {
        return new MyFullEditor();
    }
}
```
