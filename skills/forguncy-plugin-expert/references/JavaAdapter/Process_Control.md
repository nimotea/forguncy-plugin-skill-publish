# Process Control

## ProcessControl

# 流程控制

## Content

* [异常处理](/solutions/huozige/help/docs/java-adapter/java-server-command/process-control/Exception-handling)
* [支持返回结果](/solutions/huozige/help/docs/java-adapter/java-server-command/process-control/Support-return-results)
    * [结构类型的返回结果](/solutions/huozige/help/docs/java-adapter/java-server-command/process-control/Support-return-results/array-list)
* [服务端命令execute函数返回值](/solutions/huozige/help/docs/java-adapter/java-server-command/process-control/execute-return)

---

## ExceptionHandling

# 异常处理

## Content

服务端命令的核心处理函数为execute，默认的返回值为 ExecuteResult 类型。
约定规定，返回 execute.errCode 值为 0 表示成功，非 0 为失败。如果 errCode 为非 0 时，如果存在多种错误情况，插件开发者可以自行定义 errCode，以方便调试。

```auto
public class MyPluginServerCommand extends Command implements ICommandExecutableInServerSide {

    @Override
    public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
        int errorType = checkSomeThing();
        if(errorType == 1){
            return new ExecuteResult(1,"异常情况1发生了");
        }
        if(errorType == 2){
            return new ExecuteResult(2,"异常情况2发生了");
        }
        return  new ExecuteResult();
    }
    private int checkSomeThing() {
        return 0;
    }

    @Override
    public String toString() {
        return "我的服务端命令插件";
    }
}
```

如果execute抛出未处理的异常，活字格会自动把 errCode 设置为 500， message 设置为异常信息并生成日志。

---

## ExecuteReturn

# 服务端命令execute函数返回值

## Content

服务端命令的执行函数 execute 返回值类型为 ExecuteResult 对象。
如果执行成功，只需要返回默认的 ExecuteResult 对象即可。

```auto
public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
    return new ExecuteResult();
}
```

如果需要表示执行失败，应该设置返回的 ExecuteResult 对象的errCode属性为一个非 0 值。 同时推荐设置 message 属性说明失败原因。

```auto
public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
    return new ExecuteResult(1,"库存不足");
}
```

除了最常用的errCode属性和 message属性，在特定场景下可能需要设置其他 ExecuteResult 实例上的属性以满足不同的需求

#### 自定义响应（Response）内容

默认情况下，服务端命令执行的最终 ExecuteResult 会被写入到 HTTP 请求的 ResponseBody （响应） 中。如此，可以和前端的调用Http请求命令配合，完成前后端逻辑。
但是，有些情况下，服务端命令需要自己控制请求响应内容，此需求在与第三方系统集成时特别有用。通过设置 allowWriteResultToResponse 为 false 可以阻止活字格把 ExecuteResult 对象写入HTTP 响应。

```auto
public class MyPluginServerCommand extends Command implements ICommandExecutableInServerSide {

    @Override
    public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
        try {
            var response = dataContext.getContext().getResponse();
            response.setHeader("Content-Type","text/plain; charset=utf-8");
            response.getWriter().write("自定义响应内容");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        ExecuteResult result =  new ExecuteResult();
        result.setAllowWriteResultToResponse(false);
        return result;
    }

    @Override
    public String toString() {
        return "我的服务端命令插件";
    }

}
```

#### 流程控制

默认情况下，如果命令这些成功，会执命令列表中的下一个服务端命令。通过设置ExecuteResult的 processControl属性的值，可以控制命令列表的执行流程。

```auto
public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
    ExecuteResult result =  new ExecuteResult();
    result.setProcessControl(ProcessControl.Return);
    return result;
}
```

ProcessControl 可用选项如下表：

| 选项 | 说明 |
| --- | --- |
| Continue | 默认值，表示继续执行后续命令。 |
| Return | 立即返回，会跳过所有后续命令列表的执行。 |
| BreakLoopAndContinue | 如果当前命令是循环命令的子命令，跳出当前循环，继续执行循环命令之后的命令，类似于编程语言中的 break。 |
| ContinueLoop | 如果当前命令是循环命令的子命令，跳过此次循环的后续命令，继续执行下次循环，类似于编程语言中的 continue。 |

---

## SupportReturnResults

# 支持返回结果

## Content

命令执行后，可以把命令的执行结果保持到变量里，以便后续的命令或逻辑使用。
可以通过实现 @ResultToProperty 注解来实现此效果。
注意，标注 @ResultToProperty 的属性类型必须是 String. 推荐给属性添加默认值，以方便用户使用。
示例代码：

```auto
public class MyPluginServerCommand extends Command implements ICommandExecutableInServerSide {

    @FormulaProperty
    @DisplayName("加数1")
    private Object addNumber1;

    @FormulaProperty
    @DisplayName("加数2")
    private Object addNumber2;

    @ResultToProperty
    @DisplayName("相加结果")
    private String resultTo = "结果";

    @Override
    public ExecuteResult execute(IServerCommandExecuteContext dataContext) {
        double number1 = Double.parseDouble(addNumber1.toString());
        double number2 = Double.parseDouble(addNumber2.toString());
        dataContext.getParameters().put(resultTo,number1+number2);
        return  new ExecuteResult();
    }

    @Override
    public String toString() {
        return "我的服务端命令插件";
    }
}
```

设计器效果：

在后续命令编辑公式时，设置的变量可以直接在公式中使用。