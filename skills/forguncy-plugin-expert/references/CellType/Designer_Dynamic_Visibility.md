# 单元格设计时支持 - 动态隐藏属性 (Dynamic Visibility)

## 参考资料
[动态隐藏属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/celldesignsupport/dynamichiddenproperties)

## 概述
根据一个属性的值，动态控制另一个属性在设计器属性面板中的显示或隐藏。

## 实现方法
在插件类中重写 `GetDesignerPropertyVisible` 方法。

```csharp
public class MyPluginCellType : CellType
{
    public bool EnableAdvancedMode { get; set; }
    public string AdvancedSetting { get; set; }

    public override bool GetDesignerPropertyVisible(string propertyName)
    {
        // 如果当前检查的属性是 "AdvancedSetting"
        if (propertyName == nameof(AdvancedSetting))
        {
            // 仅当 EnableAdvancedMode 为 true 时显示
            return EnableAdvancedMode;
        }
        
        return base.GetDesignerPropertyVisible(propertyName);
    }
}
```
