> Source: cache-service-optimization.md (Imported from external documentation)

# 缓存服务优化

## Content

新版本我们对缓存服务进行了优化，为原本的所有缓存方法提供了异步重载方法，并且优化了实现。本章将介绍这些缓存优化的方法。
目前，活字格内的缓存主要有两种实现方式：

* 普通环境下使用 MemoryCache
* 负载均衡环境下使用 Redis

在普通模式下，由于MemoryCache是内存操作，因此使用同步或异步方法没有本质区别；但是在负载均衡环境下，由于缓存数据存储在Redis中，为了支持更大的并发以最大化地提升性能，我们强烈建议您将缓存方式改为异步。
1.验证缓存项是否存在
旧版实现（建议弃用）

```csharp
/// <summary>
/// 验证缓存项是否存在
/// </summary>
/// <param name="key">缓存键</param>
/// <returns>是否存在</returns>
[Obsolete]
bool Exists(string key);
```

 新版添加（建议使用）

```csharp
/// <summary>
/// 验证缓存项是否存在
/// </summary>
/// <param name="key">缓存键</param>
/// <returns>是否存在</returns>
Task<bool> ExistsAsync(string key);
```

2.添加缓存
旧版实现（建议弃用）

```csharp
/// <summary>
/// 添加缓存
/// </summary>
/// <param name="key">缓存键</param>
/// <param name="value">缓存Value</param>
/// <returns>是否成功</returns>
[Obsolete]
bool Add(string key, object value);

/// <summary>
/// 添加缓存
/// </summary>
/// <param name="key">缓存键</param>
/// <param name="value">缓存Value</param>
/// <param name="expiresIn">缓存过期时间</param>
/// <returns>是否成功</returns>
[Obsolete]
bool Add(string key, object value, TimeSpan expiresIn);
```

 新版添加（建议使用）

```csharp
/// <summary>
/// 添加缓存
/// </summary>
/// <param name="key">缓存键</param>
/// <param name="value">缓存Value</param>
/// <returns>是否成功</returns>
Task<bool> AddAsync(string key, object value);

/// <summary>
/// 添加缓存
/// </summary>
/// <param name="key">缓存键</param>
/// <param name="value">缓存Value</param>
/// <param name="expiresIn">缓存过期时间</param>
/// <returns>是否成功</returns>
Task<bool> AddAsync(string key, object value, TimeSpan expiresIn);
```

3.删除缓存
旧版实现（建议弃用）

```csharp
/// <summary>
/// 删除缓存
/// </summary>
/// <param name="key">缓存键</param>
/// <returns>是否成功</returns>
[Obsolete]
bool Remove(string key);

/// <summary>
/// 批量删除缓存
/// </summary>
/// <param name="keys">缓存键集合</param>
[Obsolete]
void RemoveAll(IEnumerable<string> keys);
```

 新版添加（建议使用）

```csharp
/// <summary>
/// 删除缓存
/// </summary>
/// <param name="key">缓存键</param>
/// <returns>是否成功</returns>
Task<bool> RemoveAsync(string key);

/// <summary>
/// 批量删除缓存
/// </summary>
/// <param name="keys">缓存键集合</param>
Task RemoveAllAsync(IEnumerable<string> keys);
```

4.获取缓存
旧版实现（建议弃用）

```csharp
/// <summary>
/// 获取缓存
/// </summary>
/// <param name="key">缓存键</param>
/// <returns>缓存值</returns>
[Obsolete]
T Get<T>(string key);

/// <summary>
/// 获取缓存
/// </summary>
/// <param name="key">缓存键</param>
/// <returns>缓存值</returns>
[Obsolete]
object Get(string key);
```

 新版添加（建议使用）

```csharp
/// <summary>
/// 获取缓存
/// </summary>
/// <param name="key">缓存键</param>
/// <returns>缓存值</returns>
Task<T> GetAsync<T>(string key);

/// <summary>
/// 获取缓存
/// </summary>
/// <param name="key">缓存键</param>
/// <returns>缓存值</returns>
Task<object> GetAsync(string key);
```

5.修改缓存
旧版实现（建议弃用）

```csharp
/// <summary>
/// 修改缓存
/// </summary>
/// <param name="key">缓存键</param>
/// <param name="value">缓存Value</param>
/// <returns>是否成功</returns>
[Obsolete]
bool Replace(string key, object value);

/// <summary>
/// 修改缓存
/// </summary>
/// <param name="key">缓存键</param>
/// <param name="value">缓存Value</param>
/// <param name="expiresIn">缓存时长</param>
/// <returns>是否成功</returns>
[Obsolete]
bool Replace(string key, object value, TimeSpan expiresIn);
```

 新版添加（建议使用）

```csharp
/// <summary>
/// 修改缓存
/// </summary>
/// <param name="key">缓存键</param>
/// <param name="value">缓存Value</param>
/// <returns>是否成功</returns>
Task<bool> ReplaceAsync(string key, object value);

/// <summary>
/// 修改缓存
/// </summary>
/// <param name="key">缓存键</param>
/// <param name="value">缓存Value</param>
/// <param name="expiresIn">缓存时长</param>
/// <returns>是否成功</returns>
Task<bool> ReplaceAsync(string key, object value, TimeSpan expiresIn);
```

6.获取或添加（新版新增）

```csharp
/// <summary>
/// 获取或添加
/// </summary>
/// <param name="key">缓存键</param>
/// <param name="value">缓存Value</param>
/// <param name="expiresIn">缓存时长</param>
/// <returns>缓存值</returns>
Task<T> GetOrSetAsync<T>(string key, string value, TimeSpan expiresIn);
```

 需要注意以下两点：
1\. 同步方法仅保留兼容性，不再推荐。建议尽快修改它。
2\. 此特性为 10\.0\.100\.0 版本新增的特性。