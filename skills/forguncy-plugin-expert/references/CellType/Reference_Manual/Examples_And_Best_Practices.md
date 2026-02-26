# Examples And Best Practices

## Practicalcombat

# 实战

## Content

*   [集成第三方类库-Tinymce](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/practicalcombat/integratethirdpartyclasslibrarytinymce)
    *   [快速开始，添加Tinymce单元格插件](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/practicalcombat/integratethirdpartyclasslibrarytinymce/addtinymcecellplugin)
    *   [添加中文资源与定制菜单](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/practicalcombat/integratethirdpartyclasslibrarytinymce/addchineseresourcesandcustomizedmenus)
    *   [改造为表单单元格](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/practicalcombat/integratethirdpartyclasslibrarytinymce/converttoformcell)
*   [集成Vue组件](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/practicalcombat/integratevuecomponents)
    *   [集成Vue](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/practicalcombat/integratevuecomponents/integratevue)
    *   [Vue 集成单元格值](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/practicalcombat/integratevuecomponents/vueintegratedcellvalue)
    *   [集成 Vue 组件的方法与事件](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/practicalcombat/integratevuecomponents/integratemethodsandeventsofvuecomponents)
    *   [集成第三方 Vue 组件类库](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/practicalcombat/integratevuecomponents/integratethirdpartyvuecomponentlibraries)

---

## Integratethirdpartyclasslibrarytinymce

# 集成第三方类库-Tinymce

## Content

*   [快速开始，添加Tinymce单元格插件](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/practicalcombat/integratethirdpartyclasslibrarytinymce/addtinymcecellplugin)
*   [添加中文资源与定制菜单](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/practicalcombat/integratethirdpartyclasslibrarytinymce/addchineseresourcesandcustomizedmenus)
*   [改造为表单单元格](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/practicalcombat/integratethirdpartyclasslibrarytinymce/converttoformcell)

---

## Integratevuecomponents

# 集成Vue组件

## Content

*   [集成Vue](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/practicalcombat/integratevuecomponents/integratevue)
*   [Vue 集成单元格值](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/practicalcombat/integratevuecomponents/vueintegratedcellvalue)
*   [集成 Vue 组件的方法与事件](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/practicalcombat/integratevuecomponents/integratemethodsandeventsofvuecomponents)
*   [集成第三方 Vue 组件类库](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/practicalcombat/integratevuecomponents/integratethirdpartyvuecomponentlibraries)

---

## ReactExample

# React示例：开发AntDesign Table 单元格

## Content

