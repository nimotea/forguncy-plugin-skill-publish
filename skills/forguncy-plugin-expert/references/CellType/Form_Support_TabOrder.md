# 开发表单类单元格 - 支持 Tab 键顺序 (Tab Order)

## 参考资料
[支持Tab键顺序 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportstaborder)

## 概述
允许用户自定义该单元格在页面 Tab 键导航中的顺序。

## C# 实现
重写 `SupportFeatures` 属性。

```csharp
public override SupportFeatures SupportFeatures
{
    get
    {
        return SupportFeatures.AllowSetTabOrder;
    }
}
```
