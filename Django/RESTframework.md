# Django REST Framework

## 1.Request

> 在 APIView视图类或者@api_view修饰的视图函数中, request为Request的实例

- `.query_params`: 请求参数, 等同于`request.GET`
- `.data`: 请求体内容, 包括所有内容(文件和非文件), 支持不同的content-type.
- `.method`: 请求方法;
- `.content_type`:  返回请求主体的媒体类型, 对应头部`content-type`;
- `.user`:

## 2.Response

> 使用`Response`类,  REST框架按照标准的HTTP内容协商来确定应如何呈现最终响应内容.

- `Response(data, status=None, header=None, content_type=None)`
  - `data`: 相应的数据;
  - `status`: 状态码;
  - `header`: 在响应中使用的头部信息;
  - `content_type`: 相应内容类型, 通常, 由协商自动设置;

## 3.Views

### 1.APIView

> 1.传递给处理程序的request是Request的实例;
>
> 2.任何异常都将被捕获并交给`EXCEPTION_HANDLER`配置的异常处理函数`exception_handler(exc, context)`处理;
>
> 3.传入请求将经过身份(权限验证);

- `@api_view()`:

### 2.通用视图

> 通用视图允许快速生成与数据库模型紧密映射的API视图.

#### 1.基础属性和方法

- `queryset`: 应用于此视图的查询范围;
  - 相关方法:`get_queryset() --> return queryset.all()`
- `serializer_class`:应用于此视图的验证, 序列化, 反序列化的序列化类;
  - 相关方法:`get_serializer_class() --> return self.serializer_class`'
- `lookup_field`: 单个模型实例查找的字段名, 默认是`pk`;
- `lookup_url_kwarg`: 应用于对象查找的URL关键字参数.
- `filter_backends`: 查询集过滤的过滤类, 默认是`DEFAULT_FILTER_BACKENDS`;
- `pagination_class`: 分页类, 默认是`DEFAULT_PAGINATION_CLASS`;
- `get_object()`: 返回应用于视图的对象实例.
- `get_serializer()`: 返回序列化器实例.
- `get_serializer_context()`: 传递给序列化器的上下文信息, 包括(request, view)

#### 2.Mixin

> 提供了一些用于在基本视图中使用的方法.

- 获取单个`retrieve()`
- 获取列表`list()`
- 创建`create()`
- 更新`update()`
- 删除`destroy()`

### 3.ViewSet

> 在单个类中将一组相关的逻辑操作组合在一起, 提供一系列相关操作方法如`list(), create()`, 共用`queryset,  serializer_class`等属性, 通过`as_view(actions)`, 将请求方式和相关操作对应

#### 1.ViewSetMix

- `as_view(self, actions=None)`:
  - 重写了`as_view`方法, `actions`为映射关系`{'get': 'list'}`
  - `url(xxx, UserViewSet.as_view({'get': 'list'}))`
  - 通常会向路由器注册视图集, 并允许自动生成urlconf;

- 可以通过 `@action(methods=None, detail=None, url_path=None, url_name=None, **kwargs)`标记操作为可路由的:

  - `methods`: 路由到的方法, 默认`get`;

  - `detail`: 是否是详情(获取单个还是多个);

  - > 原理: 装饰器给被装饰函数附加`mapping, detail, url_path`等属性, router通过`viewset.get_extra_actions`获取所有`action`装饰函数; 对其进行处理

#### 2.路由

> 将视图逻辑连接到一组URL的简单,快速方法.

- `BaseRouter`: 路由基类
  - `register(self, prefix, viewset, basename, base_name)`: 注册一组视图集, 前缀, basename等信息.
    - 所有注册的信息存储在`registry`属性中;
  - `urls`: 列表, 保存生成的`url(regex, view)`;
    - `regex`: 由`prefix, lookup`组成;
    - `view`: 由`ViewSet, maaping, initkwargs`组成;
- `Route = namedtuple('Route', ['url', 'mapping', 'name', 'detail', 'initkwargs'])`: 命名元组, 负责保存基本信息
  - `url = r'^{prefix}/{lookup}{trailing_slash}$'`: 生成路由的格式;
  - `mapping`: 请求方法和视图集方法的映射关系;
  - `name`: 路由名称;
  - `detail`: True/False, 是否为单个资源详情;

## 4.序列化

> 允许将**查询集或数据**转换为python数据类型

### 1.Serializer类介绍

- `.__init__(instance=None, data=empty, **kwargs)`初始化可接受信息:
  - `instance`: 对象模型实例;
  - `data`: 数据;
  - `partial`: 部分标志;
  - `context`: 上下文信息, 保存在`self._context`中;
  - `many`:

