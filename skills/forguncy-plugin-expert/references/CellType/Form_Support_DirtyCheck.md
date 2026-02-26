# 开发表单类单元格 - 支持未提交数据检查 (Dirty Check)

## 参考资料
[支持离开页面时检查是否有未提交的数据 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/developformcell/supportcheckuncommitteddatawhenleavingpage)

## 概述
当用户修改了单元格内容但未提交时，如果尝试离开页面，会弹出警告。

## C# 实现
重写 `SupportFeatures` 属性。

```csharp
public override SupportFeatures SupportFeatures
{
    get
    {
        return SupportFeatures.ShouldCheckDirtyWhenLeavePage;
    }
}
```

## 组合使用
```csharp
public override SupportFeatures SupportFeatures
{
    get
    {
        return SupportFeatures.ShouldCheckDirtyWhenLeavePage | SupportFeatures.AllowSetTabOrder;
    }
}
```
