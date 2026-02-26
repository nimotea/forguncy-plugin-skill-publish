# 添加单元格操作 - 设计时支持 (Action Design-Time Support)

## 参考资料
[高级单元格操作设计时支持 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addcellaction/addadvancedcelloperations/advanced-cell-operations-design-time-support)

## 概述
为自定义单元格操作添加参数校验、动态显示参数等设计时逻辑。

## 实现方法
使用 `[RunTimeMethodDesigner]` 特性指定设计器类。

```csharp
public class MyPluginCellType : CellType
{
    [RunTimeMethod]
    [RunTimeMethodDesigner(typeof(MyOperationDesigner))]
    public void MyOperation(bool param1, bool param2) { }
}

public class MyOperationDesigner : RunTimeMethodDesigner
{
    // 1. 自定义参数校验
    public override string Validate(IRuntimeMethodDesignerContext context)
    {
        var p1 = context.GetParameterValue("param1");
        var p2 = context.GetParameterValue("param2");
        
        if (object.Equals(p1, false) && object.Equals(p2, false))
        {
            return "参数1和参数2至少勾选一个";
        }
        return base.Validate(context);
    }

    // 2. 动态隐藏参数
    public override bool GetDesignerParameterVisible(IRuntimeMethodDesignerContext context, string parameterName)
    {
        if (parameterName == "param2")
        {
            // 仅当 param1 为 true 时显示 param2
            return object.Equals(context.GetParameterValue("param1"), true);
        }
        return base.GetDesignerParameterVisible(context, parameterName);
    }
}
```
