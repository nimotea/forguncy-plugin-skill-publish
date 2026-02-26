# Other Functions

## JavaPluginDiagnosticLog

# Java插件诊断日志

## Content

Java插件写入诊断日志，需要引用 forguncy-logger-abstractions 接口包。如果项目通过构建工具初始化，那么会自动引入此包，如果是手动创建的 Java 项目则需要在设计器安装目录（默认为 C:\\Program Files\\Forguncy 10\\WebSite\\javaAdapterServerBin）下手动引用此包：
c

日志包引用后即可在项目的任意位置写入Java诊断日志，此文档中默认以 ServerCommand 项目作为示例。
我们可以在构造方法、重载方法中记录日志，记录的方式主要有两种：

1. 直接调用 Logger 类中的静态方法。

2. 可以引用slf4j 通用日志接口直接记录。

以上两种方法是等价的。
当写入日志的Java插件被设计器加载后，即可在本地的日志目录（默认路径为：%Temp%/ForguncyDesignerLog/ForguncyJavaAdapter）中查看：

如果对应的工程上传到了 AdminPortal 中，那么用户还可以在 AdminPortal 的诊断日志界面中查看相应的日志：

---

## Log

# 日志

## Content

### 服务端命令日志

在服务端命令代码逻辑中添加日志，可以方便用户调试服务端命令，了解命令的执行状态。在`execute `方法内调用 `Logger `类中的方法来写日志

```auto
public class MyPluginServerCommand extends Command implements ICommandExecutableInServerSide {

    @Override
    public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
        Logger.error("错误信息");
        Logger.warning("警告信息");
        Logger.info("info信息");
        Logger.debug("debug信息");
        Logger.trace("trace信息");
        return new ExecuteResult();
    }

    @Override
    public String toString() {
        return "我的服务端命令插件";
    }
}
```

 

### Web Api 日志

```auto
package org.example;

import com.grapecity.forguncy.Logger;
import com.grapecity.forguncy.serverapi.annotation.Get;
import com.grapecity.forguncy.serverapi.entity.ForguncyApi;

import java.io.IOException;
import java.io.PrintWriter;

public class CustomApiT2 extends ForguncyApi {
    @Get
    public void helloWorld() throws IOException {
        Logger.error("错误信息");
        Logger.warning("警告信息");
        Logger.info("info信息");
        Logger.debug("debug信息");
        Logger.trace("trace信息");
        this.getContext().getResponse().setContentType("text/plain");
        String message = "Hello World CustomApiT2";
        PrintWriter out = this.getContext().getResponse().getWriter();
        out.print(message);
        out.close();
    }
}
```

### 安全提供程序

安全提供程序可以在 verifyUser getSettings 等方法中使用Logger 记录日志。

```auto
    @Override
    public User verifyUser(HashMap<String, String> properties) {
        Logger.error("错误信息");
        Logger.warning("警告信息");
        Logger.info("info信息");
        Logger.debug("debug信息");
        Logger.trace("trace信息");
        String name = properties.get("userName");
        for (User user : getUserInformations().getUsers()) {
            if (user.getUserId().equals(name)) {
                return user;
            }
        }
        return null;
    } 
```

效果如下：

* 如果是在设计器，在%Temp%\\ForguncyDesignerLog\\ForguncyJavaAdapter 目录下查看。
* 如果是在服务器，在日志存储目录下的ForguncyJavaAdapter目录中。

 
默认开启的日志级别是INFO 级别，只输出INFO 以上的日志信息。

---

## DatabaseLink

# 数据库连接选择属性

## Content

```auto
@Data
public class MyPluginServerCommand2 extends Command implements ICommandExecutableInServerSide {

    @DatabaseConnectionSelectorProperty
    private String string;

    @Override
    public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
        var dataAccess = dataContext.getDataAccess();
        var connectionStr = dataContext.getDataAccess().getConnectionStringByID(string);
        dataAccess.beginTransaction(connectionStr);
        var sqlValue = dataAccess.executeSql(string, "select * from test", null);
        dataAccess.commitTransaction(connectionStr);
        var result = new ExecuteResult();
        result.getReturnValues().put("connectionStr",connectionStr);
        result.getReturnValues().put("sqlValue",sqlValue);
        return result;
    }

    @Override
    public String toString() {
        return "我的服务端命令插件";
    }
}
```

在设计器中效果如下，在数据库连接管理中连接了外部数据库之后：
 
可以通过标注了@DatabaseConnectionSelectorProperty 的属性选择特定数据库。

如果需要更细致的控制，可以通过@DatabaseConnectionSelectorProperty的其他属性来控制
**（空）显示为内建库**

1. 设置DatabaseConnectionSelectorProperty的IncludeBuiltInDatabase属性
2. 代码

    ```auto
    @Data
    public class MyPluginServerCommand2 extends Command implements ICommandExecutableInServerSide {
    
        @DatabaseConnectionSelectorProperty(includeBuiltInDatabase = true)
        private String string;
    
        @Override
        public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
            var dataAccess = dataContext.getDataAccess();
            var connectionStr = dataContext.getDataAccess().getConnectionStringByID(string);
            dataAccess.beginTransaction(connectionStr);
            var sqlValue = dataAccess.executeSql(string, "select * from test", null);
            dataAccess.commitTransaction(connectionStr);
            var result = new ExecuteResult();
            result.getReturnValues().put("connectionStr",connectionStr);
            result.getReturnValues().put("sqlValue",sqlValue);
            return result;
        }
    
        @Override
        public String toString() {
            return "我的服务端命令插件";
        }
    }
    ```
