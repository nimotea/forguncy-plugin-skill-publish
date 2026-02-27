# 统一属性指南 (Unified Properties Guide)

本指南涵盖了活字格插件（服务端命令与单元格类型）中常用的属性定义方式及高级配置。

## 1. 基础属性类型 (Basic Types)

### 1.1 字符串 (String)
- **C# 定义**：
  ```csharp
  [DisplayName("文本内容")]
  [TextProperty(Watermark = "请输入...", AcceptsReturn = true)]
  public string MyText { get; set; }
  ```
- **关键点**：`Watermark` 设置水印，`AcceptsReturn` 支持多行，`CanSelectResource` 支持多语言。

### 1.2 数字 (Integer / Double)
- **C# 定义**：
  ```csharp
  [DisplayName("数值")]
  [IntProperty(MinValue = 0, MaxValue = 100)]
  public int MyInt { get; set; }
  ```
- **关键点**：使用 `[IntProperty]` 或 `[DoubleProperty]` 限制取值范围。

### 1.3 布尔值 (Boolean)
- **C# 定义**：
  ```csharp
  [DisplayName("启用")]
  [DefaultValue(true)]
  public bool IsEnabled { get; set; } = true;
  ```
- **安全提醒**：若初始值为 `true`，必须配合 `[DefaultValue(true)]` 特性，否则 `false` 状态无法正确保存。

---

## 2. 选择类属性 (Selection)

### 2.1 枚举与下拉框 (Enum / Dropdown)
- **C# 定义**：
  ```csharp
  public enum MyOptions { A, B, C }

  [DisplayName("选项")]
  public MyOptions Option { get; set; }
  ```
- **前后端同步安全原则**：
  - JS 端严禁使用魔法数字，应定义常量对象映射：`const Options = { A: 0, B: 1 };`
  - 使用 `this.CellElement.CellType.Option` 获取值并与常量对比。

---

## 3. 高级属性 (Advanced)

### 3.1 公式支持 (Formula)
- **C# 定义**：
  ```csharp
  [DisplayName("动态值")]
  [FormulaProperty]
  public object DynamicValue { get; set; }
  ```
- **服务端处理**：`context.EvaluateFormula(DynamicValue)`。
- **前端处理**：`this.evaluateFormulaAsync(this.CellElement.CellType.DynamicValue)`。

### 3.2 列表与对象列表 (List / ObjectList)

活字格区分“基础类型列表”和“复杂对象列表”，两者必须使用不同的 Attribute。

#### A. 基础列表 (ListProperty)
适用于 `List<string>`, `List<int>` 等简单类型。

```csharp
[DisplayName("IP 白名单")]
[ListProperty] // 必须标记
public List<string> IpWhitelist { get; set; }
```

#### B. 对象列表 (ObjectListProperty)
适用于自定义类的列表（如 `List<MyItem>`）。

**强制规则**：
1.  属性必须标记 `[ObjectListProperty]`。
2.  **关键**：列表项类（Item Class）必须继承 `ObjectPropertyBase`，否则在设计器中无法正确解析子属性。

```csharp
[DisplayName("配置项列表")]
[ObjectListProperty] // 规则 1
public List<MyConfigItem> Items { get; set; }

// 规则 2: 必须继承 ObjectPropertyBase
public class MyConfigItem : ObjectPropertyBase
{
    [DisplayName("键")]
    public string Key { get; set; }

    [DisplayName("值")]
    [FormulaProperty]
    public object Value { get; set; }
}
```

- **注意**：复杂对象会自动序列化为 JSON 字符串传递给前端。

---

## 4. 动态字段映射 (Dynamic Field Mapping)

当插件需要处理结构不固定的数据（如 JSON 导入、第三方 API 对接）时，使用固定的 DTO 类（配合 `[JsonProperty]`）会极大限制灵活性。

**传统痛点**：用户必须在活字格中使用“设置变量”或 SQL 别名来重命名字段，以匹配插件写死的属性名。

**推荐方案**：使用 `List<MappingItem>` 配合 `JObject` 实现动态映射。

### 4.1 定义映射类
```csharp
public class ColumnMapping
{
    [DisplayName("源字段 (API/JSON)")]
    [Description("数据源中的字段名，例如: user_name")]
    public string SourceField { get; set; }

    [DisplayName("目标列 (表格/变量)")]
    [Description("活字格中的列名或属性名，例如: 姓名")]
    public string TargetField { get; set; }
}
```

### 4.2 插件属性定义
```csharp
[DisplayName("字段映射配置")]
[ObjectListProperty]
public List<ColumnMapping> Mappings { get; set; }
```

### 4.3 运行时处理逻辑
```csharp
public override ExecuteResult Execute(IServerCommandExecuteContext dataContext)
{
    // 假设 apiData 是从外部获取的 JObject
    var apiData = JObject.Parse(jsonContent);
    var resultDict = new Dictionary<string, object>();

    foreach (var mapping in Mappings)
    {
        // 1. 根据 SourceField 从源数据获取值
        var value = apiData[mapping.SourceField]?.ToObject<object>();
        
        // 2. 映射到用户指定的 TargetField
        if (!string.IsNullOrEmpty(mapping.TargetField))
        {
            resultDict[mapping.TargetField] = value;
        }
    }

    // resultDict 现在包含了用户期望的键值对，可以直接用于更新表格或返回
    return ExecuteResult.CreateSuccess(resultDict);
}
```

---

## 5. 开发建议
- **简洁性**：优先使用基础类型，仅在必要时引入复杂对象。
- **安全性**：对所有属性值进行防御性编程，处理 `null` 或 `undefined` 的情况。
