# 服务端命令插件 API 参考 (ServerCommand)

本目录存放与 `ServerCommand` 开发相关的详细 API 文档、接口定义及使用示例。

## 开发导航 (Development Guide)

通过以下问题快速定位所需文档：

1.  **我要定义命令参数?** -> 查阅 **[属性开发](#属性开发)**
    -   *基础类型*: [字符串](./Add_Property_String.md), [整数](./Add_Property_Integer.md), [布尔](./Add_Property_Boolean.md)
    -   *复杂结构*: [对象](./Add_Property_Object.md), [列表](./Add_Property_ObjectList.md)
    -   *资源选择*: [数据库](./Add_Property_DatabaseConnection.md), [服务端命令](./Add_Property_ServerCommandName.md)

2.  **我要实现命令逻辑?** -> 查阅 **[流程控制](#流程控制-process-control)** & **[其他功能](#其他功能-other-functions)**
    -   *执行结果*: [返回值](./Process_Execute_Result.md), [支持返回结果](./Process_Return_Results.md)
    -   *外部交互*: [数据库](./Other_Database_Interaction.md), [HTTP请求](./Other_ThirdParty_Network.md)
    -   *控制*: [异常处理](./Process_Exception_Handling.md), [子命令](./Other_Add_SubCommand.md), [日志](./Other_ServerCommand_Log.md)

3.  **我要定制设计器体验?** -> 查阅 **[设计时扩展](#设计时扩展-design-time-extensions)**
    -   *编辑器*: [自定义编辑器](./Designer_Custom_Editor.md)
    -   *属性控制*: [校验](./Designer_Validation.md), [动态隐藏](./Designer_Dynamic_Visibility.md), [联动](./Designer_Property_Linkage.md)

4.  **我要测试命令?** -> 查阅 **[测试与调试](#测试与调试-testing--debugging)**
    -   *数据生成*: [Mock 数据工具](./Testing_MockData.md)

## 目录

### 快速查阅 (Quick Reference)
- [服务端命令 Attribute 索引 (Attribute Index)](./Attribute_Index.md)

### 基础
- [服务端命令基本结构 (Basic Structure)](./Basic_Structure.md)

### 属性开发
- [添加属性 - 字符串属性 (String Property)](./Add_Property_String.md)
- [添加属性 - 公式属性 (Formula Property)](./Add_Property_Formula.md)
- [添加属性 - 整数属性 (Integer Property)](./Add_Property_Integer.md)
- [添加属性 - 小数属性 (Double Property)](./Add_Property_Double.md)
- [添加属性 - 百分比属性 (Percentage Property)](./Add_Property_Percentage.md)
- [添加属性 - 布尔属性 (Boolean Property)](./Add_Property_Boolean.md)
- [添加属性 - 枚举属性 (Enum Property)](./Add_Property_Enum.md)
- [添加属性 - 下拉列表属性 (Dropdown/Combo Property)](./Add_Property_Dropdown.md)
- [添加属性 - 单选/列表/图标 (UI Controls & Icons)](./Attribute_UI_Controls.md)
- [添加属性 - 对象属性 (Object Property)](./Add_Property_Object.md)
- [添加属性 - 对象列表属性 (Object List Property)](./Add_Property_ObjectList.md)
- [添加属性 - 服务端命令选择属性 (ServerCommand Selection)](./Add_Property_ServerCommandName.md)
- [添加属性 - 数据源属性 (Data Source Property)](./Add_Property_DataSource.md)
- [添加属性 - 数据库连接选择属性 (Database Connection)](./Add_Property_DatabaseConnection.md)

### 设计时扩展 (Design-Time Extensions)
- [自定义命令编辑器 (Custom Command Editor)](./Designer_Custom_Editor.md)
- [属性校验与高级校验 (Validation)](./Designer_Validation.md)
- [动态隐藏属性 (Dynamic Visibility)](./Designer_Dynamic_Visibility.md)
- [命令的分组与排序 (Grouping & Sorting)](./Designer_Grouping_Sorting.md)
- [给命令/属性添加说明 (Descriptions)](./Designer_Descriptions.md)
- [属性值联动 (Property Linkage)](./Designer_Property_Linkage.md)
- [折叠高级属性 (Advanced Folding)](./Designer_Advanced_Folding.md)
- [序列化控制 (Serialization Control)](./Attribute_Serialization.md)
- [搜索控制 (Search Control)](./Attribute_Search.md)

### 流程控制 (Process Control)
- [异常处理 (Exception Handling)](./Process_Exception_Handling.md)
- [支持返回结果 (Support Return Results)](./Process_Return_Results.md)
- [服务端命令执行函数返回值 (Execute Function Return Value)](./Process_Execute_Result.md)

### 其他功能 (Other Functions)
- [添加子命令 (Add Sub-Command)](./Other_Add_SubCommand.md)
- [数据库交互 (Database Interaction)](./Other_Database_Interaction.md)
- [第三方网络服务交互 (Third-party Network Interaction)](./Other_ThirdParty_Network.md)
- [服务端命令日志 (Server Command Log)](./Other_ServerCommand_Log.md)

### 测试与调试 (Testing & Debugging)
- [测试数据生成 (Mock Data Generation)](./Testing_MockData.md)

## 待补充内容
- `Command` 基类
