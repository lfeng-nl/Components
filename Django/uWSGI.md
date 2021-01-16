# uWSGI

## 1.相关基础概念

### 1.WSGI协议

> WSGI: Python Web Server Gateway Interface, 为Python语言定义的**Web服务器**和**Web应用程序或框架**之间的一种简单而通用的接口规范`application(environ, start_response)`.
>
> WSGI服务器负责生成环境信息, 调用指定的接口app, 并传入`environ`环境信息, `start_response`回调对象, 并接受返回值
>
> [参考](https://www.python.org/dev/peps/pep-3333/)

- 应用程序必须接受两个位置参数;

  - `environ`: 字典对象, 包含 CGI 风格的环境变量, 还必须包含WSGI所需的环境变量;

  - `start_response(status, response_headers, exc_info=None)`: 接受两个参数的可调用对象, 用于发送响应头部信息.

    - `status`: 字符串, 响应状态;
    - `response_headers`: 格式为`[(head, head_value)]`, list 类型, 元素为包含头部和信息的`tupe`,
    - `exc_info`: 异常信息;
    - `start_response('200 OK', [('Content-Type', 'text/html')])`

- `application`必须返回一个可迭代对象, 产生 0 个或多个`byts`类型,

- python 中的简单测试

  ```python
  from wsgiref.simple_server import WSGIServer, WSGIRequestHandler

  def application(environ, start_response):
      status = '200 OK'
      response_headers = [('Content-type', 'text/plain')]
      start_response(status, response_headers)
      return [b'hello']

  # 配置服务器
  server = WSGIServer(('0.0.0.0', 80), WSGIRequestHandler)
  server.set_app(application)

  # 启动服务器, 当监听到连接时, 通过`_handle_request_noblock()`处理, 该函数内部通过 一系列调用, 最后会实例化RequestHandlerClass, ReqestHandlerClass初始化时会执行handle方法 对于WSGI, WSGIRequsestHandler().handle();
  server.server_forever()

    def handle(self):
        handler = ServerHandler(
            self.rfile, self.wfile, self.get_stderr(), self.get_environ())
        handler.request_handler = self      # backpointer for logging
        handler.run(self.server.get_app())
    
    def run(self, application):
        # 生成environ环境信息
        self.setup_environ()
        # 调用指定的application, 传入回调函数 start_response
        self.result = application(self.environ, self.start_response)
        # 处理返回,响应请求
        self.finish_response()
    
    # 接受status, headers, 将数据写入data (HTTTP协议的头部信息)
    def start_response(sefl, starus, handers):
      pass
  ```

### 2.uswgi

- 是uWSGI服务器独占的传输协议, 类似FastCGI

### 3.uWSGI

- 一个web服务, 实现了WSGI协议, uwsgi协议, http协议等;
- 接收请求后调用 WSGI Application , WSGI Application 处理后返回响应到 uWSGI, 类似中间件一样的角色;

## 2.架构

### 1.Nginx + uWSGI + Django

![](.\image\Nginx+uWSGI+Django.webp)

- Nginx: 做反向代理服务器, 负责静态资源处理, 动态请求转发以及结果的回复;
- uWSGI: 做Web服务器; 接收Nginx请求, 调用Django的 application;
- Django: 作为应用框架, 处理请求并相应结果;
- **Nginx和uWSGI之间通过socket连接(TCP/UNIX/HTTP)**

## 2.配置

> [参数参考](https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/Options.html)

- 格式: 支持ini, xml, yaml, json
- 参考配置项:
  - py-autoreload: 监控python模块mtine来触发重载(只可在开发时使用)

- 处理静态文件:
  - `check-static`:  指定目录中的静态文件;
  - `static-map` : 映射指定请求前缀到你的系统物理目录上;`static-map /images=/var/www/img`, 当收到`/images/logo.png` 的请求，并且 `/var/www/img/logo.png` 存在，会直接返回, 否则由应用接管;
  - `route`: 使用内部路由,可以构建复杂的映射关系;`route = /static/(.*)\.png static:/var/www/images/pngs/$1/highres.png`

## 3.uWSGI知识点



## 参考

[uWSGI-docs 文档](https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/index.html)

  ```

  ```