- 关键属性和方法:
  - `.data`: 序列化后的数据;
  - `.is_valid()`: 验证传入的数据, 返回`True/False`;
  - `.validated_data`: 通过验证和清理后的数据, 必须执行过`is_valid()`;
  - `.save()`: 将验证后的数据转化为一个实例,  `validated_data`必须有数据, 根据初始化时是否传入`instance`, 调用`.create()`或`.update()`实现;
  - `.create()`: 创建实例并保存;
  - `.update()`: 更新并保存实例;
  - `.to_representation(instance)`: `Object instance -> Dict`, 重写实现支持序列化, 进行读取操作;
  - `.to_internal_value(data)`: `Dict of native values <- Dict of primitive datatypes`, 重写实现支持反序列化, 进行写操作;
  - `.fields`: 保存所有的字段信息;
  - `.errors`: 保存`is_valid()`验证失败的信息;

### 2.序列化

- 序列化过程:
  - 调用每个字段的`field.to_representation()`, 获取对应值, 所有字段名和值组成`OrderedDict()`;
  - 处理多个对象: `many=True`
    - 初始化时, 需要传入`many=True`参数; *当`many=True`时, 会采用`Meta`中定义的`list_serializer_class`或者`ListSerializer`进行实例化,  指定的实例化类型通过`.child`进行绑定*
    - 通过`serializer.data`得到一个列表;

- 提供额外的上下文信息:`context={}`
  - 传入的上下文信息会被存储在`self._context`中, 在后续的自定义方法或者重写的`to_representation`方法中可以从中获取信息;

- 利用模型定义序列化类: `ModelSerializer`
  - 在`Meta`中, 定义序列化类相关属性;
    - `model`: 指定对应模型,
    - `readonly_fields`:
    - `fields`: 指明需要序列化的所有字段, 对应` exclude `;
    - `depth`: 关系字段默认是pk, 可以使用`depth`生成嵌套关系(生成嵌套, 反序列化时保存需要重写);
    - `read_only_fields`: 只读字段;
  - 可以在模型的基础上增加字段;
  - `serializer_related_field`: 指定默认关系字段`PrimaryKeyRelatedField`, 

### 3.反序列化

- 反序列化过程:
  - 初始化参数中的`data`数据, 会存放在`self.initial_data`中, 经过`self.is_valid`验证通过, 会存放在`self._validated_data`中;
  - 调用`sava()`方法, 取出`validated_data`, 调用`update(self.instance, validated_data)或 create(validated_data)`保存数据;
  - 注意: 默认的`create, update`方法不能处理嵌套数据, 嵌套数据的保存需要重写该方法;

- 部分更新: 部分更新时, 可以通过`partial=True`参数, 避免验证失败;
- 反序列化过程只会操作**可写字段**;

### 4.数据验证过程

- 标准验证流程: 序列化器通过`is_valid()`验证传入数据的合法性;
  - 1.验证通过的数据存放在`self._validated_data`中, 当存在验证数据时, 不会再次进行验证;
  - 2.调用`self.run_validation`进行验证;
    - 将数据转换为`OrderedDict`类型, 并调用字段的`validator`验证器, 以及`validate_<字段名>`验证字段;
    - 调用自定义验证函数`self.validate()`
    - 如果验证不通过, 抛出`ValidationError`异常;
- 自定义验证:
  - 可以针对某个字段定义`.validate_<field_name>(value)`方法, 附加验证指定字段;
  - 可以重写`.validate(data)`方法;
  - 字段定义时, 可以通过`validators`指定多个验证器`score = IntegerField(validators=[multiple_of_ten, xxx])`;
- 如果 验证不通过, 需要引发`serializers.ValidationError`;

### 5.字段

- 核心参数:
  - `read_only`: 序列化包含, 但是反序列化不包含;
  - `write_only`: 序列化不包含, 但是反序列化包含;
  - `required`: 标识反序列化必须提供该字段信息;
  - `validators`: 验证器

- `get_attribute()`: 获取实例的改字段值;
- `to_representation(value)`: 
- 不同的字段, 会根据参数和字段性质, 定义不同的验证器`validator`, 例如`MaxLengthValidator, MinLengthValidator, EmailValidator`;
- 关系字段:
  - 默认关系字段: `PrimaryKeyRelatedField`

## 5.限流

### 1.DRF中限流的实现方式

- 按照配置, 解析出最大允许**请求次数`num_requests`**和**时间范围`duration`**
- 由`request`拼出当前请求在缓存中对应的`key`.
- 获取缓存记录(列表, 元素为每次请求的时间戳);
- 遍历当条缓存记录, 如果时间戳超出范围(`<= now - duration`), 清理对应的记录;
- 判定剩余记录数量, 超出允许请求次数, 则禁止请求; 反之, 添加当前时间戳到对应缓存记录(可以设置过期时间(时间范围))并允许请求.

### 2.配置

```python

```

