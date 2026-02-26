---
type: reference
module: FAQ
concepts: [Serialization, DefaultValue, JsonIgnore, SaveJsonIgnore, PageMetadataJsonIgnore, ShouldSerialize]
version: 8.0+
---

# 如何控制属性的序列化

通过以下方法可以控制插件特定属性的序列化行为。活字格中单元格属性涉及两个保存逻辑：

1.  **设计时保存**：在设计器中，保存为 `.fgcc` 项目文件。
2.  **运行时发布**：发布时，属性值被序列化为元数据（Metadata），供浏览器中的 JavaScript 调用。

精细控制序列化过程可达成以下目的：
*   减少冗余数据存储，提升保存速度及降低磁盘占用。
*   避免敏感数据暴露给浏览器端 JavaScript。

> **注意**：除非有明确需求（如性能优化或安全隐患），否则不建议过度干预序列化逻辑，以避免引入不必要的复杂度和 Bug。

## 控制方法详解

### 1. DefaultValueAttribute
如果属性值与 `DefaultValue` 标注的值一致，该属性**不会**被保存到项目文件中，同时也**无法**在 JavaScript 代码中获取该属性的值（值为 `undefined`）。

```csharp
using GrapeCity.Forguncy.CellTypes;
using System.ComponentModel;

namespace MyPlugin
{
    public class MyPluginCellType : CellType
    {
        [DefaultValue(10)]
        public int MyProperty { get; set; } = 10;
    }
}
```

### 2. JsonIgnoreAttribute
标注了 `[JsonIgnore]` 的属性，**既不会**被保存到项目文件，**也无法**通过 JavaScript 获取。通常用于仅在服务端运行时使用的临时属性。

```csharp
using GrapeCity.Forguncy.CellTypes;
using Newtonsoft.Json;

namespace MyPlugin
{
    public class MyPluginCellType : CellType
    {
        [JsonIgnore]
        public int MyProperty { get; set; } = 10;
    }
}
```

### 3. SaveJsonIgnoreAttribute
标注了 `[SaveJsonIgnore]` 的属性，**不会**被保存到项目文件（.fgcc），但**可以**通过 JavaScript 代码获取。
*   **适用场景**：属性值可以通过其他属性计算得出，或者是运行时动态生成的，不需要持久化存储，但前端需要使用。

```csharp
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Plugin;

namespace MyPlugin
{
    public class MyPluginCellType : CellType
    {
        [SaveJsonIgnore]
        public int MyProperty { get; set; } = 10;
    }
}
```

### 4. PageMetadataJsonIgnoreAttribute
标注了 `[PageMetadataJsonIgnore]` 的属性，**会**被保存到项目文件，但**无法**通过 JavaScript 代码获取。
*   **适用场景**：敏感数据（如数据库连接字符串、密钥），仅在服务端使用，不希望暴露给前端。

```csharp
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Plugin;

namespace MyPlugin
{
    public class MyPluginCellType : CellType
    {
        [PageMetadataJsonIgnore]
        public int MyProperty { get; set; } = 10;
    }
}
```

### 5. ShouldSerialize{PropertyName} 方法
通过定义 `ShouldSerialize` + `属性名` 方法，可以动态控制属性是否序列化（包括保存和前端获取）。
*   返回 `true`：属性被序列化。
*   返回 `false`：属性被忽略。

> **示例**：当 `MyProperty` 值为 10 或 20 时，不进行序列化。

```csharp
using GrapeCity.Forguncy.CellTypes;

namespace MyPlugin
{
    public class MyPluginCellType : CellType
    {
        public int MyProperty { get; set; } = 10;

        public bool ShouldSerializeMyProperty()
        {
            // 逻辑：当值不为 10 且不为 20 时，才进行序列化（返回 true）。
            // 反之，如果值为 10 或 20，返回 false（不序列化）。
            return MyProperty != 10 && MyProperty != 20;
        }
    }
}
```
