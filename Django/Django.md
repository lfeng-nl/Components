# Django

## 1.基础概述

> Django的框架设计采用mvt模式，MTV模式：把Web应用分为：模型（Model），模板（Template），视图（view），对于Django，还有一个url分发器；
>
> ![MTV](https://images2015.cnblogs.com/blog/1086023/201704/1086023-20170407232851300-1237658304.png)
>
> （扩展：mvc，Model、View、Controller，它是用一种业务逻辑、数据与界面显示分离的方法来组织代码，将众多的业务逻辑聚集到一个部件里面，在需要改进和个性化定制界面及用户交互的同时，不需要重新编写业务逻辑，达到减少编码的时间）

### 1.文件定义

- `urls.py`：网址入口，关联到对应的`views.py`中的函数，访问网址就是对应一个函数；

- `views.py`：处理用户发出请求，从`urls.py`中对应过了，通过渲染`templates`中的网页将显示内容，返回用户，显示到页面上；

- `models.py`：数据库操作相关，存入或读取数据时用；

- `templates.py`：HTML模板文件，得到动态内容的网页；

- `admin.py`：后台；

- `settings.py`：Django的配置文件；

```
Django 项目结构
project_name
├──── manage.py
├──── project_name
|    ├──── __init__.py
|    ├──── settings.py
|    ├──── urls.py
|    └──── wsgi.py
|
└──── app_name
      ├──── __init__.py
      ├──── admin.py
      ├──── domels.py
      ├──── vews.py
      └──── templates
            ├──── xxxx.html
            └──── app_name
                  └──── xxxx.html
```

### 2.Django 基本命令

- `django-damin.py startproject project_name`：创建一个项目，会生成一个名为`project_name`的文件夹，
- `python manage.py startapp app_name`：在项目文件夹内运行，创建一个名为`app_name`的文件夹，
- `python manage.py makemigrations`：数据库
- `python manage.py migrate`：数据库
- `python manage.py runserver [port]`：开发服务器，仅用于开发、测试、调试用；
- `python manage.py shell`：`Django`项目环境终端；
- `python manage.py collectstatic`: 收集静态文件到`STATIC_ROOT`配置的文件路径中;
- 更多详细介绍可参考：[`django-admin` and `manage.py`](https://docs.djangoproject.com/en/1.11/ref/django-admin/)

## 2.视图和URL

> Dgango处理访问的过程：ROOT_URLCONF确定url文件路径 ---> 查找匹配到的url --> 查找对应的view函数 --> 将HttpRequest 作为第一个参数（还可以将URL中匹配的参数传入：r'/test/(\d)/(\d)/$' ，匹配两个数字作为参数）

### 1. [URL](https://docs.djangoproject.com/en/2.2/topics/http/urls/)

- 由`settings.ROOT_URLCONF`配置根`URLconf`模块;

- Django 加载模块中的`urlpatterns`变量;

- Django会根据加载的`urlpatterns`, 遍历匹配, 找到第一个匹配到的信息;

- 匹配到URL之后，Django导入并调用给定的视图；

  - 视图函数参数：1.HttpRequest实例，2.正则表达式中匹配的参数；

  ```python
  # 路径转换器
  path('abc/<int:year>/', views.year)
  # str 匹配除分隔符'/'之外的任何非空字符串
  # int 匹配零和正整数
  # slug 匹配ASCII字母或数字组成的任何slug字符, 以及连字符和下划线;
  # uuid 匹配格式化的uuid
  # path 匹配任何非空字符串, 包括路径分隔符'/'
  
  # 正则匹配
  re_path(r'^abc/(?P<year>[0-9]{4}/$)', views.year)
  ```

- `include('appName.urls')`
    - 包含其他模块;
    - 匹配时会除去已匹配到的前缀, 遍历`include`的模块, 进行匹配;
- 传递额外参数:
  
    - `urlpatterns = [re_path(r'^blog/(?P<year>[0-9]{4})/$', views.year_archive, {'foo': 'bar'}),]`

### 2.[视图views](https://www.cnblogs.com/huchong/p/7718393.html)

>   视图函数，简称视图，是一个简单的Python 函数，它接受Web请求并且返回Web响应。响应可以是一张网页的HTML内容，一个重定向，一个404错误，一个XML文档，或者一张图片. . . 
>
>   视图函数，围绕两个对象进行：HttpRequest，HttpResponse;

#### 1.`HttpRequest` 和 `HttpResponse`

> - 每一个视图函数会接受一个`HttpRequest`类的实例作为第一个参数，名为`request`
> - 每一个视图函数会返回一个`HttpResponse`类的实例

- **`HttpRequest `**:  由框架生成, 对用户请求的封装; [参考](<https://docs.djangoproject.com/en/2.2/ref/request-response/#django.http.HttpRequest>)
-   `HttpRequest.body`：请求体；
    -   `HttpRequest.method`：请求方式;
    -   `HttpRequest.COOKIES`：包含所有cookies的字典；
    
- **`HttpResponse`** : 响应, 视图函数负责生成 [参考](<https://docs.djangoproject.com/en/2.2/ref/request-response/#django.http.HttpResponse>)
- `HttpResponst.set_cookie()`：添加cookie；
    - `HttpResponse.delete_cookie()`：删除相应cookie;
- 另外有: `JsonResponse, FileResponse, HttpResponseRedirect`等派生类型;

- 返回错误状态码:
    - 直接设置状态码，从而达到返回错误的目的：`return HttpResponse(status=404)`
    - 或者直接错误派生类: `HttpResponseNotFound`

#### 2.文件上传

- Django文件上传是通过`request.FILES`;

- ```python
  f = request.FILES['file']
  with open('file_name', 'wb') as destination:
      for chunk in f.chunks():
          destination.write(chunk)
  ```

- 当上传文件小于2.5M时，会存放内存中，可以直接读取，当太大时，会存放于`tmp`目录；

- ``FILE_UPLOAD_HANDLERS`定义文件上传的处理行为；默认：

  - ```python
    [
        'django.core.files.uploadhandler.MemoryFileUploadHandler',
        'django.core.files.uploadhandler.TemporaryFileUploadHandler',
    ]
    ```


#### 3.视图函数装饰器

> `django.views.decorators`

- `require_http_methods(['GET', 'POST'])`: 设置允许的请求方式;
- `condition(etag_func, last_modified_func)`: 控制特定视图的协商缓存行为; 制定函数生成`ETag`和`Last-Modified`头部信息;
- `gzip_page`: 如果浏览器允许, 会压缩内容;
- `cache_control()`: 强制缓存;
- `never_cache()`: 禁用缓存;

#### 6.[中间件 Middleware](https://docs.djangoproject.com/en/1.11/topics/http/middleware/)

> 1.在http**请求 到达视图函数之前** ； 2.视图函数**return 之后**，django会根据自己的规则在合适的时机执行中间件中的响应方法。

![](https://images2015.cnblogs.com/blog/1122865/201707/1122865-20170702160228602-1675492679.png)

- 自定义中间件：

  - 一般写法比较固定，可以写成函数形式，也可以写成类的实例调用，可以放在任何python文件中；

  - 函数形式：

    ```python
    def simple_middleware(get_response):
        def middleware(request):
            #在每一个请求前执行
            ...
            #在每一个请求前执行
            response = get_response(request)  # --> 可能代表视图函数，也可能是下一个中间件
            #在每一个响应后执行
            ...
            #在每一个响应后执行
            return response
        return middleware
    ```

  - 类形式：

    ```python
    class SimpleMiddleware(object):
        def __init__(self, get_response):
            self.get_response = get_response
    
        def __call__(self, request):
            #在每一个请求前执行
            ...
            #在每一个请求前执行
            response = self.get_response(request)
            #在每一个响应后执行
            ...
            #在每一个响应后执行
            return response
    ```

- 中间件的使用：

  - 1.加入setting，`MIDDLEWARE `列表；
  - 2.在view函数执行前后调用；

### 3.类视图

#### 1.简介

>   `.as_view()`: 返回一个内部定义的函数, 该函数的作用: 
>
>   1.  创建视图类的实例;
>   2.  将传入函数的`request, *args, **kwargs`设置为实例的属性;
>   3.  调用实例的`dispatch()`方法, 根据请求方式, 调度相应的方法;

- 所有类视图应继承于`View`类，并提供请求方法的对应处理函数，通过`as_view()`, 绑定到url；

  ```python
  from django.views import View
  
  class MyView(View):
      # 响应GET请求
      def get(self, request):
          return HttpPesponse('xx')
      
  url(r'xx', MyView.as_view())
  ```

- **混入 `Mixins`**

  - 多重继承, 用于组合父类的行为和属性;

- 装饰器:

  - 类上的方法和独立函数并不完全相同, 因此不能只将函数装饰器应用于该方法, **需要先将其转换为方法装饰器**;
  - `@method_decorator(装饰器名, name='方法名')`:  用于装饰类, 指定**装饰器名**和需要装饰的**方法名**;
  - `@method_decorator(装饰器名)`:  省略掉参数, 直接装饰方法;

### 4.模板

- 模板引擎：Django默认模板引擎，DTL；比较火的模板引擎：`Jinja2`

#### 1.Template对象

- 生成模板对象：`get_template(template_name, using=None), select_template(*template_name_list*, *using=None* ` ：返回`Template`对象，using，使用的模板引擎；
  - `Template.render(context=None, request=None)`：context 字典形式的上下文信息，request --HttpRequest对象；返回解析后的字符串；
- Django还提供了一些简化函数：
  - `reder_to_string(template_name, context=None, request=None, ...)`：直接获取模板文件，解析，返回字符串；

#### 2.Django模板相关设置

- 模板文件的查找：

    -   `DIRS` ：定义模板的查找路径；
    -   `APP_DIRS` ：模板引擎是否会去每个app下查找模板；
    -   模板引擎会优先搜索`DIRS`目录下的文件，未找到再搜索每个app下的模板文件；
    -   各app下的模板文件等效，会统一查找；
    -   若需要某个应用独占的模板，可用文件夹区分，但是视图函数中**要写明路径**，`'blog/home.html'`

#### 3.模板语法

> 主要有：变量，标签，过滤器

- 变量：`{{ various }} `

    -   通过句点查找`. `，模版系统可调用传入参数的：属性，方法（不能传参），列表索引，字典。
    -   如果变量不存在，模版系统会把它展示为空字符串，不做任何事情来表示失败。

- 标 签：`{% xx %} `，如for，if

    - if/else，允许 and, or,  not 关键字对多个变量做判断，不支持圆括号进行组合，所以同一个标签中只能使用其中一个。

        ```html
        {#  if..elif..else..endif 语句 #}
        {% if condition1 %}
        	expression1
        {% elif condition2 %}
        	expression2
        {% else %}
        	expression3
        {% endif %}
        ```

    - for，允许我们在序列上迭代，使用 `reversed `可反向迭代，

        ```html
        {#  for 语句 #}
        {% for items in list %｝
        ...
        {% endfor %}

        {% for x in x_list reversed %}
        ...
        {% endfor %}
        ```

    - for支持 `% empty %}` 标签，通过它可以定义当列表为空时的输出内容，

        ```html
        {% for x in x_list %}
        ...
        {% empty %}
        x_list为空时输出的内容
        {% endfor %}
        ```

    - ` forloop.counter` ：循环计数器变量，表示当前循环执行次数；

    - `forloop.revcounter `：循环剩余；

    - `forloop.last `： 最后一次循环；

    - ... 还有很多，可参考官方文档；

- **模板中的条件`{% if var %}`判断** ：

    -   1.根据视图中返回的数据的`bool`值进行判断；
    -   2.当指定变量`var`不存在时，给果为false；
    -   3.特别注意：对于字符串、列表、字典等数据类型，当数据为空时`bool`值为`False`；

- 变量`{{ var }}`插入位置：

    -   当`{{ var }}`插入js脚本时可能会产生问题；（特殊符号会用特殊标记进行替换）；
    -   

- `{% ifequal var1 var2%}`： 如果相等，显示中间的值。等价于`{% if var1 == var2 %}`

- 过滤器：使用管道符号`| `来应用过滤器，用于进行计算，转换操作；

- 模版注释：`{#....#} ` 不能跨越多行；注意，html注释不能注释模版语言；

- 跨行注释：使用` {% comment %}`标签；

- 动态url：`<a href="{% url 'namespace:url_name' %}">xxx</a> `

- 过滤器：`{{ name|lower }}`, 通过管道符号连接，将变量输入到后续的过滤器中进行处理；

- 模板继承：[官方文档](https://docs.djangoproject.com/en/1.11/ref/templates/language/#template-inheritance)

    -   首先编写被继承的`base.html `文件；

        ```html
        <html>
            <head>
            </head>
            <body>
                <!-- 需要继承者改变或填充的部分(可以有多处) -->
                {% block xx_name %}
                <!-- 可以添加写默认的内容 -->
                {% endblock %}
            </body>
        </html>
        ```

    -   继承者继承`base.html `：

        ```html
        <!-- extends 标记需要继承的模板  -->
        {% extends "base.html" %}   <!-- 注意继承文件路径问题 -->

        {% block xx_name %}
        <!-- 写入填充内容 -->
        ....
        {% endblock %}
        ```

    -   使用继承的常见方式：

        -   1.创建`base.html `模板，在其中定义站点的主要外观感受，
        -   2.为网站的每个区域创建`base_SECTION.html `模板，（例如，`base_photos.html`，`base_form.html `）包含区域特定风格与设计。
        -   3.为每种类型的页面创建独立的模板；

- `include `：可以将每个网页都公用的小功能打包为html，然后使用时`include `该文件；

    ```html
    {% include "xxx.html" %}
    ```


### 5.自定义模板标签

> 模板标签本质上就是一个 Python 函数，因此按照 Python 函数的思路来编写模板标签的代码就可以了.

- 实现步骤：

  - 在app目录下，创建`templatetags `文件夹，并创建`__init__.py `文件，使之成为一个包；

  - 实例化一个`template.Library `,

    ```python 
    from django import template

    register = template.Library()
    ```

  - 定义一个模板标签函数，并用`register.simple_tag`修饰；

    ```python
    @register.simple_tag
    def get_tags():
        rerurn Tag.objects.all()
    ```

  - 使用前，导入自定义模板标签文件，`{% load file_name %} `;

## 3.[Model](https://docs.djangoproject.com/en/1.11/topics/db/models/)

> Model是信息和数据的唯一来源，它包含所存储数据的基本字段和行为，通常，每个模型映射到一个数据库表；
>
> ORM：Object Relational Mapping(关系对象映射)，用类来操作数据库中的表，类名 <--->数据库中的表名，类的属性 <--->表中的字段，类的实例化对象 <--->表中的一行数据；
>
> Django的 ORM 操作本质上会根据对接的数据库引擎，翻译成对应的sql语句；所有使用Django开发的项目无需关心程序底层使用的是MySQL、Oracle、sqlite....，如果数据库迁移，只需要更换Django的数据库引擎即可；
>
> Django的模型需要依附具体的app，并把app添加到设置中的INSTALLED_APPS中；

### 1.数据库后端

`Django `默认使用`sqlite3 `，使用`MySQL `等其他数据库需要进行配置；

- 设置`settings.py `，设置的中数据库名称在数据库中必须已经存在；

  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'db_name',    # 数据库名称
          'USER':'root',        # mysql 用户名
          'PASSWORD':'psw',     # mysql 密码
          'HOST':'',            # 数据库主机地址
          'PORT':'3306',        # 端口
      }
  }
  ```

- 编辑`appname/models.py `内容；创建`model `类相当于数据库中的表，会在数据库中生成名为：`appname_classname `的表；创建的类必须继承`models.Model `；

  -   ```python
      rom django.db import models

      class Person(models.Model):
          first_name = models.CharField(max_length=30)
          last_name = models.CharField(max_length=30)
      ```

- 执行：`python manage.py makemigrations `和`python manage.py migrate `：

  -   `python mange.py check`：可以检查模型的语法和逻辑是否正确；
  -   `python manage.py makemigrations `：在相应app下建立`migrations `目录，并记录你所有的关于`modes.py `的改动；
  -   `python manage.py migrate `：作用到数据库，产生对应的表；
      -   多数据库时: 可以通过`--databases db_name`指定数据库配置, 默认使用`default`;
  -   默认作用全局，如果仅想作用于某个app，需要加上`appname`

- 详细配置单个APP的数据：在`settings.py `中，除了`default `配置，还可以按照 app 来单独配置某个app所使用的数据库。

### 2.定义model

#### 1.字段

> 字段对应数据的一列, 可以确定数据库类类型, 和数据验证

- 普通字段:
  - `BooleanField()`：布尔型字段，
  - `CharField()`：字符型字段，该字段类型有一个必需参数：max_length  在数据库水平限定了字符串最大长度;
  - `IntegerField()` ： 整形字段；
  - `FloatField()` ：浮点数；
  - `TextField()` ：与`CharField`类似，但一般用来存储体积较大的文本；
  - `EmailField()` ：特殊的`CharField`，检查值是否为有效电子邮件；
  - `FilePathField()`: 择仅限于文件系统上某个目录中的文件名;
  - `GenericIPAddressField()`: IPv4或IPv6地址;
  - `UUIDField()`: uuid, 存储通用唯一标识符的字段. `default=uuid.uuid4`;  
  - `FileField(upload_to='')`: 文件上传字段, 数据库中为字符类型,
    - `upload_to='uploads/'`: 上载目录,  会存放到`MEDIA_ROOT/uploads`;
    - `storage`: 存储对象, 用于文件存储和检索, 
    - 访问字段时, 会得到一个`FieldFile`代理实例, 可以得到以下API:
      - `name`: 包括根的相对路径的文件名, 数据库存储, 指定的**上载目录**加保存时指定的**文件名**;
      - `url`: 访问文件的相对url;
      - `save(name, content, save=True)`: content为`django.core.files.File`的实例; 
- 关系字段:
  - `ForeignKey(to, on_delete)`:  多对一;
  - `ManyToManyField(to, **options)`: 多对多, 数据库会建立一个中间连接表来表示多对多关系;

#### 2.字段参数

- 普通字段参数:
  - `null ` ：默认`False `, 对应数据库`NOT NULL`，`True`表示数据库该字段可以为空, 为空时, 值为`None`;
  
  - `blank `：默认`False `，主要针对表单验证, ,例如字符串, 当为空时, 值为`''`;

  - `choices ` ：可以提供备选数据，带有`choices `选项的字段中保存了两部分信息，一个为value一个为display_name, Django会为该字段提供一个`get_字段名_display()`的方法, 获取对应的display_name值;
  
      ```python
       class Person(models.Model):
          GENDER_CHOICES = (
              ('M', 'Male'),
              ('F', 'Female'),
          )
          gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
          
          
      >>> p = Person(name="Fred Flinstone", gender="M")
      >>> p.save()
      >>> p.gender
      'M'
      >>> p.get_gender_display()
    'Male'
    ```
  
  - `db_column `：显式指定该字段数据库column的名称；
  
  - `db_index `：如果为`True`，为该字段创建索引；
  
  - `default `： 默认值；不会反应到数据库上；
  
  - `primary_key `：  若设置为`True`，则表示将该字段设置为主键。一般情况下django默认会设置一个自增长的id主键；
    
  - `unique `： 默认`False`,  `True`表示该字段不可重复； 
  
  - `validators`:  该字段运行的验证程序列表; `validators=[validate_even]`;
  
- 关系字段参数:

  - `on_delete ` ：当关联的字段被删除时，对象应该采取的操作；有以下值可选：
        -   `models.CASCADE `: 级联删除;
        -   `modles.PROTECT ` :  当删除一个具有外键关系的对象时，会引发一个异常，阻止删除该对象；
        -   `models.SET_NULL `: 设置删除对象所关联的外键字段为`null`。但字段的null属性必需为True
        -   `models.SET_DEFAULT `:  设置删除对象所关联的外键字段为默认的值。
         -   `models.SET(value) `: 设置删除对象所关联的对象的外键字段为`value `, `value `也可以是一个可调用函数。

  - `to_field `：  设置所关联对象的关联字段。默认为关联对象的主键字段。

  - ` related_name` ：关联对象反向引用的描述符;  设置为`+`表示模型不具有向后关系;

      > **注意**: 当模型类被继承时, `related_name`应当使用`'%(class)s'`的形式命名;

      - 可以有多个不同的种类同时指出反向引用名；
  
          ```python
          class A(models.Model):
              user = models.ForeignKey(User, related_name='as')
              
           class B(models.Model):
            user = models.ForeignKey(User, related_name='bs')   
          ```
  
  - `related_query_name`: 反向过滤器名称, 默认为`related_name`值;
  
      > `default_related_name`: 默认反向查找名称, 默认值为`<model_name> _set`
  
  - `db_table`：用于明确指明中间表的名称，否则，中间表名称由系统自动生成，一般为相关联表的名称的组合；
  
  - `db_constraint`: 控制是否应在数据库中为此外键创建约束, 默认`True`,

#### 3.Meta,继承,代理

- Meta: 为model提供元数据信息
  - `abstract`：该模型为抽象基类，用于继承；
  - `app_label`: 所属的app, app外定义时需指定;
  - `db_table`：用于定义数据库表的名字（默认是按照app_name和类名生成）；
  - `ordering`：获取的对象列表的默认排序，`ordering = ['-create_time']`，按某一字段进行排序；
  - `permissions`：自定义权限，`permissions = ( ("view_task", "Can sese available tasks"), )`
  - `indexes`: 要在模型上定义的索引列表, `indexes=[models.Index(fields=['xxx', 'xxxx'], models.Index(fields=['xxx']))]`;
  - `managed`: Django来管理表的生命周期.

- 代理:
  - Meta中, 设置`proxy = True`, 在python层面提供额外选项和功能.例如某些字段的拼接, 排序等等.

- 继承:
  - Meta中, 设置`abstract`将父类模型设置为抽象.

#### 4.重写或定义方法

- 重新定义预定义方法

  ```python
  def delete(self, *args, **kwargs):
    do_something()
    # 调用父类方法;
    super(Blog, self).delete(*args, **kwargs)
    do_something_else()
  ```

- 也可以在模型类中定义自定义的方法, 存放特殊的业务逻辑;

### 3.Model操作

#### 1.创建

```python
# 方法 1
Author.objects.create(name="WeizhongTu", email="tuweizhong@163.com")

# 方法 2
twz = Author(name="WeizhongTu", email="tuweizhong@163.com")
twz.save()

# 方法 3
twz = Author()
twz.name="WeizhongTu"
twz.email="tuweizhong@163.com"
twz.save()

# 方法 4，首先尝试获取，不存在就创建，可以防止重复
Author.objects.get_or_create(name="WeizhongTu", email="tuweizhong@163.com")
# 返回值(object, True/False), 存在未创建为False，不存在创建为True
```

- `save(force_insert=False, force_update=False, using=DEFAULT_DB_ALIAS, update_fields=None)`
  - `update_fields=['xxx']`:  指定更新字段，可以避免缓存造成影响，也可提高效率;

- 更新关系字段：
  - `ForeignKey`：直接赋值；
  - `ManyToManyField`：使用`add()`方法，可同时添加多个，如`add(a1, a2, a3)`;

#### 2.检索

- `QuerySet`: 数据库中的对象集合;
- 返回字典或元组形式的API
  - `values(), values_list()`
- 并,交,差集: 注意, 某些数据库引擎不支持
  - `uniton(), intersection(), difference()`
- 查询优化api:
  - `select_related(), 多对一查询优化, prefetch_related()多对多查询优化`

```python
# 查询所有对象
Author.objects.all()

# 查询单个对象, 不存在抛出 DoesNotExist 异常, 多个抛出 MultipleObjectsReturned 异常
Author.objects.get(name='WeizhongTu')

# fileter过滤器，返回符合要求的 QuerySet 类型对象; exclude为反向过滤器；
# ！！当查找失败时，返回为空的QuerySet
Author.objects.filter(name="abc")
Author.objects.exclude(name="abc")

# 其他字段查询关键字：in, gt(大于)， gt(大于)， gte(大于等于)， lt(小于)，lte(小于等于)
# 类似 LIKE 的语句: iexact, contains, icontains, startswith, istartswith, endswith, iendswith
Author.objects.filter(name__iexact="abc") # xx__iexact，不区分大小写
Author.objects.filter(name__contains="abc") # xx__contains,包含 "abc"
Author.objects.filter(name__icontains="abc") # xx__icontains, 包含，且不区分大小写
Author.objects.filter(id__in=[1,2,3]) # 在给定范围

# QuerySet 支持链式查询
Author.objects.filter(name__contains="Wei").exclude(email="tuweizhong@163.com")

# QuerySet 排序, 需要排序字段前加一个 - 号，表示逆序排序，
Author.objects.all().order_by('name')
Author.objects.all().order_by('-name')
```

#### 3.QuerySet 高阶用法

```python
# values获取字典形似结果， values_list 获取元祖形似的结果
Author.object.values('name', 'email')  # 返回由{'name':xx, 'email':xx} 组成的QuerySet
Author.object.values_list('name', 'email')  # 返回由(xxx, xxx)组成的QuerySet

# annotate (注释，对QuerySet中的每个元素添加额外信息， 借助Sum、Count、Avg，按某一项区分求另一项统计信息)

# select_related 优化外键查询（一对多），查询时也将额外的关联信息一并查询，当后面使用外键关系时不会再次进行查询
a = Article.object.all().select_related('author')[0]

# prefetch_related 优化一对多，多对多查询，同sleect_related查询方式会有区别
a = Artilcle.object.all().prefetch_related('tags')[0]

# defer 排除不需要的字段，不进行查询，当后续再使用时会自动查询
a = Atricle.object.all().defer('title')[0]  # --> 查询时不包含 ‘title’ 字段
a.title                                     # --> 单独查询‘title’字段

# iexact, contains, icontains, startswith, istartswith, endswith, iendswith
Entyr.objects.filter(headline__contains="%")

# F查询和Q查询 form django.db.models import F, Q
# F 允许Django在未实际获取到值的情况下具有对数据库字段的值的引用

#对图书馆里的每一本书的价格 上调1块钱
Book.objects.all().update(price=F('price')+1)

book = Book.objects.get(id=1)
book.price = F('price') + 1
book.save()

# Q 对象, 可以将多个条件通过（&、|、~）进行组合, 组成复杂过滤条件；
Atricle.object.fifter(Q(查询条件1)| Q(查询条件2))
```

#### 4 .其他

- 删除: `delete()`, 可以对单个对象调用, 也可对`QuerySet`调用, 对`QuerySet`调用不会调用单个类的`delete()`方法;

  - 对于外键或多对多关系, 会受指定的`on_delete`参数影响;
  
- 复制：当需要复制某个model实例的时候，只需要将`id/pk (主键)`置为`None`

  ```python
  blog = Blog(name='My blog', tagline='Blogging is easy')
  blog.save() # blog.pk == 1
  
  blog.pk = None
  blog.save() # blog.pk == 2
  ```

- 批量更新：`update(key=value)`，会直接转为`SQL`语句,  不会调用类的`save()`方法;

- 关系字段的附带方法：

  - 多对多的关系字段自带：`add(), count(), all(), romove(), `等方法；

### 4.[Transaction管理（事务管理）](https://docs.djangoproject.com/en/1.11/topics/db/transactions/)

> 数据库事务：指作为单个逻辑工作单元执行的一系列操作，要么完全的执行，要么完全的不执行；事务是数据库运行中的逻辑工作单位；

- Django默认自动提交, 如果不处于事务中, 每个查询都会立即提交到数据库;
- Web事务常用的是整个请求包装在事务中,  通过设置`ATOMIC_REQUESTS`, 调用视图会进入事务, 如果产生异常, 将进行回滚；
- 块级的事务处理`atomic`：
  - `@transaction.atomic`：装饰器，作用于函数；
  - 或者 `with transaction.atomic()`：作用于代码块；
- 取消view函数的事务处理`@transaction.non_atomic_requests`：
- Django事务原理:
  - 1.在最外面的原子块打开事务;
  - 2.在内部原子块创建保存点;
  - 3.退出内部原子块时释放或回滚到保存点;
  - 4.退出最外面的块时提交或回滚事务;

- `on_commit()`事务提交完成后执行回调;
  - `transaction.on_commit(cb_func)`
  - 只有整个事务完成才会触发回调, 内部`savepoint`不会触发回调;
  - 当回滚到内部保存点, 内部原子块内的提交回调在整个事务完成时也不会被调用;
  - 如果`on_commit()`中注册的函数触发了异常, 则后续的函数将不会被执行;

### 5.聚合函数

> 对一组值执行计算，并返回单个值；
>
> Django通过对QuserySet类型执行聚合（.aggreate()）函数；返回字典类型；

- `Avg( )`：求平均，Book.objects.all( ).aggregate(Avg('price'))，也可以指定返回字典的键的名字：`Book.objects.aggregate(min=Min('price'))`
- `Max( )`：求最大值；
- `annotate()`:Join，

### 6.存取优化

> 可以通过`.explain()`查看`QuerySet`的执行计划
>
> 或使用django-debug-toolbar等工具, 监视数据库

- 使用数据库优化技术:

  - 索引: 确定哪些字段需要添加索引, 使用`Meta.indexex`或`Field.db_index`添加;
  - 使用适当的字段类型;
  
- 理解`QuerySets`；

  - `QuerySets`是惰性的, 创建`QuerySet`的行为不涉及任何数据库活动, 只有**评估(evaluated)**时, 才会执行数据库操作;
  - `QuerySet` 的评估：只有评估发生, Django才会实际操作数据库; 触发评估的方式有:
    - 迭代: 会在第一次迭代时执行其数据库查询;
    - 分片:
    - 序列化或缓存: 序列化或缓存数据时会触发评估;
    - 对`QuerySet`执行一些转换函数: 1.`repr()`, 所以在交互式终端中, 都是立刻执行; 2.`len()`, Django推荐使用`.count()`方法, 会使用数据库级别的优;  3.`list()`, 4.`bool()`, 如果只想确定是否存在至少一个结果可以使用`.exists()`方法 ;
  - `QuerySet`的缓存: 每个`QuerySet`包含一个缓存, 以减少对数据库的访问; 当期被评估时就会缓存查询结果, 查询`QuerySet`的部分结果时不会生成缓存信息;

- 检索的尽可能精确: 使用`filter, exclude`过滤;

- 使用`QuerySet.update()`和`QuerySet.delete()`: 尽可能进行批量删除个更新, 但是**注意!! 批量更新和删除不会调用单个实例的save()和delete()方法**

- 大量创建模型时使用：

  ```python
  Entry.objects.bulk_create([
      Entery(headline='xx'),
      Entery(headline='xxxx'),
  ])
  ```

- 直接只用外键的值：对于id，会生成 `name_id`的属性直接保存在模型中，所以直接拿id会比查询快；

  ```python
  entry.blog_id  #好于 entry.blog.id
  ```

### 7.多数据库和数据库路由

> 每个设定的数据库中均保存有所有的数据结构信息;  default数据库是所有默认使用数据库,  可以通过数据库路由分配具体使用数据库;

- 定义:
  - 在`DATABASES`设置中, 除`default`外, 还可定义需要使用的数据库信息, 名称可以用于`manager.py migrate --database=xxx`, 将每个应用程序模型同步到指定数据库; 未指定则使用`default`;

- 数据库路由就是提供了以下方法的类:
  - `db_for_read(model, **hints)`: 应当用于读取操作的数据库, 返回设置中配置的数据库名或None(None使用默认);
  - `db_for_write(model, **hints)`: 应当用于写操作的数据库, 返回设置中配置的数据库名或None(None使用默认);
  - `allow_relation(obj1, obj2, **hints)`: 验证操作, 两个对象之间是否应该允许关系, 默认之允许同一数据库内的关系;
  - `allow_migrate(db, app_label, model_name=None, **hints)`:  `makemigrations`总是创建模型的变化迁移, 但是如果`allow_migrate`返回`False`, 将跳过对`model_name`的`migrate`操作;

- 在设置中使用`DATABASE_ROUTERS`设置数据库路由;
- 手动使用数据库:
  - `xxx.objects.using('xx').all()`: 使用指定数据库;
  - `xxx.objects.save(using='xxx')`: 保存到指定数据库;yun
- Django目前不提供跨越多个数据库的外键或多对多关系, 因为需要评估主键的有效性; 数据库级别也会因为键的约束阻止数据插入;

### 8.其他

- Managers: 为Django模型提供数据库查询操作的接口,  默认名为`objects`;
  - 重命名: 通过定义属性`xxx=models.Manager()`, 重命名`objects`;
  - 定制: 1.定义继承`Manager`的类, 2.定义属性, 类型为自定义的Manager类型;
- 执行原生SQL
  - `Manager.raw('raw sql')`:
- 迁移:

## 4.处理HTTP请求

### 1.使用会话 sessions

> session 信息存储在服务端，由 cookies 或其他方式携带session ID， 
>
> Django中 session 是以中间件`SessionMiddleware`的形式实现；

- 配置session引擎:
  - `SESSION_ENGINE`: 配置session引擎, 有`db, file, cache, cache_db, signed_cookies`; 引擎不同, session的存储方式不同, 默认是db存储;
- Django在中间件`SessionMiddleware`中处理session, 根据`session_key`和过期时间查询到当前`session`数据;
- 在视图中，可以同过`request.session` 读取或改写 session值；类型为：`django.contrib.sessions.backends.db.SessionStore`
- 通过[`SESSION_EXPIRE_AT_BROWSER_CLOSE`](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-SESSION_EXPIRE_AT_BROWSER_CLOSE) ,设置会话保持时间;
- 在views中使用session: `request.session`
  - `setdefault()`:  若值不存在, 设置值;
  - `items()`: 返回所有的键值对;
  - `keys()`: 返回所有key;
  - `get()`: 返回指定key的值;
  - `pop()`: 抛出指定key;
  - `cycle_key()`: 更新会话秘钥;
  - `set_expiry(value)`: 设置会话到期时间;

### 2.文件服务器

- `MEDIA_ROOT`和`MEDIA_URL`:
- 模型中使用文件:
  - `ImageField`:
  - `FileField`:
- `File`对象: 文件实例;
  - 对打开文件`TextIOWrapper`的封装;
- `FileSystemStorage(location, base_url)`: 文件存储类
  - `location`: 保存文件的绝对路径. 默认是`MEDIA_ROOT`;
  - `base_url`: 提供此位置的文件url, 默认是`MEDIA_RUL`;
  - 提供: `save(), delete(), open(), exists()`等方法;

### 3.缓存

- Django可以使用基于Memcached, 数据库, 文件系统缓存, 本地内存缓存;

- 配置:

  - ```python
      CACHES = {
          'default': {
              # memcached 配置
              'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
              'LOCATION': '127.0.0.1:11211',
              # 数据库缓存 配置
              'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
              'LOCATION': 'cache_table_name',
              # 文件系统缓存 配置
              'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
              'LOCATION': '/var/tmp/django_cache',
              # 本地内存缓存 配置
              'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
              'LOCATION': 'unique-snowflake',
          }
      }
      ```

- 基于Memcached: 缓存存放于内存, 非永久性存储;

- 数据库缓存:
  
- 使用前, 需要用`python manage.py createcachetable`创建缓存表;
  
- 本地内存缓存:

  - **每个进程都有自己私有缓存实例, 不能进行跨进程缓存**
  - 不推荐生产环境使用,  可用于测试开发环境;

- 整站缓存:
  - 添加中间件`django.middleware.cache.UpdateCacheMiddleware, django.middleware.cache.FetchFromCacheMiddleware`;
    - `UpdateCacheMiddleware`: 在响应阶段: 判断是可缓存, 是, 缓存`response`
    - `FetchFromCacheMiddleware`: 在请求处理中, 根据`request`和配置的`CACHE_MIDDLEWARE_KEY_PREFIX`或者是`CACHE_MIDDLEWARE_ALIAS`获取缓存中的`response`
  
- 视图缓存:
  - `@cache_page(timeout)`
  - 处理过程类似整站缓存, 但是仅处理装饰视图;
- 缓存基本用法`django.core.cache.caches`:
  
  - `get(key, default, version), set(key, value, timeout, version), get_or_set(), delete()`

## 5.认证及权限

>扩展：
>
>Session：由于http协议是无状态协议，当需要做到同一用户的前后两次浏览相关联时就需要用到Session。Session信息存储于服务端；
>
>Cookie：存储于客户端；

### 1.Django 身份证明系统

- `django.contrib.auth`：身份证明系统核心极其默认模型；
- `django.contrib.contenttypes` ：权限管理；

### 2.User 及验证

> 验证系统的核心；保存用户信息的模型，像超级用户或管理员也在其中；

- 通过`AUTH_USER_MODEL`指定使用的用户模型类, 默认使用`auth.User`; 可以通过`get_user_model()`获取用户模型;
- 创建用户: `User.objects.create_user()`;

### 3.验证

- 通过`AUTHENTICATION_BACKENDS`指定验证模块, 默认是`django.contrib.auth.backends.ModelBackend`;
- 可以同时存在多个验证模块;

- 编写验证模块:
  
  - `authenticate(request, username=None, password=None)`: 获取用户, 验证凭证。如果它们无效，它应该返回`None`, 通过返回用户
- `django.contrib.auth.authenticate()`: 导入配置的后端模块并实例化,  以此调用后端模块的`authenticate`方法; 只要其中一个backend获取到用户信息, 退出;

- `login_required()`：

  - 装饰器，修饰视图函数；作用:

    - 1.如果用户未登陆，重定向到`settings.LOGIN_URL`，也可通过参数`@login_required(login_url='xxx')`指定；(后面还会加上请求的url作为登陆后的地址，`/login/?next=/xxxx/`);

    - 2.如果用户已经登陆，则正常执行视图;

    - ```python
      from django.contrib.auth.decorators import login_required

      # 可用于视图视图函数
      @login_required
      def my_view(request):
          pass

      # 也可用于url中的视图，
      url(r'^xxx/$', login_required(views.my_view), name='index'),

      # 需要配合 setting 中的 LOGIN_URL = 'url'
      ```

- `permission_required`装饰器，检查用户是否就有某种权限，

  - `@permission_required('polls.can_vote', login_url='/loginpage/')`；
  - 也用可使用user对象的方法`has_perm()`来判断，具有权限返回`True`；

### 4.权限管理

- `Permission`: 权限表, models有对应的`add_xxx, delete_xx, change_xx, view_xx`权限信息.

- 每个用户有一系列与之对应的权限表(`Permission`).
- 用户访问时, 可以获取到该用户的权限信息` {'app_lable-x.add_xxx', 'app_lable-x.add_xxx', 'app_lable-x.add_xxx'}`
- 根据请求方式(GET, POST等)和需要出来的model, 可以拼出 请求需要的权限`'%(app_label)'s.add_%(model_name)s'% (model._meta.app_label, model._meta.model_name)`
- 判断权限是否允许(是否在权限信息列表中)

## 6.安全

### 1.csrf攻击

> Cross Site Request Forgery，跨站域请求伪造，用户访问A站时，同过A站向B站发送请求，如果此时，用户登录过B站，那么会有cookie的本地存放，请求可能就会成功；也就说：黑客借助受害者的cookie骗取服务器的信任，但是黑客并拿不到cookie，也看不到cookie内容；另外，对于服务器返回的结果，由于浏览器的同源策略限制，黑客也无法解析；

- 防御CSRF的策略：
  - 1. 用户操作限制，比如验证码；
  - 2. 请求来源限制，比如限制HTTP Referer才能完成操作；
  - 3. token验证机制，比如请求数据字段,或头部中添加一个token，响应请求时校验其有效性；
- Django的策略:
  - `CsrfViewMiddleware`中间件会进行`csrf_token`的设置和验证工作:
    - 1.可以在`POST`数据时将`'csrfmiddlewaretoken': csrf_token`信息作为form信息传递;
    - 2.也可以设置`X-CSRFToken: csrf_token`的头部信息;
      - 注意: 前端头部设置和后端获取名称存在差异
      - a. 前端链接字符为`-`, 后端为`_`;
      - b. 后端会加上`HTTP`的前缀;
      - c.可以通过`CSRF_HEADER_NAME` 设置头部名称;
  - `rotate_token()`: 更新CSRF token信息, 通常在登录时调用.
- Django忽略csrf验证: `@csrf_exempt`;

### 2.XSS攻击

> 跨站脚本攻击, 通过想Web页面里插入恶意Script代码, 当用户浏览该页时, 嵌入其中Web里面的Script代码会被执行, 从而达到恶意攻击用户的目的.
>
> XSS攻击的本质就是想办法教唆用户的浏览器去执行一些这个网页中原本不存在的前端代码. 实现劫持访问, 盗用cookie,等
>
> 1.反射型: 不可信的用户数据被提交到一个web应用, 然后该数据立刻在相应中被返回, 
>
> 2.存储型: 会持久保存于Web应用的数据存储中, 例如留言, 插入脚本后, 留言内容会存储到服务器中, 每个打开该页面的用户都会收到攻击;

- 防御措施:
  - 过滤特殊字符:`<script>, <img> , <a>`等;
  - 对特殊符号进行转换编码;
  - 限制字符长度;
- Django模板可以转义对HTML特别危险的特定字符;

### 3.SECRET_KEY

- 在`django-admin startproject`时自动创建的随机产生;
- 该字符串被用于:
  - 用于`cryptographic signing`
  - All [`PasswordResetView`](https://docs.djangoproject.com/en/2.1/topics/auth/default/#django.contrib.auth.views.PasswordResetView) tokens.
  - All [messages](https://docs.djangoproject.com/en/2.1/ref/contrib/messages/) if you are using [`CookieStorage`](https://docs.djangoproject.com/en/2.1/ref/contrib/messages/#django.contrib.messages.storage.cookie.CookieStorage) or [`FallbackStorage`](https://docs.djangoproject.com/en/2.1/ref/contrib/messages/#django.contrib.messages.storage.fallback.FallbackStorage).

## 7.信号

> 发送者可以通知一组接收者执行某些操作. 信号自身会维护一个`receivers`的存储, 记录所有注册的接收者, 当调用`send()`方法发送信号时, 执行`receivers`中注册的接收者.

## 11.自定义命令

- 在app目录, 添加management/commands文件夹, Django会将该目录的每一个非`_`开头的python文件注册manage.py命令;

- 命令的Python模块必须定义Command类(`django.core.management.base.BaseCommand`的子类);

- 在定义的Command类中, 重写`def handle(self, *args, **options)`方法, 作为命令处理函数;

- 通过self.stdout.write(), self.stderr.write()`进行内容输出;

- 通过写`def add_arguments(self, parser):`接收指定参数

  - `parser.add_argument('name', nargs='+', type=str, default)`

  - `nargs`参数数量限制: 

  - ```python
    OPTIONAL = '?'
    ZERO_OR_MORE = '*'
    ONE_OR_MORE = '+'
    PARSER = 'A...'
    REMAINDER = '...'
    ```

## 附录

### I.调试技巧

### 1.log

> Django使用`logging`模块来打印系统记录；

- logging级别：*由低到高*
  - `logger.debug()`：仅用于调试
  - `logger.info()`：一般系统信息
  - `logger.warning()`
  - `logger.error()`
  - `logger.critical()`

- Using logging

  ```python
  import logging

  logger = logging.getlogger(__name__)  # 实力化logget， 并命名；
  ...
  logget.error('something wrong!')    # 打印日志
  ```