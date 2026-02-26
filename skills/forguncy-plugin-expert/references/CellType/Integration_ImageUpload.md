# 和活字格原生功能集成 - 支持图片上传 (Image Upload)

## 参考资料
[支持图片上传 - 活字格V11帮助文档](https://www.grapecity.com.cn/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/integratedwithhzgfunction/support-image-upload)

## 概述
插件可以调用活字格内置 API 实现文件上传功能，并受到系统的安全限制（如文件类型限制）。

## 实现步骤

### 1. 定义上传限制属性 (C#)
需要定义一个实现了 `IUploadLimit` 接口的辅助类，并将其作为属性添加到插件中。
**必须标记 `[ServerProperty]`**，以便在运行时传递给前端。

```csharp
public class MyPluginCellType : CellType
{
    [DisplayName("允许的文件类型")]
    public string Accept { get; set; } = ".jpg,.png";

    [Browsable(false)]
    [SaveJsonIgnore]
    [ServerProperty] // 关键：标记为服务端属性
    public UploadLimit UploadLimit
    {
        get
        {
            return new UploadLimit() { ExtensionFilter = this.Accept };
        }
    }
}

public class UploadLimit : IUploadLimit
{
    public string ExtensionFilter { get; set; }
    public double SizeLimit { get; set; }
}
```

### 2. 前端调用上传 API (JS)
使用 `Forguncy.Common.uploadImageToServer` 方法。

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        const accept = this.CellElement.CellType.Accept;
        // 获取上传限制对象的 ID
        const uploadLimitId = this.CellElement.ServerPropertiesId.UploadLimit;

        const fileInput = $("<input type='file'>");

        fileInput.on("change", () => {
            const file = fileInput[0].files[0];
            if (!file) return;

            Forguncy.Common.uploadImageToServer(
                file,
                null,
                accept,
                (fileName) => {
                    // 成功回调：fileName 是服务器上的相对路径
                    console.log("上传成功: " + fileName);
                    
                    // 获取完整预览 URL
                    const url = Forguncy.Helper.SpecialPath.getBaseUrl() + 
                                Forguncy.ModuleLoader.getCdnUrl("FileDownloadUpload/Download?file=" + encodeURIComponent(fileName));
                },
                (error) => {
                    alert("上传失败: " + error);
                },
                undefined,
                uploadLimitId // 关键：传入限制 ID
            );
        });

        return fileInput;
    }
}
```
