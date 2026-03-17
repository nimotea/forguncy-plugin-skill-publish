---
name: forguncy-plugin-expert
description: 活字格插件开发专家 - 为活字格低代码平台创建服务器命令(ServerCommand)、单元格类型(CellType)、客户端命令(ClientCommand)、服务器API和中间件。当用户提到"做个插件"、"创建自定义命令"、"开发单元格类型"、"Forguncy扩展"、"活字格自定义功能"，或请求"帮我写个服务器命令"、"实现一个控件"时，必须使用此技能。即使用户没有明确说"插件专家"，只要涉及活字格功能开发，都应该触发此技能。
---

# 活字格 (Forguncy) 插件开发专家

## 核心职责

帮助开发者创建高质量、生产就绪的活字格插件。熟悉 .NET、活字格 SDK 和最佳实践。

## 何时使用

以下场景必须触发此技能：

- 用户说"做个插件"、"创建自定义命令"、"开发单元格类型"
- 用户提到 Forguncy/活字格 + 开发/扩展/自定义功能
- 用户请求实现 ServerCommand、CellType、ClientCommand、ServerAPI、Middleware
- 用户询问活字格插件开发的 API 或最佳实践

## 核心文档（必读）

- [DOC\_INDEX.md](references/DOC_INDEX.md) - 开发任务入口，先读它
- [CLI\_Reference.md](references/CLI_Reference.md) - CLI 项目创建指南
- [SDK\_BestPractices.md](references/SDK_BestPractices.md) - 编码规范
- [API\_Cheatsheet.md](references/API_Cheatsheet.md) - API 速查

## 关键规则

### 为什么这些规则重要

| 规则                                | 原因                      | 违规风险      |
| --------------------------------- | ----------------------- | --------- |
| 使用 `scripts/` 脚本                  | 统一环境配置，避免路径问题           | 构建失败      |
| Windows 用 PowerShell              | Bash 在 Windows 下路径处理不一致 | 命令执行失败    |
| 用 `this.Context.DataAccess`       | 活字格已封装连接池和事务            | 资源泄漏、性能问题 |
| 参数化查询                             | 防止 SQL 注入               | 安全漏洞      |
| 用 `Logger` 而非 `Console.WriteLine` | 日志统一管理，便于排查             | 生产环境无法调试  |
| 更新 `PluginConfig.json`            | 设计与运行时必须一致              | 功能不可用     |
| 路径问题问用户                           | 避免猜测导致更多问题              | 浪费时间      |

### 核心要点速记

- **数据访问**：`this.Context.DataAccess`
- **日志**：`Logger.Info()` / `Logger.Error()`（静态类）
- **构建命令**：`dotnet build`（在项目根目录）
- **构建器**：必须用 `forguncy-plugin-create` CLI（参数化模式）

## 插件类型选择

| 类型                | 适用场景                | 前端需求       |
| ----------------- | ------------------- | ---------- |
| **ServerCommand** | 后端逻辑、数据库操作、文件处理     | 否          |
| **CellType**      | 自定义 UI 控件、图表、复杂交互组件 | Vue + TS   |
| **ClientCommand** | 纯前端逻辑、页面跳转、浏览器 API  | JavaScript |
| **ServerAPI**     | 外部系统 HTTP 接口        | 否          |
| **Middleware**    | 请求拦截、全局异常处理、认证      | 否          |

## 工作流程

### Step 1: 知识检索

先读 [DOC\_INDEX.md](references/DOC_INDEX.md)，找到对应插件类型的文档，再开始编写代码。

### Step 2: 项目初始化

使用 `forguncy-plugin-create` CLI 创建项目（**严禁 GUI 模式**）：

```bash
forguncy-plugin-create --name <PluginName> --types <types> --framework vue --lang ts --forguncy-path "<Path>" --plugin-path "<OutputPath>"
```

详细流程见 [CLI\_Reference.md](references/CLI_Reference.md)，包括：

- 环境预检（.NET SDK、CLI、活字格路径、Node.js）
- 参数组装（插件名称、类型、框架、语言）
- 退出码处理（0=成功，1=失败）

### Step 3: 需求分析与计划

正式编码前，先写计划文档：

- 位置：`plans/序号_需求简述.md`
- 内容：需求分析、模板选择、参考文档、代码变更点
- **必须等用户确认后再开始编码**

### Step 4: 编码实现

遵循 [SDK\_BestPractices.md](references/SDK_BestPractices.md)：

- `Execute` 方法返回 `ExecutionResult`
- 属性带 `[DisplayName]`（中文）
- 关键逻辑用 `try-catch` 包裹
- 用 `Logger` 记录关键步骤

### Step 5: 构建验证

```bash
dotnet build
```

MSBuild 会自动处理前端依赖（`npm install` + `npm run build`），**不要手动执行**。

### Step 6: 环境修复

遇到构建失败、程序集引用丢失：

1. 停止任务
2. 询问用户活字格安装路径（**不要猜测**）
3. 获得路径后执行 `scripts/update_references.ps1`

## 常见场景示例

**场景 1：创建新插件**

> 用户："帮我做个二维码生成的插件"
>
> 响应：检查环境 → 组装 CLI 参数 → 执行创建 → 确认成功 → 开始编写业务代码

**场景 2：实现服务器命令**

> 用户："写一个服务器命令，查询订单表"
>
> 响应：检索 DOC\_INDEX → 读取 ServerCommand 文档 → 生成计划 → 确认后编码

**场景 3：构建失败**

> 用户："dotnet build 报错了"
>
> 响应：停止任务 → 询问活字格路径 → 更新引用 → 重新构建

## 快速命令参考

```bash
# 创建项目（CLI 模式）
forguncy-plugin-create --name MyPlugin --types celltype,command,servercommand --framework vue --lang ts

# 构建
dotnet build

# 更新活字格引用
powershell -File scripts/update_references.ps1 -ForguncyPath "C:\Program Files\Forguncy 12"
```

