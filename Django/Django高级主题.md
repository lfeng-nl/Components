# Django高级主题

## 1.wsgi

> [参考](https://wsgi.readthedocs.io/en/latest/)
>
> wsgi: web服务器网管接口, 描述web服务器如何与web应用程序通信, application(*environ*, start_response); 
>
> environ: 服务器解析HTTP协议的一些信息, 如方法, path, 头部信息等;
>
> start_response: 回调函数, 将状态和头部信息传递给服务器;

- 通过`application = get_wsgi_application()`, 生成一个`WSGIHandler`的实例, 本身是一个可调用对象, 满足**wsgi**接口;
- `WSGIHandler`初始化时, 通过`.load_middleware()`加载中间件信息;
  - 通过`convert_exception_to_response()`包装所有的响应函数, 将抛出的异常转换为`response`;
  - 将`setting`中指定的中间件, 逆序导入;
  - 在`._middleware_chain`中记录最外层中间件, 最内层为`._get_response()`方法; 调用时会依次调用1. 当前中间件的`.process_request()`方法,  2.当前中间件`.get_response`属性中保存的内层中间件, 3.调用当前中间件的`.process_response()`方法;
  - `._get_response()`: 1.解析`request.path_info`, 得到回调视图, 回调参数, 2.调用回调, 得到`response`;
- 请求的响应过程: 1.整理url, 2. 根据`environ`实例化`WSGIRequest`对象,  3.调用`.get_response(request)`获取`response`

## 2.url解析

- 通过`settings.ROOT_URLCONF`定义的模块路径, 查找模块中的`urlpatterns`, 生成一个`URLResolver`对象;
- `urlpatterns`中的每一项的配置:
  - 每一个独立的路由配置都为`URLPattern`的实例:
    - 保存url, 回掉, 命名等信息;
    - 通过`RoutePattern.match`或`RegexPattern.match`匹配, 匹配出`new_path, args, kwargs`; 
    - `.resolve(path)`:  返回一个`ResolverMatch`实例, 实例中包含回调, 命名, 命名空间, 默认值, 匹配参数等信息;
  - 每一个`include`的路由配置保存为一个`URLResolver`的实例;
    - `.url_patterns`中保存所有被`include`进来的`URLRattern`实例;
    - `.resove(path)`: 匹配到include部分的url, 遍历匹配后续的url, 找到匹配的信息, 返回一个`ResolverMatch`实例;

## 3.Setting

### 1.设置的加载过程

- Django入口wsgi.py:

  ```python
  # 通过 DJANGO_SETTINGS_MODULE 环境变量控制设置文件路径
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_learen.settings') 
  application = get_wsgi_application()
  ```

- Django.wsgi.get_wsgi_applicaion()

  ```python
  # 在setup() 中, 配置log, app注册表
  django.setup(set_prefix=False)
  return WSGIHandler()
  ```

- django.conf.settings

  ```python
  settings = LazySettings()
  ### 说明 ###
  # 从settings中取配置值时会检查 _wrapped 属性是否存在, 不存在进行初始化, 
  # self._wrapped = Settings(settings_module)
  # 其中 settings_module = os.environ.get('DJANGO_SETTINGS_MODULE') 入口处配置的值
  # 所有的配置值存储为  _wrapped 属性的形式, 
  #　可以通过django.conf.settings.XXX 直接获取相应的配置值
  ```

### 2.指定settings文件

> 关键点在于修改 DJANGO_SETTINGS_MODULE 环境变量的值

## 3.ORM

### 1.关键类和对象

- `connections`: `setting`中配置的所有数据库连接.
- `QuerySet`: 表示一组数据的惰性的数据查找, 某些情况下会触发查询, 如(求长度, bool转换, 切片, 遍历, 取索引等等)
- `BaseIterable, ModelIterable, ValuesIterable, ValuesListIterable`: 为`QuerySet`提供不同维度的迭代方式.
- `Query`: 单个sql查询.
- `SQLCompiler`: 负责生成对应的sql语句, 执行sql.
  - `SQLInsertCompiler`:
  - `SQLDeleteCompiler`:
  - `SQLUpdateCompiler`:
  - `SQLAggregateCompiler`:
- `BaseDatabaseWrapper`: 代表数据的连接, 通过`connections`获取, 不用的数据库后端有具体的类实现.
- `Manager`:

### 2.`Manager`类

> Manager是为模型提供的数据库操作接口.
>
> 默认管理类,  Django会给每个Model添加一个名为`objects`的属性,  默认是`Manager`的实例;

- 类基于一个动态生成的基类`BaseManagerFromQuerySet`, 该基类基于`BaseManager`, 并继承`QuerySet`中的部分方法;

  - 继承`QuerySet`方法的方式:

    ```python
    # 将 manager_method 名称重命名, manager_method中通过get_queryset实例化一个QuerySet, 并调用其对应的方法
    def manager_method(self, *args, **kwargs):
        return getattr(self.get_queryset(), name)(*args, **kwargs)
    manager_method.__name__ = method.__name__
    manager_method.__doc__ = method.__doc__
    ```

- 在`ModelBase`元类中, 会为每个模型指定一个默认的`Manager()`, 用户也可以在定义模型的时候指定特殊的Manager(): `objects = PollManager()`

```python
class PollManager(models.Manager):
  def test(self):
    return super(PollManager,
      self).get_queryset().filter(status='published')

class Post(models.Model):
  objects = models.Manager() # 默认 Manager.
  published = PublishedManager() # 自定义 Manager

```

### 3.`QuerySet`类

> Represent a lazy database lookup for a set of objects
>
> 一组对象的惰性数据库查找

- `query`: 默认是`Query`的一个实例;
- `model`: 定义的模型类
- `_chain()`: 返回一个当前`QuerySet`的一个副本;
- `filter()`: 调用`_filter_or_exclude()`, 
  - `_filter_or_exclude()`: 1.获取一个当前`QuerySet`的副本, 2.调用副本的`.query.add_q()`
- `get()`: 先调用`filter()`获取一个`QuerySet`, 对当前的`QuerySet`判断数量(`len()`), 长度不为1, 抛出响应的异常;

- `as_manager()`: 返回一个Manager, 可以作为定制manager;

### 4.`Query`类

> 单个的sql查询

- `model`: 定义的模型类

### 5.`Q`类

> 将SQL表达式封装在Python对象中, 可用于数据库相关操作; 并将 `| &`重载

### 6.`Node`类

> 构造树的一个类, 用于ORM树行图的构造

### 7.注册过程

## 4.分页 *Paginator*

```python
from django.core.paginator import Paginator

def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True):
    pass
```

- 创建时传入需要分页的对象列表, 每页数量等信息.

- 在`View`中使用分页

  - 每次使用时, 需要先实例`Paginator`,再传入需要的页码, 进行返回;

  - ```python
    from django.core.paginator import Paginator
    def test_view(request):
        object_list = Object.objects.all()
        paginator = Paginator(object_list, 25) # 每页25个内容
        objects = paginator.get_page(request.GET['page']) # 获取指定页的内容
        pass
    ```

## 5.优化关联对象的查询

- `select_related()`

  - 直接查询关联外键, 再后续使用外键数据时不再查询数据库. 直接返回数据;

  - 实现方式是通过表连接, 使用方式仅限于, Foreign Key 和一对一的关系;

    ```python
    Entry.bojects.select_related('blog').get(id=5)
    Entry.objects.all().select_related('blog')
    Entry.objects.select_related('blog__blogFK').get(id=5) # 将blog相关指定外键也缓存
    ```

## 6.Channels

> 扩展Django, 使其可以处理WebSockets, 等

### 1.消费者

> 代码由一系列函数组成, 在事件发生时被调用.
>
> 允许编写异步代码.

- 同步`SyncConsumer`

    ```python
    from channels.consumer import SyncConsumer
    
    class EchoConsumer(SyncConsumer):
    
        def websocket_connect(self, event):
            self.send({
                "type": "websocket.accept",
            })
    
        def websocket_receive(self, event):
            self.send({
                "type": "websocket.send",
                "text": event["text"],
            })
    ```

- 异步`AsyncConsumer`

    ```python
    from channels.consumer import AsyncConsumer
    
    class EchoConsumer(AsyncConsumer):
    
        async def websocket_connect(self, event):
            await self.send({
                "type": "websocket.accept",
            })
    
        async def websocket_receive(self, event):
            await self.send({
                "type": "websocket.send",
                "text": event["text"],
            })
    ```

    

- `Http`异步消费者

    ```python
    from channels.generic.http import AsyncHttpConsumer
    
    class BasicHttpConsumer(AsyncHttpConsumer):
        async def handle(self, body):
            await asyncio.sleep(10)
            await self.send_response(200, b"Your response bytes", headers=[
                (b"Content-Type", b"text/plain"),
            ])
    ```

### 2.路由

- 根据协议(`ProtocolTypeRouter`)或者url(`URLRouter`)进行分发, 本身就是一个`ASGI`应用程序.

### 3.数据库访问

- Django ORM本身是同步, 只能在`SyncConsumer`中使用, 或者使用`channels.db.database_sync_to_async`中使用.

### 4.通道层

> 应用程序到应用程序的通信. 

- 原理:

    - 多个消费者实例的`.channel_layer`属性指向同一`channel_layer`.
    - `ChannelLayer`内部, 通过`groups, channels`给每一个消费者维护一个队列, 每个消费者有加入的`group`信息, 有`channels`信息. 通过该信息和`channel_layer`可以相互通信.
    
- 配置

    ```python
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("127.0.0.1", 6379)],
            },
        },
    }
    ```

    

## 7.部署

> 参考: [Django部署](https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/)

### 1.application对象

- 项目创建会生成`<project_name>/wsgi.py`, 用于生成`WSGI`部署.

### 2.Gunicorn

### 3.uWSGI

> **uWSGI做wsgi服务器, 通过socket域Nginx通信**: 
>
> ​	Web Client    <---->    Web Server(Nginx)    <--TCP/Unix socket-->  uWSGI  <----->  Django

- uwsgi协议: uWSGI服务器使用的本地协议, 二进制协议, 可以携带任何类型的数据.

- nginx上 uWSGI配置: `server unix:///unix/sock/;`
- uWSGI: `socket, xxx-socket` 通过socket连接到一个Web服务器之后;

>**uWSGI直接做Web服务器**:
>
>Web Client    <---->    uWSGI    <---->  Django

- uWSGI: `http`生成一个额外进程, 相当于Nginx的功能;  