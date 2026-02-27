# 活字格插件构建标准 (Build Standardization)

## 1. 核心原则 (Core Principles)
为确保下游 AI Agent 操作的一致性和构建产物的可预测性，所有 .NET 插件项目必须遵循以下构建标准：

- **单一命令**：仅使用 `dotnet build`。
- **零参数**：严禁在构建命令中附加任何参数（如 `-c`, `-o`, `-r` 等）。
- **默认配置**：默认使用 Debug 配置构建，无需手动切换至 Release。

## 2. 标准构建流程 (Standard Build Process)

### 2.1 执行构建
在项目根目录（包含 `.csproj` 的目录）执行：
```bash
dotnet build
```

### 2.2 输出验证
构建完成后，产物通常位于 `bin/Debug/<TargetFramework>/` 目录。
- **TargetFramework**：取决于 `.csproj` 中的配置（常见为 `net6.0`, `net8.0`, `netstandard2.0` 等）。
- **默认路径**：`bin/Debug/net6.0/` (对于大多数现代活字格插件)。

**注意**：Agent 必须根据项目实际的 TargetFramework 动态推断并检查上述目录是否存在，以验证构建是否成功。

## 3. 禁止行为 (Forbidden Actions)
1.  **禁止**使用 `dotnet publish`、`dotnet pack` 或 `msbuild`。
2.  **禁止**在 `dotnet build` 后添加 `-c Release`。
3.  **禁止**编写复杂的 PowerShell/Shell 脚本来封装构建命令。
4.  **禁止**依赖 IDE 特定的构建文件（如 `.sln`）进行非标准构建。

## 4. 故障排查 (Troubleshooting)
若 `dotnet build` 失败：
1.  **引用丢失**：运行 `scripts/update_references.ps1` 修复 DLL 引用。
2.  **环境问题**：检查 .NET SDK 版本 (`dotnet --version`)。
3.  **代码错误**：根据编译器报错修复代码，**严禁**尝试通过添加构建参数（如忽略警告）来绕过错误。