<span class="ne-text">本例会演示如何使用前端工程化模板，一步一步开发一个 </span>[<span class="ne-text">AntDesign 表格</span>](https://ant.design/components/table-cn){:target="_blank"}<span class="ne-text">单元格。此单元格会包含以下功能：</span>

1. <span class="ne-text">数据绑定：展示活字格数据表数据；</span>
2. <span class="ne-text">行点击事件：点击行时，执行活字格命令；</span>
3. <span class="ne-text">通过公式修改表格标题；</span>
4. <span class="ne-text">通过属性控制是否显示表格前端分页组件。</span>

#### <span class="ne-text">通过活字格插件创建器，创建工程模板</span>

#### <span class="ne-text">安装 AntDesign</span>

<span class="ne-text">启动命令行，执行下列命令：</span>

1. `<span class="ne-text">cd C:\\Users\\roberthu\\Documents\\HZG-Plugins\\AntdTable\\AntdTable\\FrontEndModule</span>`
2. `<span class="ne-text">npm install antd</span>`

<span class="ne-text">安装成功后，就可以在活字格的前端项目中使用 AntDesign 的组件。</span>

#### <span class="ne-text">添加属性定义</span>

1. <span class="ne-text">使用 VisualStudio 打开 “C:\\Users\\roberthu\\Documents\\HZG-Plugins\\AntdTable\\AntdTable.sln” 项目。</span>
2. <span class="ne-text">编译，确保前端项目的 </span>`<span class="ne-text">npm install</span>`<span class="ne-text"> 被执行。</span>
3. <span class="ne-text">打开 AntdTableCellType.cs 文件，按如下代码修改，按照需求定义数据源属性 </span>[<span class="ne-text">参考</span>](https://www.yuque.com/robert-bh51n/ea8l6c/wmx4wh9c5q5s5x67)<span class="ne-text">，行点击命令 </span>[<span class="ne-text">参考</span>](https://www.yuque.com/robert-bh51n/ea8l6c/lq26nef34eb3mru1)<span class="ne-text">，表格标题属性 </span>[<span class="ne-text">参考</span>](https://www.yuque.com/robert-bh51n/ea8l6c/keoludxsp0diwbgk)<span class="ne-text">，显示分页 </span>[<span class="ne-text">参考</span>](https://www.yuque.com/robert-bh51n/ea8l6c/zuoi0fknr7d29wxt)<span class="ne-text">。</span>

```auto
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;
using System.ComponentModel;

namespace AntdTable
{
    [Designer("AntdTable.Designer.AntdTableCellTypeDesigner, AntdTable")]
    public class AntdTableCellType : CellType
    {
        [CustomCommandObject(InitParamProperties = "record", InitParamValues = "数据行")]
        [DisplayName("行点击命令")]
        public object RowClickCommand { get; set; }

        [BindingDataSourceProperty]
        [DisplayName("绑定数据源")]
        public object DataSource { get; set; }

        [FormulaProperty]
        [DisplayName("表格标题")]
        public object Title { get; set; }

        [BoolProperty(IndentLevel = 0)]
        [DisplayName("显示分页条")]
        public bool ShowPagination { get; set; }

        public override string ToString()
        {
            return "AntDesign 表格单元格";
        }
    }
}
```

---

## VueExample

# Vue示例：开发ElementPlus Table单元格

## Content

本例会演示如何使用前端工程化模板，一步一步开发一个 [ElementPlus 表格](https://element-plus.org/zh-CN/component/table.html){:target="_blank"}单元格。此单元格包含以下功能：

1. 数据绑定：展示活字格数据表数据；
2. 行点击事件：点击行时，执行活字格命令；
3. 通过公式修改表格标题；
4. 通过属性控制是否显示表格前端分页组件。

#### 通过活字格插件创建器，创建工程模板

#### 安装ElementPlus

启动命令行，执行下列命令：

1. `cd C:\Users\roberthu\Documents\HZG-Plugins\ElementTable\ElementTable\FrontEndModule`
2. `npm install element-plus`

安装成功后，就可以在活字格的前端项目中使用 ElementPlus 的组件。

#### 添加属性定义

1. 使用 VisualStudio 打开 “C:\\Users\\roberthu\\Documents\\HZG-Plugins\\ElementTable\\ElementTable.sln” 项目。
2. 编译，确保前端项目的`npm install`被执行。
3. 打开 ElementTableCellType.cs 文件，按如下代码修改，按照需求定义参考[数据源属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/datasourceproperty)，行点击命令参考[命令属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/commandproperty)，表格标题属性参考[公式属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/formulaproperty)，显示分页参考[布尔属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/booleanproperty)。

```csharp
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;
using System.ComponentModel;

namespace ElementTable
{
    [Designer("ElementTable.Designer.ElementTableCellTypeDesigner, ElementTable")]
    public class ElementTableCellType : CellType
    {
        [CustomCommandObject(InitParamProperties = "record", InitParamValues = "数据行")]
        [DisplayName("行点击命令")]
        public object RowClickCommand { get; set; }

        [BindingDataSourceProperty]
        [DisplayName("绑定数据源")]
        public object DataSource { get; set; }

        [FormulaProperty]
        [DisplayName("表格标题")]
        public object Title { get; set; }

        [BoolProperty(IndentLevel = 0)]
        [DisplayName("显示分页条")]
        public bool ShowPagination { get; set; }

        public override string ToString()
        {
            return "饿了么表格单元格";
        }
    }
}
```

#### 添加前端属性定义

修改FrontEndModule/src/ElementTableCellType.ts 文件的 ElementTableCellTypeMetadata 接口，添加 TypeScript 属性声明。名字要和 ElementTableCellType.cs 文件对应。

```typescript
import ElementTableCellTypeComponent from './ElementTableCellTypeComponent.vue'
import { createApp, type App as VueAppInstance } from 'vue'
import ElementPlus from 'element-plus'

export interface ElementTableCellTypeMetadata {
    RowClickCommand: Forguncy.Plugin.ICustomCommandObject
    DataSource: object
    Title: string
    ShowPagination: boolean
}

export default class ElementTableCellType extends Forguncy.Plugin.CellTypeBase<ElementTableCellTypeMetadata> {
    vueApp: VueAppInstance | undefined;
    root?: JQuery;
    constructor(...args: unknown[]) {
        super(...args);
    }
    async onPageLoaded() {
        this.vueApp = createApp(ElementTableCellTypeComponent, {
            cellType: this
        });
        this.vueApp.use(ElementPlus)
        this.vueApp.mount(this.root![0]);
    }

    createContent() {
        this.root = $('<div style="height:100%"></div>');
        return this.root;
    }
    destroy(): void {
        if (this.vueApp) {
            this.vueApp.unmount();
            this.vueApp = undefined;
        }
        super.destroy();
    }
}
```

#### 添加前端实现

<span class="ne-text">修改FrontEndModule/src/ElementTableCellTypeComponent.vue 文件如下：</span>

```auto
<template>
    <el-card>
        <div slot="header">
            {{title}}
        </div>
        <el-table :data="pagedData" style="width: 100%" @row-click="handleRowClick">
            <el-table-column v-for="col in columns"
                             :key="col.prop"
                             :prop="col.prop"
                             :label="col.prop" />
        </el-table>
        <el-pagination v-if="cellTypeMeta.ShowPagination"
                       layout="total, sizes, prev, pager, next, jumper"
                       @size-change="handleSizeChange"
                       @current-change="handleCurrentChange"
                       :total="dataSource.length" />
    </el-card>
</template>
<script setup lang="ts">
    import { computed, onMounted, ref } from 'vue'
    import type { ElementTableCellTypeMetadata } from './ElementTableCellType'
    import 'element-plus/dist/index.css'

    interface Props {
        cellType: Forguncy.Plugin.CellTypeBase<ElementTableCellTypeMetadata>
    }
    const props = defineProps<Props>()
    const cellType = props.cellType
    const cellTypeMeta = cellType.CellElement.CellType

    const title = ref(null)
    const dataSource = ref<Record<string, any>[]>([])
    const columns = ref<{ prop: string }[]>([])
    const pageSize = ref(10)
    const currentPage = ref(1)

    const pagedData = computed(() => {
        const start = (currentPage.value - 1) * pageSize.value
        return dataSource.value.slice(start, start + pageSize.value)
    })

    const handleSizeChange = (size: number) => {
        pageSize.value = size
    }

    const handleCurrentChange = (page: number) => {
        currentPage.value = page
    }

    const handleRowClick = (record: unknown) => {
        const initParam: Record<string, unknown> = {};
        initParam[cellTypeMeta.RowClickCommand.ParamProperties["record"]] = record;
        cellType.executeCustomCommandObject(cellTypeMeta.RowClickCommand, initParam)
    }

    onMounted(() => {
        cellType.onFormulaResultChanged(cellTypeMeta.Title, (result) => {
            title.value = result
        })
        cellType.getBindingDataSourceValue(cellTypeMeta.DataSource, null, (data) => {
            dataSource.value = data
            const autoColumns: { prop: string }[] = []
            if (data && data.length > 0) {
                const keys = Object.keys(data[0])
                keys.forEach(key => {
                    autoColumns.push({
                        prop: key,
                    })
                })
            }
            columns.value = autoColumns
        }, true)
    })
</script>
```

代码说明：

1. 通过 props.cellType 可以获取单元格实例；
2. 通过 props.cellType.CellElement.CellType 可以获取单元格的配置；
3. 使用 useEffect 钩子，在初始化逻辑里：
    1. 通过调用 cellType 的 onFormulaResultChanged 获取并订阅公式计算结果，参考[公式属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/formulaproperty) ；
    2. 通过调用 getBindingDataSourceValue 方法，获取并订阅数据源绑定结果，参考[数据源属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/datasourceproperty)；
4. 通过 executeCustomCommandObject 方法执行命令，参考[命令属性](/solutions/huozige/help/docs/plugindevelopment/plugindevelop/developcelltypeplugin/addproperty/commandproperty)。

#### 设计器效配置

#### 运行效果

---

## Integratemethodsandeventsofvuecomponents

# 集成 Vue 组件的方法与事件

## Content

在上一节中，介绍了如何创建一个插件单元格使用 Vue的组件和属性。本章节讲介绍如何把Vue的方法和事件与活字格的命令和单元格操作集成。
假设在按钮点击时，希望执行活字格的命令。并且单元格提供两个单元格操作。一个是修改标签文本，一个是控制 count 属性自增。
**C# 端代码如下：**

```
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;

namespace MyPlugin
{
    [DependenceRuntimModule("vue3")]
    public class MyPluginCellType : CellType
    {
        [CustomCommandObject]
        public object ClickComment { get; set; }
        public string Label { get; set; } = "点击次数为";

        [RunTimeMethod]
        public void CountAdd()
        {
        }

        [RunTimeMethod]
        public void ChangeLabel(string label)
        {
        }
    }
}
```

**JavaScript 代码如下：**

```
/// <reference path="../Declarations/forguncy.d.ts" />
/// <reference path="../Declarations/forguncy.Plugin.d.ts" />

class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.content = $("<div/>");
        return this.content;
    }
    onPageLoaded() {
        const uid = "uid-" + new Date().valueOf();
        const self = this;
        this.content.attr("id", uid);
        const option = {
            template:
                `<div id="app">
  <button @click="onClick">
    {{label}} : {{ count }}
  </button>
</div>`,
            data() {
                return {
                    count: 0,
                    label: self.CellElement.CellType.Label
                }
            },
            methods: {
                onClick() {
                    self.executeCustomCommandObject(self.CellElement.CellType.ClickCommand);
                    this.addOne();
                },
                addOne() {
                    this.count++;
                },
                changeLabel(newLabel) {
                    this.label = newLabel;
                }
            }
        };
        option.beforeCreate = function () {
            self.vue = this;
        };
        this.vueApp = Vue.createApp(option);
        this.vueApp.mount(`#${uid}`);
    }
    CountAdd() {
        this.vue.addOne();
    }
    ChangeLabel(label) {
        this.vue.changeLabel(label);
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

修改点：

1. 给 option 对象添加了 methods 属性。
2. methods 属性声明了三个方法，分别为： onClick, addOne 和 changeLabel。 这三个方法执行的上下文都是vue 组件内部，可以直接操作(获取或设值) vue 组件的属性。
3. 组件模板中，按钮的click 事件绑定了 onClick。点击按钮时， onClick 方法会被调用。在onClick 方法中，可以执行活字格的命令。
4. 单元格上声明了和C# 的 RunTimeMethod 同名的方法。 执行单元格操作时会被自动调用。在这个方法中，可以通过 this.vue.proxy 获得vue 组件，并调用vue组件内部方法，会操作属性。this.vue 通过监听beforeCreate 生命周期获得vue实例。

**设计时效果：**

**运行时效果如下：**

---

## Integratethirdpartyvuecomponentlibraries

# 集成第三方 Vue 组件类库

## Content

在之前章节中已经讲解了如何集成Vue组件的属性、事件和方法。 在 Vue 生态中有大量的第三方组件类库资源。本章节将以集成Element Plus 为例，讲解如何集成Vue 组件。

**首先，通过修改PluginConfig.json 文件，引人第三方组件的Js。**

找到Element Plugs CDN 上的Js，Css 文件并下载到插件的 Resources 文件夹内。

  

```
{
  "assembly": [
    "MyPlugin.dll"
  ],
  "css": [
    "Resources/Element/index.css"
  ],
  "javascript": [
    "Resources/Element/index.full.min.js",
    "Resources/MyPluginCellType.js"
  ],
  "serverApiAssembly": [],
  "image": "Resources/PluginLogo.png",
  "description": "这是一个活字格插件",
  "name": "我的插件",
  "pluginType": "cellType,command",
  "guid": "f1e8c65d-9009-4e7e-b2a4-b6ff4c00e458",
  "version": "1.0.0.0",
  "dependenceVersion": "8.0.104.0",
  "bundleJavaScript": true,
  "bundleCSS": true
}
```

**修改C# 代码如下：**

```
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Commands;
using GrapeCity.Forguncy.Plugin;

namespace MyPlugin
{
    [DependenceRuntimModule("vue3")]
    public class MyPluginCellType : CellType
    {
        [CustomCommandObject]
        public object ClickCommand { get; set; }

        [ComboProperty(ValueList = "success|warning|info|error")]
        public string icon { get; set; } = "success ";

        public string title { get; set; } = "标题";

        public string subTitle { get; set; } = "这里是子标题，可以是一些描述";

        public string buttonText { get; set; } = "返回";
    }
}
```

**修改JavaScript 代码如下：**

```
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.content = $("<div/>");
        return this.content;
    }
    onPageLoaded() {
        const uid = "uid-" + new Date().valueOf();
        this.content.attr("id", uid);
        const self = this;
        const cellType = this.CellElement.CellType;
        const option = {
            template:
                `<el-result
  :icon="icon"
  :title="title"
  :sub-title="subTitle"
>
  <template #extra>
    <el-button type="primary" @click="onClick">{{buttonText}}</el-button>
  </template>
</el-result>`,
            data() {
                return {
                    title: cellType.title,
                    icon: cellType.icon,
                    subTitle: cellType.subTitle,
                    buttonText: cellType.buttonText,
                }
            },
            methods: {
                onClick() {
                    self.executeCustomCommandObject(self.CellElement.CellType.ClickCommand);
                },
            }
        };
        this.vueApp = Vue.createApp(option);
        this.vueApp.use(window.ElementPlus);
        this.vueApp.mount(`#${uid}`);
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

  

**设计时效果：**

****

**运行时效果如下：**

---

## Integratevue

# 集成Vue

## Content

Vue 是目前流行的前端框架，有大量的开源库资源可以使用。活字格可以使用Vue开发单元格插件，达到事半功倍的效果。
**从最简单的Vue例子开始**
活字格自带了Vue3的运行时环境，所以开发 Vue 单元格插件不需要引用 Vue 的 js，只需要声明DependenceRuntimModule 即可。
**C# 端代码如下：**

```javascript
using GrapeCity.Forguncy.CellTypes;
using GrapeCity.Forguncy.Plugin;

namespace MyPlugin
{
    [DependenceRuntimModule("vue3")]
    public class MyPluginCellType : CellType
    {
        public string Label { get; set; } = "点击次数为";
    }
}
```

**JavaScript 代码如下：**

```javascript
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.content = $("<div/>");
        return this.content;
    }
    onPageLoaded() {
        const uid = "uid-" + new Date().valueOf();
        const self = this;
        this.content.attr("id", uid);
        const option = {
            template: 
`<div id="app">
  <button @click="count++">
    {{label}} : {{ count }}
  </button>
</div>`,
            data() {
                return {
                    count: 0,
                    label: self.CellElement.CellType.Label
                }
            }
        };
        this.vueApp = Vue.createApp(option);
        this.vueApp.mount(`#${uid}`);
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

代码详解：

1. 在 createContent 只需要创建一个空 div 作为 Vue 组件的容器。
2. 具体的处理逻辑要写在 onPageLoaded 函数中，因为 Vue 组件要求容器 div 必须已经挂载到Dom 树中。
3. 代码第7,8行，生成一个唯一的 Id，并把Id设置到容器上，因为 VueApp 的 mount 方法必须提供一个Id。
4. 第10行开始，构建一个option 对象，vue 组件的设置都会写到 option 对象中。最重要的属性就是 template属性和 data 属性。 template 属性用于变形 Vue 的模板，可以使用 \`\` 符号包裹多行模板字符串。
5. data 必须是一个函数，返回一个Json对象，对象上的属性可以直接和模板中的属性绑定。data 对象上的属性可以是静态值，也可以是活字格的属性。
6. 最后，通过 Vue.createApp 方法，创建一个Vue 的App。
7. 通过 vueApp 的 mount 方法把 vueApp 的单元格的容器Dom 绑定。

**运行时效果如下：**

---

## Vueintegratedcellvalue

# Vue 集成单元格值

## Content

本章节将介绍如何把单元格的值和Vue集成。

### 如果仅用于显示

在data上定义一个普通属性，重写setValueToElement方法，在setValueToElement设置这个属性即可。

```
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.content = $("<div/>");
        return this.content;
    }
    onPageLoaded() {
        const uid = "uid-" + new Date().valueOf();
        const self = this;
        this.content.attr("id", uid);
        const option = {
            template:
  `<button>{{text}}</button>`,
            data() {
                return {
                    text: ""
                }
            }
        };
        option.beforeCreate = function () {
            self.vue = this;
        };
        this.vueApp = Vue.createApp(option);
        this.vueApp.mount(`#${uid}`);
    }
    setValueToElement(_, value) {
        this.vue.text = value?.toString();
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```

### 双向绑定实现编辑

VUE 支持通过 v-model 双向绑定受控组件（通常是表单控件），对于此类组件，可以实现对单元格值的编辑。代码如下：

```
class MyPluginCellType extends Forguncy.Plugin.CellTypeBase {
    createContent() {
        this.content = $("<div/>");
        return this.content;
    }
    onPageLoaded() {
        const uid = "uid-" + new Date().valueOf();
        const self = this;
        this.content.attr("id", uid);
        const option = {
            template:
  `<input v-model="text" @change="handleChange">`,
            data() {
                return {
                    text: ""
                }
            },
            methods: {
                handleChange() {
                    self.commitValue();
                }
            }
        };
        option.beforeCreate = function () {
            self.vue = this;
        };
        this.vueApp = Vue.createApp(option);
        this.vueApp.mount(`#${uid}`);
    }
    setValueToElement(_, value) {
        this.vue.text = value?.toString();
    }
    getValueFromElement() {
        return this.vue.text;
    }
}
Forguncy.Plugin.CellTypeHelper.registerCellType("MyPlugin.MyPluginCellType, MyPlugin", MyPluginCellType);
```