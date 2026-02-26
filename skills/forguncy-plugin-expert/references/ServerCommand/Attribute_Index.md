# 服务端命令 Attribute 索引 (Attribute Index)

本文档汇总了开发服务端命令插件时常用的 Attribute（特性），按功能分类，方便快速查阅。

## 属性标记 (Property Attributes)

用于控制命令属性的行为、类型及在设计器中的表现。

| Attribute                                | 说明                                                                   | 详细文档                                              |
| :--------------------------------------- | :--------------------------------------------------------------------- | :---------------------------------------------------- |
| **[FormulaProperty]**                    | 标记属性支持公式（用户可输入公式或变量）。                             | [公式属性](./Add_Property_Formula.md)                 |
| **[ResultToProperty]**                   | 标记属性为“返回值属性”，用于接收命令执行结果的变量名。                 | [支持返回结果](./Process_Return_Results.md)           |
| **[ServerCommandNameProperty]**          | 标记属性为“服务端命令选择器”，允许用户选择当前工程中的其他服务端命令。 | [服务端命令选择](./Add_Property_ServerCommandName.md) |
| **[BindingDataSourceProperty]**          | 标记属性为“数据表选择器”，允许用户选择数据库中的表。                   | [数据源属性](./Add_Property_DataSource.md)            |
| **[DatabaseConnectionSelectorProperty]** | 标记属性为“数据库连接选择器”。                                         | [数据库连接](./Add_Property_DatabaseConnection.md)    |
| **[ObjectProperty]**                     | 标记属性为复合对象类型。                                               | [对象属性](./Add_Property_Object.md)                  |
| **[ObjectListProperty]**                 | 标记属性为对象列表类型。                                               | [对象列表属性](./Add_Property_ObjectList.md)          |
| **[ListProperty]**                       | 标记属性为基础类型列表（如字符串列表）。                               | [列表属性](./Add_Property_List.md)                    |
| **[ComboProperty]**                      | 标记属性为下拉框选择（通常配合 `RecommendedValues`）。                 | [下拉列表属性](./Add_Property_Dropdown.md)            |
| **[RadioGroupProperty]**                 | 标记属性在设计器中显示为单选按钮组。                                   | [UI 控件属性](./Attribute_UI_Controls.md)             |
| **[IntProperty]**                        | 标记属性为整数类型（通常用于增强校验）。                               | [整数属性](./Add_Property_Integer.md)                 |
| **[DoubleProperty]**                     | 标记属性为小数类型。                                                   | [小数属性](./Add_Property_Double.md)                  |
| **[BoolProperty]**                       | 标记属性为布尔类型。                                                   | [布尔属性](./Add_Property_Boolean.md)                 |

## 设计时行为 (Design-Time Attributes)

用于控制属性在设计器中的可见性、默认值及序列化行为。

| Attribute                    | 说明                                                             | 详细文档                                       |
| :--------------------------- | :--------------------------------------------------------------- | :--------------------------------------------- |
| **[DisplayName]**            | 设置属性在设计器中显示的名称。                                   | 通用                                           |
| **[Description]**            | 设置属性的提示说明（悬停显示）。                                 | [添加说明](./Designer_Descriptions.md)         |
| **[DefaultValue]**           | 设置属性的默认值。                                               | [折叠高级属性](./Designer_Advanced_Folding.md) |
| **[Browsable(false)]**       | 隐藏属性，使其不在属性面板中显示（常用于子命令列表或内部状态）。 | [添加子命令](./Other_Add_SubCommand.md)        |
| **[AdvancedProperty]**       | 标记为高级属性，默认折叠。                                       | [折叠高级属性](./Designer_Advanced_Folding.md) |
| **[SearchableProperty]**     | 标记属性值可以被全局搜索功能索引。                               | [搜索控制](./Attribute_Search.md)              |
| **[JsonIgnore]**             | 属性完全不参与序列化（不保存到文件，不生成元数据）。             | [序列化控制](./Attribute_Serialization.md)     |
| **[SaveJsonIgnore]**         | 属性不保存到工程文件（但可能参与元数据生成）。                   | [序列化控制](./Attribute_Serialization.md)     |
| **[PageMetadataJsonIgnore]** | 属性不包含在页面元数据中（通常用于减小前端包体积）。             | [序列化控制](./Attribute_Serialization.md)     |

## 类标记 (Class Attributes)

用于标记命令类本身的元数据、图标及设计器关联。

| Attribute         | 说明                                 | 详细文档                                     |
| :---------------- | :----------------------------------- | :------------------------------------------- |
| **[Category]**    | 指定命令在工具箱中的分组。           | [分组与排序](./Designer_Grouping_Sorting.md) |
| **[OrderWeight]** | 指定命令在分组中的排序权重。         | [分组与排序](./Designer_Grouping_Sorting.md) |
| **[Icon]**        | 指定命令的图标（嵌入资源路径）。     | [图标设置](./Attribute_UI_Controls.md)       |
| **[Designer]**    | 指定关联的自定义设计器类（全类名）。 | [自定义编辑器](./Designer_Custom_Editor.md)  |
| **[SearchTags]**  | 为命令指定额外的搜索关键字。         | [搜索控制](./Attribute_Search.md)            |

## 校验标记 (Validation Attributes)

用于属性值的有效性检查。

| Attribute      | 说明                 | 详细文档                             |
| :------------- | :------------------- | :----------------------------------- |
| **[Required]** | 标记属性为必填项。   | [属性校验](./Designer_Validation.md) |
| **[Range]**    | 限制数字属性的范围。 | [属性校验](./Designer_Validation.md) |
