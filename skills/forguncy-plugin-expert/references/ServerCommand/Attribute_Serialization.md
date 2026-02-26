# 序列化控制 (Serialization Control)

在插件开发中，有时需要精细控制属性的序列化行为，例如：某些属性仅用于运行时状态不需要保存，或者某些敏感数据不需要导出到元数据中。活字格提供了一组 Attribute 来实现这些控制。

## 常用 Attribute

### 1. [JsonIgnore]

- **作用**：完全忽略该属性。
- **行为**：
    - **不保存**：属性值不会被保存到工程文件（.fgcp）中。
    - **不生成元数据**：属性值不会包含在生成的前端/后端元数据中。
- **场景**：用于存储运行时的临时状态、缓存数据或计算属性。

```csharp
[JsonIgnore]
public string RuntimeCache { get; set; }
```

### 2. [SaveJsonIgnore]

- **作用**：仅在保存工程时不序列化。
- **行为**：
    - **不保存**：属性值不会被保存到工程文件中。
    - **生成元数据**：但是，如果该属性在生成阶段有值，它**会**被包含在元数据中。
- **场景**：用于那些可以通过其他属性推导出来，不需要持久化存储，但在运行时或编译时需要的属性。

```csharp
[SaveJsonIgnore]
public string ComputedHash { get; set; }
```

### 3. [PageMetadataJsonIgnore]

- **作用**：在生成页面元数据时忽略。
- **行为**：
    - **保存**：属性值会正常保存到工程文件。
    - **不生成元数据**：属性值不会发送给前端（浏览器）。
- **场景**：
    - 仅在服务端使用的敏感配置（如数据库密码、API 密钥）。
    - 减少前端数据包体积，剔除纯服务端逻辑需要的配置。

```csharp
[PageMetadataJsonIgnore]
[DisplayName("API 密钥")]
public string ApiKey { get; set; }
```

## 综合示例

```csharp
public class MySecureCommand : Command
{
    // 普通属性：保存并发送给前后端
    public string Name { get; set; }

    // 仅服务端使用：保存，但不发给前端
    [PageMetadataJsonIgnore]
    public string SecretKey { get; set; }

    // 运行时临时变量：完全不保存
    [JsonIgnore]
    public int RuntimeCounter { get; set; }
}
```
