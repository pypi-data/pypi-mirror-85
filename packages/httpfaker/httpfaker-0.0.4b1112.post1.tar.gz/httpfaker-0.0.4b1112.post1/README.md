# http-faker

#### 介绍
**灵活又简单的mock服务**

gitee地址： https://gitee.com/guojongg/http-faker

httpfaker基于faker和flask库，提供强大的逻辑处理能力；通过对配置文件（yaml/json）的描述，可返回想要的任意数据。

httpfaker针对返回数据的规则编写灵活，简单。除了可以满足传统的接口mock外，还支持处理业务逻辑，可实现真正的业务功能。

适用于：
* 前端人员： 前后端分离开发，无需等到后台接口实现即可开始进行页面请求
* 测试人员： 提前进行接口测试代码编写；**服务未至，用例先行**
* 其他需要写一个简单api的人员： 通过yaml文件配置，可减少开发代码；无需关注请求处理部分，只需关注自己的业务逻辑即可。

#### 简单使用
```shell script
# 安装
pip install httpfaker

# 简单使用
httpfaker init
cd httpfaker-project
httpfaker 
```
![img003](https://gitee.com/guojongg/http-faker/raw/master/docs/image/img003.gif)


上面例子中使用`httpfaker init`预生成了一个[example.yml](apis/api_login_POST.yml)文件，yaml文件中描述了一个登录的场景：
1. 前端通过`post`方法调用`/api/login`这个地址，并在请求body中传来了`username`和`password`两个参数。
2. `httpfaker`接收到请求后会按照logic中描述的逻辑进行业务处理：先打印了请求参数，再按照`verify`中描述的，调用`verify_accont`方法，
来验证用户名和密码是否匹配，然后按照`token`中描述的调用`gen_token`方法，生成`token`。
（verify_account和gen_token方法已经注册到httpfaker调用函数中了，注册方法见[自定义方法的注册](docs/自定义方法使用说明.md)）
3. 在逻辑处理完成后，httpfaker按照`response`中描述的内容进行字段返回，`headers`中引用了在`env`中定义的
`content_type`; `body`中的`code、msg、data`等字段直接引用logic中已经生成的结果。

在上述流程中完成了用户登录到返回数据的一个完整流程，包含了业务处理部分，使mock服务不仅仅只是mock，还可以包括真实的业务逻辑。

#### 其它
* **http2api**: httpfaker支持录入接口数据，使用http2api，只需要在前端进行请求，可以自动将请求内容转换为httpfaker可读的模板。
* **swagger2api**: 支持将swagger格式的接口数据直接转换为httpfaker可读的模板。

#### 完整示例
[完整示例](apis/api_login_POST.yml)