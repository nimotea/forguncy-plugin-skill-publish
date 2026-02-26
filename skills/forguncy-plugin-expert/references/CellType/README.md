# 单元格插件 API 参考 (CellType)

本目录存放与 `CellType` 开发相关的详细 API 文档、接口定义及使用示例。

## 开发导航 (Development Guide)

通过以下问题快速定位所需文档：

1.  **我要定义数据或配置项?** -> 查阅 **[添加属性 (Add Property)](#添加属性-add-property)**
    -   *基础类型*: [字符串](Add_Property_String.md), [整数](Add_Property_Integer.md), [布尔](Add_Property_Boolean.md)
    -   *UI 选择器*: [下拉列表](Add_Property_Dropdown.md), [颜色](Add_Property_Color.md), [图片](Add_Property_Image.md)
    -   *复杂结构*: [列表](Add_Property_List.md), [对象](Add_Property_Object.md), [树](Add_Property_Tree.md)
    -   *资源选择*: [数据库](Add_Property_DatabaseConnection.md), [角色](Add_Property_RoleSelector.md), [页面](Add_Property_PageName.md)

2.  **我要开发表单输入控件?** -> 查阅 **[表单开发 (Form Development)](#表单开发-form-development)**
    -   *核心功能*: [数据绑定](Form_Support_Value.md), [值变更命令](Form_Support_ValueChange.md)
    -   *状态控制*: [只读](Form_Support_ReadOnly.md), [禁用](Form_Support_Disable.md), [权限](Form_Support_Permission.md)
    -   *校验与交互*: [数据校验](Form_Support_Verification.md), [Tab顺序](Form_Support_TabOrder.md), [默认值](Form_Support_DefaultValue.md)

3.  **我要增强设计器体验?** -> 查阅 **[设计时支持 (Design-Time Support)](#设计时支持-design-time-support)**
    -   *预览*: [设计时预览](Designer_Preview.md)
    -   *面板控制*: [分组排序](Designer_Grouping_Sorting.md), [动态隐藏](Designer_Dynamic_Visibility.md), [属性联动](Designer_Property_Interaction.md)

4.  **我要与活字格功能集成?** -> 查阅 **[功能集成 (Function Integration)](#功能集成-function-integration)**
    -   *外观*: [支持样式](Support_Cell_Style.md), [模板样式](Support_Template_Style.md)
    -   *运行时*: [生命周期](Integration_Lifecycle.md), [调试显示](Integration_DebugDisplay.md)
    -   *表格支持*: [集成到表格](Integration_ListView.md) (包含 [编辑](Integration_ListView_DoubleClickEdit.md) 与 [交互](Integration_ListView_Interaction.md))

5.  **我要添加运行时行为?** -> 查阅 **[单元格操作 (Cell Actions)](#单元格操作-cell-actions)**
    -   [修改属性](Action_ModifyProperty.md), [执行方法](Action_AdvancedOperations.md)

## 文档列表
- [基础结构 (Basic Structure)](Basic_Structure.md)

### 添加属性 (Add Property)
- [字符串属性 (String)](Add_Property_String.md)
- [公式属性 (Formula)](Add_Property_Formula.md)
- [整数属性 (Integer)](Add_Property_Integer.md)
- [小数属性 (Double)](Add_Property_Double.md)
- [百分比属性 (Percentage)](Add_Property_Percentage.md)
- [布尔属性 (Boolean)](Add_Property_Boolean.md)
- [枚举属性 (Enum)](Add_Property_Enum.md)
- [下拉列表属性 (Dropdown/Combo)](Add_Property_Dropdown.md)
- [单选框属性 (Radio)](Add_Property_Radio.md)
- [颜色属性 (Color)](Add_Property_Color.md)
- [字体属性 (Font)](Add_Property_Font.md)
- [图片属性 (Image)](Add_Property_Image.md)
- [命令属性 (Command)](Add_Property_Command.md)
- [数据源属性 (Data Source)](Add_Property_DataSource.md)
- [对象属性 (Object)](Add_Property_Object.md)
- [列表属性 (List)](Add_Property_List.md)
- [对象列表属性 (Object List)](Add_Property_ObjectList.md)
- [树结构属性 (Tree)](Add_Property_Tree.md)

### 其他选择器属性 (Other Selectors)
- [数据库连接选择 (DB Connection)](Add_Property_DatabaseConnection.md)
- [角色选择 (Role)](Add_Property_RoleSelector.md)
- [页面选择 (Page Name)](Add_Property_PageName.md)
- [服务端命令选择 (Server Command)](Add_Property_ServerCommandName.md)

### 样式与集成 (Style & Integration)
- [支持单元格样式 (Basic Style)](Support_Cell_Style.md)
- [支持单元格模板样式 (Template Style)](Support_Template_Style.md)
- [支持复杂单元格样式 (Complex Style)](Support_Complex_Style.md)

### 功能集成 (Function Integration)
- [单元格生命周期 (Lifecycle)](Integration_Lifecycle.md)
- [可见范围设置 (Visible Range)](Integration_VisibleRange.md)
- [图片上传支持 (Image Upload)](Integration_ImageUpload.md)
- [调试显示自定义 (Debug Display)](Integration_DebugDisplay.md)
- [集成到表格 (ListView Integration)](Integration_ListView.md)
  - [鼠标交互 (Interaction)](Integration_ListView_Interaction.md)
  - [直接点击编辑 (Click Edit)](Integration_ListView_ClickEdit.md)
  - [双击编辑 (Double Click Edit)](Integration_ListView_DoubleClickEdit.md)
  - [常见问题 (FAQ)](Integration_ListView_FAQ.md)

### 设计时支持 (Design-Time Support)
- [设计时预览 (Preview)](Designer_Preview.md)
- [动态隐藏属性 (Dynamic Visibility)](Designer_Dynamic_Visibility.md)
- [初始化属性值 (Init Properties)](Designer_Init_Properties.md)
- [分组与排序 (Grouping & Sorting)](Designer_Grouping_Sorting.md)
- [行为与校验 (Behavior & Validation)](Designer_Behavior_Validation.md)
- [属性联动与高级属性 (Property Interaction)](Designer_Property_Interaction.md)

### 表单开发 (Form Development)
- [支持单元格值 (Cell Value)](Form_Support_Value.md)
- [支持值变更命令 (Value Change Command)](Form_Support_ValueChange.md)
- [支持只读 (ReadOnly)](Form_Support_ReadOnly.md)
- [支持禁用 (Disable)](Form_Support_Disable.md)
- [支持数据校验 (Verification)](Form_Support_Verification.md)
- [支持权限 (Permission)](Form_Support_Permission.md)
- [支持 Tab 顺序 (Tab Order)](Form_Support_TabOrder.md)
- [支持未提交检查 (Dirty Check)](Form_Support_DirtyCheck.md)
- [支持默认值 (Default Value)](Form_Support_DefaultValue.md)

### 单元格操作 (Cell Actions)
- [修改属性值 (Modify Property)](Action_ModifyProperty.md)
- [高级操作 (Advanced Operations)](Action_AdvancedOperations.md)
- [操作设计时支持 (Action Design-Time)](Action_DesignTime.md)

## 待补充内容
- 接口定义
- 常用基类方法
- 前端 JS 交互 API
