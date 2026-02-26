# 添加属性 - 树结构属性 (Tree Property)

## 参考资料
[树结构属性 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/treeproperty)

## 概述
用于构建层级结构数据。

## 基础用法 ([TreeProperty])
节点类型必须实现 `ITreeNode` 接口。

```csharp
public class MyPluginCellType : CellType
{
    [TreeProperty(NodeType = typeof(MyNode))]
    public List<ITreeNode> Nodes { get; set; } = new List<ITreeNode>();
}

public class MyNode : ObjectPropertyBase, ITreeNode
{
    [DisplayName("节点文本")]
    public string Text { get; set; } // 实现 ITreeNode
    
    // 实现 ITreeNode: 子节点列表
    public IEnumerable<ITreeNode> Children { get; set; } = new List<MyNode>();
    
    // 其他属性
    public string Value { get; set; }
}
```

## 高级用法

### 设置默认节点名称 (DefaultNodeName)
```csharp
[TreeProperty(NodeType = typeof(MyNode), DefaultNodeName = "新节点")]
public List<ITreeNode> Nodes { get; set; }
```
