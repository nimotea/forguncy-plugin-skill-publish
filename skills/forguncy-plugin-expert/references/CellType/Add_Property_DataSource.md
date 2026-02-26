# 添加属性 - 数据源属性 (Data Source Property)

## 参考资料
[数据源属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/datasourceproperty)

## 概述
用于绑定数据表或视图的数据。属性类型必须为 `object`。

## 基础用法 ([BindingDataSourceProperty])
```csharp
public class MyPluginCellType : CellType
{
    [DisplayName("绑定数据源")]
    [BindingDataSourceProperty]
    public object DataSource { get; set; }
}
```

## 高级用法

### 允许添加自定义列 (AllowAddCustomColumns)
```csharp
[BindingDataSourceProperty(AllowAddCustomColumns = true)]
public object DataSource { get; set; }
```

## JS 处理逻辑
使用 `getBindingDataSourceValue` 获取数据，并处理数据刷新。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.content = $("<div></div>");
        return this.content;
    }

    onPageLoaded() {
        const dataSource = this.CellElement.CellType.DataSource;
        
        // 获取数据 (最后一个参数 true 表示自动监听依赖变化并刷新)
        this.getBindingDataSourceValue(dataSource, null, (data) => {
            this.content.empty();
            // data 是一个对象数组，每个对象代表一行数据
            for (const row of data) {
                // row["列名"] 获取值
                this.content.append($("<div>" + JSON.stringify(row) + "</div>"));
            }
        }, true);
    }
}
```
