# 活字格 (Forguncy) 插件开发参考手册 (AI Optimized)

> 本文档经过针对 AI 检索的深度优化，去除了冗余代码和无关描述，仅保留核心定义和逻辑。

## 1. 核心指南 (Core Guides)
*   **指导原则**: [Guiding_Principles.md](Guiding_Principles.md)
*   **API 速查表**: [API_Cheatsheet.md](API_Cheatsheet.md)
*   **项目配置**: [Project_Configuration/Plugin_Metadata.md](Project_Configuration/Plugin_Metadata.md)

## 2. 服务端命令 (ServerCommand)
*   **基础属性 (Basic Properties)**: [ServerCommand/Reference_Manual/Properties_Basic.md](ServerCommand/Reference_Manual/Properties_Basic.md)
    *   包含: Bool, Int, Double, Decimal, String, Enum, Formula 等基础类型。
*   **高级属性 (Complex Properties)**: [ServerCommand/Reference_Manual/Properties_Complex.md](ServerCommand/Reference_Manual/Properties_Complex.md)
    *   包含: Object, List, DataSource, DatabaseConnection, ServerCommandName 等复杂类型。
*   **设计时支持 (Design Time)**: [ServerCommand/Reference_Manual/DesignTime_Support.md](ServerCommand/Reference_Manual/DesignTime_Support.md)
    *   包含: 属性联动、动态可见性、验证、折叠、分组。
*   **流程控制 (Process Control)**: [ServerCommand/Reference_Manual/Process_Control.md](ServerCommand/Reference_Manual/Process_Control.md)
    *   包含: 异常处理、返回值结构。
*   **其他功能 (Other Functions)**: [ServerCommand/Reference_Manual/Other_Functions.md](ServerCommand/Reference_Manual/Other_Functions.md)
    *   包含: 日志记录、数据库操作、网络请求、缓存服务、子命令调用。
*   **入门教程**: [ServerCommand/Reference_Manual/Tutorial_SimpleServerCommand.md](ServerCommand/Reference_Manual/Tutorial_SimpleServerCommand.md)

## 3. 单元格插件 (CellType)
*   **基础属性**: [CellType/Reference_Manual/Properties_Basic.md](CellType/Reference_Manual/Properties_Basic.md)
*   **高级属性**: [CellType/Reference_Manual/Properties_Complex.md](CellType/Reference_Manual/Properties_Complex.md)
*   **设计时支持**: [CellType/Reference_Manual/DesignTime_Support.md](CellType/Reference_Manual/DesignTime_Support.md)
*   **运行时行为**: [CellType/Reference_Manual/Runtime_Behavior.md](CellType/Reference_Manual/Runtime_Behavior.md)
    *   包含: 表单值处理、只读/禁用状态、脏数据检查、权限控制。
*   **系统集成**: [CellType/Reference_Manual/System_Integration.md](CellType/Reference_Manual/System_Integration.md)
    *   包含: 生命周期、列表视图集成、样式支持、文件上传。
*   **示例与最佳实践**: [CellType/Reference_Manual/Examples_And_Best_Practices.md](CellType/Reference_Manual/Examples_And_Best_Practices.md)
*   **入门教程**: [CellType/Reference_Manual/Tutorial_SimpleCellType.md](CellType/Reference_Manual/Tutorial_SimpleCellType.md)

## 4. 客户端命令 (ClientCommand)
*   **基础属性**: [ClientCommand/Properties_Basic.md](ClientCommand/Properties_Basic.md)
*   **高级属性**: [ClientCommand/Properties_Complex.md](ClientCommand/Properties_Complex.md)
*   **设计时支持**: [ClientCommand/DesignTime_Support.md](ClientCommand/DesignTime_Support.md)
*   **其他功能**: [ClientCommand/Other_Functions.md](ClientCommand/Other_Functions.md)
*   **入门教程**: [ClientCommand/Tutorial_SimpleClientCommand.md](ClientCommand/Tutorial_SimpleClientCommand.md)

## 5. Java 适配器 (JavaAdapter)
*   **属性定义**: [JavaAdapter/Properties.md](JavaAdapter/Properties.md)
*   **设计时支持**: [JavaAdapter/DesignTime_Support.md](JavaAdapter/DesignTime_Support.md)
*   **流程控制**: [JavaAdapter/Process_Control.md](JavaAdapter/Process_Control.md)
*   **安全提供者**: [JavaAdapter/Security_Provider.md](JavaAdapter/Security_Provider.md)
*   **其他功能**: [JavaAdapter/Other_Functions.md](JavaAdapter/Other_Functions.md)

## 6. 其他模块
*   **服务端 API**: [ServerApi/ServerSideApiDevelopment.md](ServerApi/ServerSideApiDevelopment.md)
*   **中间件**: [Middleware/](Middleware/)
*   **FAQ**: [FAQ/](FAQ/)
*   **发布指南**: [Publish/](Publish/)
*   **调试指南**: [Debug/](Debug/)
*   **升级指南**: [Upgrade/](Upgrade/)