3. 效果
    

4. 说明
    对于内建数据库（Sqlite）连接名称为null

注意，标注@DatabaseConnectionSelectorProperty的属性类型必须是 String。

---

## ContextParameterValuePassing

# 上下文参数值传递

## Content

在使用命令的过程中，经常会在上下文参数中添加对应的值。

* 传递基本类型的值，用int类型举例

比如：

```auto
public class MyPluginServerCommand extends Command implements ICommandExecutableInServerSide {

    @Override
    public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
        dataContext.getParameters().put("number", 1);
        return new ExecuteResult();
    }

    @Override
    public String toString() {
        return "我的服务端命令插件";
    }
}
auto
public class MyPluginServerCommand3 extends Command implements ICommandExecutableInServerSide {

    @Override
    public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
        var number = (int)dataContext.getParameters().get("number");
        executeResult.getReturnValues().put("number", number);
        return executeResult;
    }

    @Override
    public String toString() {
        return "我的服务端命令插件3";
    }
}
```

* 传递对象类型的值

比如：

```auto
public class MyPluginServerCommand extends Command implements ICommandExecutableInServerSide {

    @Override
    public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
        JavaChildren javaChildren = new JavaChildren();
        javaChildren.setName("Zhang San");
        javaChildren.setAge(30);
        dataContext.getParameters().put("用户", javaChildren);
        return new ExecuteResult();
    }

    @Override
    public String toString() {
        return "我的服务端命令插件";
    }
}
auto
@Data
public class JavaChildren extends ObjectPropertyBase {

    private String name;

    private int age;
}
```

上面命令中，给上下文参数添加了一个key 为“用户” 的 javaChildren 对象。
当如果你在同一个插件的工程中获取当前上下文的 “用户” 参数的 value。可以直接获取到一个 javaChildren 对象。

```auto
public class MyPluginServerCommand3 extends Command implements ICommandExecutableInServerSide {

    @Override
    public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
        var javaChildren = (JavaChildren)dataContext.getParameters().get("用户");
        var executeResult = new ExecuteResult();
        executeResult.getReturnValues().put("Name", javaChildren.getName());
        return executeResult;
    }

    @Override
    public String toString() {
        return "我的服务端命令插件3";
    }
}
```

 如果是另一个插件工程中获取当前当前上下文的 “用户” 参数的 value。此工程中不存在 javaChildren 类。或者类结构和 javaChildren 不相同的时候。此时获取到的 value 是一个Map\<String,Object>。 其中key即为 javaChildren 各个属性的名称，value即为对应属性的值。
代码如下：

```auto
public class MyPluginServerCommand2 extends Command implements ICommandExecutableInServerSide {

    @Override
    public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
        var map = (Map<String,Object>)dataContext.getParameters().get("用户");
        var executeResult = new ExecuteResult();
        executeResult.getReturnValues().put("Name", map.get("name"));
        return executeResult;
    }

    @Override
    public String toString() {
        return "我的服务端命令插件2";
    }
}
```

* 传递 List 或 Array 之类的集合，统一会转成 list 类型。如果其中的元素为自定义对象类型。list 中的元素取值和 上数自定义对象类型一致。

---

## DatabaseInteraction

# 数据库交互

## Content

在服务端命令中，可以通过 IDataAccess 接口对数据库进行增删改查。
获取IDataAccess 的方法是 dataContext.getDataAccess()。
本例中使用的示例数据库如下：

#### 获取数据示例代码

参数为OData字符串。

```auto
public class MyPluginServerCommand extends Command implements ICommandExecutableInServerSide {

    @Override
    public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
        Object data = dataContext.getDataAccess().getTableData("学生表?$select=ID,姓名,年龄");
        ExecuteResult result =  new ExecuteResult();
        result.setMessage(data.toString());
        return result;
    }

    @Override
    public String toString() {
        return "我的服务端命令插件";
    }
}
```

效果如下：

#### 新增数据示例代码

```auto
public class MyPluginServerCommand extends Command implements ICommandExecutableInServerSide {

    @Override
    public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
        Map<String,Object> data = new HashMap<>();
        data.put("姓名","赵六");
        data.put("年龄","40");
        dataContext.getDataAccess().addTableData("学生表",data);
        return new ExecuteResult();
    }

    @Override
    public String toString() {
        return "我的服务端命令插件";
    }
}
```

执行结果如下：

#### 删除数据示例代码

```auto
public class MyPluginServerCommand extends Command implements ICommandExecutableInServerSide {

    @Override
    public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
        ColumnValuePair data = new ColumnValuePair();
        data.setColumnName("ID");
        data.setValue(2);
        dataContext.getDataAccess().deleteTableData("学生表",data);
        return new ExecuteResult();
    }

    @Override
    public String toString() {
        return "我的服务端命令插件";
    }
}
```

执行结果如下：