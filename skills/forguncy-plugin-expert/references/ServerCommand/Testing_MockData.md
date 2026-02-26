# 服务端命令测试数据生成 (Test Data Generation)

在开发服务端命令插件时，为了验证业务逻辑（如 L1.5 排程算法、复杂计算等），往往需要大量的测试数据。手动构造 JSON 数据既耗时又容易出错。为此，我们提供了一个通用的 **Mock 数据生成工具**。

## 工具介绍

`scripts/generate_mock_data.py` 是一个轻量级的 Python 脚本，能够根据用户定义的 Schema 配置文件，批量生成符合结构的 JSON 数据文件。

### 核心功能
*   **多文件生成**：一次配置可生成多个关联文件（如 `WorkOrders.json` 和 `Resources.json`）。
*   **灵活类型支持**：支持 UUID、自增字符串、随机整数范围、日期偏移、枚举值等。
*   **零依赖**：仅使用 Python 标准库，无需安装额外 pip 包。

## 使用指南

### 1. 准备配置文件
创建一个 JSON 配置文件（例如 `my_test_config.json`），定义你需要的数据结构。

```json
{
    "outputs": [
        {
            "filename": "MyData.json",
            "count": 50,
            "schema": {
                "Id": "uuid",
                "Name": "string:User-{index}",
                "Age": "int:18,60",
                "Role": "enum:Admin,User,Guest",
                "JoinDate": "date:past_365d"
            }
        }
    ]
}
```

### 2. 运行脚本
在项目根目录下运行以下命令：

```bash
python scripts/generate_mock_data.py --config ./my_test_config.json --output ./test_data
```

### 3. 使用数据
生成的 JSON 文件可以直接用于：
*   **单元测试**：作为测试用例的输入。
*   **活字格调试**：复制 JSON 内容粘贴到服务端命令的“参数”中进行本地调试。

## 支持的类型语法

| 类型           | 语法示例                | 说明                                             |
| :------------- | :---------------------- | :----------------------------------------------- |
| **UUID**       | `"uuid"`                | 生成随机 GUID                                    |
| **字符串模板** | `"string:Item-{index}"` | 生成带序号的字符串，`{index}` 会被替换为 1, 2... |
| **整数范围**   | `"int:1,100"`           | 生成 1 到 100 之间的随机整数                     |
| **日期**       | `"date:today"`          | 生成当天日期 (YYYY-MM-DD)                        |
| **未来日期**   | `"date:future_30d"`     | 生成未来 30 天内的随机日期                       |
| **过去日期**   | `"date:past_30d"`       | 生成过去 30 天内的随机日期                       |
| **枚举**       | `"enum:A,B,C"`          | 从提供的选项中随机选择一个                       |
| **布尔**       | `"bool"`                | 随机生成 `true` 或 `false`                       |

## 典型场景示例：L1.5 排程数据

针对常见的 L1.5 业务场景（工单与资源），我们提供了标准配置模板。
你可以直接使用 `assets/schemas/l1_5_mock_config.json` 生成测试数据。

**配置文件示例 (`l1_5_mock_config.json`)**:
```json
{
    "outputs": [
        {
            "filename": "WorkOrders.json",
            "count": 10,
            "schema": {
                "Id": "uuid",
                "OrderNo": "string:WO-{index}",
                "ProductName": "enum:Product A,Product B",
                "Quantity": "int:10,500",
                "DueDate": "date:future_30d",
                "Priority": "enum:High,Medium,Low"
            }
        },
        {
            "filename": "Resources.json",
            "count": 5,
            "schema": {
                "Id": "uuid",
                "Name": "string:Machine #{index}",
                "Type": "enum:CNC,Lathe",
                "Capacity": "int:8,24"
            }
        }
    ]
}
```

**运行命令**:
```bash
python scripts/generate_mock_data.py --config assets/schemas/l1_5_mock_config.json --output ./l1_5_data
```
