> Source: assembly-could-not-be-loaded.md (Imported from external documentation)

# 如何解决程序集无法加载的问题

## Content

## <span class="ne-text">问题描述</span>

<span class="ne-text">开发服务端命令或中间件时，引人了第三方包，开发和编译时都没有问题，但是在执行这个服务端命令时，会报以下错误：</span>
<span class="ne-text">Could not load file or assembly 'RestSharp, Version=110.1.0.0, Culture=neutral, PublicKeyToken=598062e77f915f75'. Could not find or load a specific file. (0x80131621)</span>

## <span class="ne-text">问题调查</span>

<span class="ne-text">出现这个错误，通常是因为第三方库中使用 DLL 文件在活字格服务器中也被使用了，而活字格服务器使用的DLL版本却低于类库中引用的版本。例如问题描述中的例子，是加载 RestSharp.dll 失败了。</span>
<span class="ne-text">可以打开活字格的 bin 目录找到 RestSharp.dll 文件。</span>
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.03739c.png)
<span class="ne-text">通过查看文件属性，可以查看活字格中引用的 DLL 的版本。</span>
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.40e6a8.png)
<span class="ne-text">根据异常信息可以知道，第三方类库尝试加载 RestSharp.dll 的版本号为 110.1.0.0，活字格引用的版本号是 106.15.0.0，而.NET框架的策略是：如果主进程（活字格）依赖的版本高，插件依赖的版本低，是可以正确加载的。反之，则会加载失败。</span>

## <span class="ne-text">解决方案</span>

### <span class="ne-text">方法一：直接从活字格的Bin目录引用</span>

<span class="ne-text">1.首先从NuGet里删除RestSharp包。</span>
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.dc997e.png)
<span class="ne-text">2.通过添加引用直接引用活字格中的对应的Assembly文件。</span>
<span class="ne-text">3.选择“添加项目引用”。</span>
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.261478.png)
4.<span class="ne-text">单击“浏览”。</span>
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.3f1e94.png)
5.找到活字格的安装目录，找到对应的DLL文件，单击“添加”。
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.1d7587.png)
6.<span class="ne-text">添加后即可在程序集中找到RestSharp引用。重新编译解决方案即可。</span>
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.774c35.png)

### <span class="ne-text">方法二：降低第三方类库的版本</span>

<span class="ne-text">有些时候，无法直接通过添加活字格安装目录的DLL来解决问题，可能是因为这个DLL是用过第三方类库间接引用的，这种情况的话方法一就不能解决问题。</span>
<span class="ne-text">此时可以通过降低第三方类库的版本，确保插件依赖的版本号低于活字格依赖的版本号，例如，InfluxDB.Clent.Core 最新版依赖的RestSharp的版本是110.1.0.0 会导致这个问题，只需要安装一个较低版本的InfluxDB.Clent.Core，查看它依赖的RestSharp版本低于 106.15.0.0 即可。</span>
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.690fee.png)
<span class="ne-text">通过查看InfluxDB.Clent.Core可以发现 3.3.0 版本依赖的 RestSharp 版本为 106.12.0.0，低于106.15.0.0。 所以安装InfluxDB.Clent.Core的3.3.3版本就可以解决问题了。</span>
![image](/DOCUMENT_SITE_LINK_PREFIX_HERE/document-site-files/images/03fe0519-46b1-4a5e-a4a7-f63ca4bfa6df/image.5bce96.png)