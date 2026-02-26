# 和活字格原生功能集成 - 支持单元格模板样式 (Support Template Style)

## 参考资料
[支持单元格模板样式 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/supportcell-type-style-root/supportcelltemplatestyle)

## 概述
为插件提供预置的样式模板（如“主要”、“成功”、“错误”样式），方便用户快速应用。

## 实现步骤
1. C# 类实现 `IStyleTemplateSupport` 接口。
2. 添加 `[MyPluginStyleTemplateSupport]` 特性（自定义特性）。
3. 实现自定义特性类，继承自 `CellTypeStyleTemplateSupportAttribute`。

## 代码示例

### MyPluginCellType.cs
```csharp
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Plugin;

namespace MyPlugin
{
    [MyPluginStyleTemplateSupport] // 应用自定义模板特性
    public class MyPluginCellType : CellType, IStyleTemplateSupport
    {
        // 必须实现的接口属性
        public string TemplateKey { get; set; }
    }

    // 定义模板支持特性
    public class MyPluginStyleTemplateSupportAttribute : CellTypeStyleTemplateSupportAttribute
    {
        // 1. 定义模板包含的部分（例如只有“主体”）
        public override List<TemplatePart> TemplateParts => new List<TemplatePart>() {
            new TemplatePart() {
                Name= "主体",
                SupportStates = CellStates.Normal | CellStates.Hover | CellStates.Active,
                SupportStyles = SupportStyles.BackgroundColor | SupportStyles.ForegroundColor | SupportStyles.RoundedCorner | SupportStyles.Border
            }
        };

        // 2. 定义预置模板列表
        public override List<CellTypeStyleTemplate> PresetTemplates => new List<CellTypeStyleTemplate>()
        {
            new CellTypeStyleTemplate()
            {
                Key = "主要",
                Category = "预置样式",
                Styles = new Dictionary<string, TemplatePartStyle>()
                {
                    {
                        "主体", new TemplatePartStyle()
                        {
                            NormalStyle = new PartStyleUnit()
                            {
                                Background = "Accent 1",
                                FontColor = "Background 1",
                                BorderRadiusString = "4px 4px 4px 4px"
                            },
                            HoverStyle = new PartStyleUnit() { Background = "Accent 1 20" },
                            ActiveStyle = new PartStyleUnit() { Background = "Accent 1 -20" },
                        }
                    }
                }
            },
            // 可以添加更多模板...
        };
    }
}
```
