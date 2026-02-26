> Source: how-to-add-column-properties.md (Imported from external documentation)

# 如何添加数据表列属性

## Content

要添加数据表列属性，目前没有直接标注Attribute生成的办法可以添加，需要通过实现Designer的 GetEditorSetting 方法实现。
示例代码如下：

```
    [Designer("MyPlugin.Designer.MyPluginCommandDesigner, MyPlugin")]
    public class MyPluginCommand : Command
    {
        [DisplayName("表名")]
        public string TableName { get; set; }

        [DisplayName("列名")]
        public string ColumnName { get; set; }
    }
```

修改 Designer\\MyPluginCommandDesigner.cs 示例代码如下：

```
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
namespace MyPlugin.Designer
{
    public class MyPluginCommandDesigner : CommandDesigner<MyPluginCommand>
    {
        public override EditorSetting GetEditorSetting(PropertyDescriptor property, IBuilderCommandContext builderContext)
        {
            if (property.Name == nameof(MyPluginCommand.TableName))
            {
                return new TableComboTreeSelectorEditorSetting();
            }
            if (property.Name == nameof(MyPluginCommand.ColumnName))
            {
                return new ColumnNameEditorSetting(builderContext, GetColumns(builderContext));
            }
            return base.GetEditorSetting(property, builderContext);
        }

        public override void OnPropertyEditorChanged(string propertyName, object propertyValue, Dictionary<string, IEditorSettingsDataContext> properties)
        {
            if(propertyName == nameof(MyPluginCommand.TableName))
            {
                var columnSetting = properties[nameof(MyPluginCommand.ColumnName)];

                if(columnSetting.EditorSetting is ColumnNameEditorSetting comboSetting)
                {
                    comboSetting.Source = GetColumns(comboSetting.BuilderContext);
                }
            }
            base.OnPropertyEditorChanged(propertyName, propertyValue, properties);
        }

        private List<string> GetColumns(IBuilderCommandContext builderContext)
        {
            var tableInfo = builderContext.EnumAllTableInfos().FirstOrDefault(i => i.TableName == this.Command.TableName);
            if(tableInfo != null)
            {
                return tableInfo.Columns.Select(i => i.ColumnName).ToList();
            }
            return new List<string>();
        }
    }

    class ColumnNameEditorSetting: ComboEditorSetting
    {
        public IBuilderCommandContext BuilderContext { get; set; }
        public ColumnNameEditorSetting(IBuilderCommandContext builderContext, List<string> columns)
            : base(columns)
        {
            BuilderContext = builderContext;
        }
    }
}
```

代码说明：

1. 重写 GetEditorSetting 方法
    1. 判断属性名为 TableName 时，返回 TableComboTreeSelectorEditorSetting。
    2. 判断属性名为 ColumName 时，返回 ColumnNameEditorSetting （自定义类型，从 ComboEditorSetting 派生，主要目的是缓存 IBuilderCommandContext）。
2. 重写 OnPropertyEditorChanged 方法
3. 在 TableName 变化时，清空 ColumnName属性的值，并根据新的TableName值重写设置下拉列表。

最终设计时效果：
![](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/8ca07557-62b8-4219-8ddd-357e505dc985/80958803/image2023-1-19_16-4-40.png)