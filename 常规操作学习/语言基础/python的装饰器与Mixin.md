# 起因

今天在阅读python-gitlab库的时候，发现简单地实现了get方法，get方法，可以同时解析id与字符形式。

首先是gitlab的api：

api支持id（int）与url式字符串的格式。

例如：

```shell
# url格式：
curl --request GET --header PRIVATE-TOKEN=$CI_JOB_TOKEN $CI_API_V4_URL/projects/$CI_INTER_ID/repository/files/$NEED_FILE_1/raw?ref=master
```

其中`$CI_INTER_ID`可以是int形式，`6`,也可以是url的字符串形式`mabo_group%2Fbase_application%2Fdoctopus_ziyan`

# 源码

使用这个库构建的时候，其使用了这样的方法：

```python
# 入口
gl.groups.get(group_id)
# Group定义：
class GroupManager(CRUDMixin, RESTManager):
	_path = '/groups'
    _obj_cls = Group
    _list_filters = ('skip_groups', 'all_available', 'search', 'order_by',
                     'sort', 'statistics', 'owned', 'with_custom_attributes')
    _create_attrs = (
        ('name', 'path'),
        ('description', 'visibility', 'parent_id', 'lfs_enabled',
         'request_access_enabled')
    )
    _update_attrs = (
        tuple(),
        ('name', 'path', 'description', 'visibility', 'lfs_enabled',
         'request_access_enabled')
    )
    
# CRUDMixin的定义
class CRUDMixin(GetMixin, ListMixin, CreateMixin, UpdateMixin, DeleteMixin):
    pass

class NoUpdateMixin(GetMixin, ListMixin, CreateMixin, DeleteMixin):
    pass

# GetMixin的定义
class GetMixin(object):
    @exc.on_http_error(exc.GitlabGetError)
    def get(self, id, lazy=False, **kwargs):
        """Retrieve a single object.

        Args:
            id (int or str): ID of the object to retrieve
            lazy (bool): If True, don't request the server, but create a
                         shallow object giving access to the managers. This is
                         useful if you want to avoid useless calls to the API.
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            object: The generated RESTObject.

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server cannot perform the request
        """
        if not isinstance(id, int):
            id = id.replace('/', '%2F')
        path = '%s/%s' % (self.path, id)
        if lazy is True:
            return self._obj_cls(self, {self._obj_cls._id_attr: id})
        server_data = self.gitlab.http_get(path, **kwargs)
        return self._obj_cls(self, server_data)
```

# 继承与派生

#### 本质上就是一个**类的继承**。

<!--说什么Mixin技术。。。呵呵-->

> <https://www.cnblogs.com/eric-nirnava/p/mixin.html>

用法就如同上述所示。会直接把对应的方法加进去的。

当然，对于避免继承线过长，所以尽量多使用组合，少用派生。

#### 类的组合：

组合，在一个类中以另一个类的对象作为数据属性，称为类的组合。

我喜欢这种形式。

```python
class Skill:
    def fire(self):
        print("release Fire skill")

class Riven:
    camp='Noxus'
    def __init__(self,nickname):
        self.nickname=nickname
        self.skill5=Skill().fire()#Skill类产生一个对象，并调用fire()方法,赋值给实例的skill5属性

r1=Riven("瑞雯")
```

# 装饰器：

> <https://foofish.net/python-decorator.html>

首先，python可以将函数，像普通变量一样，当作参数，传递给另外一个函数。

[^]: 传递函数！这个可以玩的东西就有点多了啊！

装饰器，简单来说就是将函数包起来使用：

```python
def use_logging(func):

    def wrapper():
        logging.warn("%s is running" % func.__name__)
        return func()   # 把 foo 当做参数传递进来时，执行func()就相当于执行foo()
    return wrapper

def foo():
    print('i am foo')

foo = use_logging(foo)  # 因为装饰器 use_logging(foo) 返回的时函数对象 wrapper，这条语句相当于  foo = wrapper
foo() 
```

这里，将foo重定向为use_logging(foo)。

[^return wrapper]: 这里不是很必要，但写了也没啥毛病就是了。

### @ 语法糖

@ 符号就是装饰器的语法糖，它放在函数开始定义的地方，这样就可以省略最后一步再次赋值的操作。

### *args、**kwargs

可能有人问，如果我的业务逻辑函数 foo 需要参数怎么办？比如：

```python
def foo(name):
    print("i am %s" % name)
```

我们可以在定义 wrapper 函数的时候指定参数：

```python
def wrapper(name):
        logging.warn("%s is running" % func.__name__)
        return func(name)
    return wrapper
```

这样 foo 函数定义的参数就可以定义在 wrapper 函数中。这时，又有人要问了，如果 foo 函数接收两个参数呢？三个参数呢？更有甚者，我可能传很多个。当装饰器不知道 foo 到底有多少个参数时，我们可以用 *args 来代替：

```python
def wrapper(*args):
        logging.warn("%s is running" % func.__name__)
        return func(*args)
    return wrapper
```

如此一来，甭管 foo 定义了多少个参数，我都可以完整地传递到 func 中去。这样就不影响 foo 的业务逻辑了。这时还有读者会问，如果 foo 函数还定义了一些关键字参数呢？比如：

```python
def foo(name, age=None, height=None):
    print("I am %s, age %s, height %s" % (name, age, height))
```

这时，你就可以把 wrapper 函数指定关键字函数：

```python
def wrapper(*args, **kwargs):
        # args是一个数组，kwargs一个字典
        logging.warn("%s is running" % func.__name__)
        return func(*args, **kwargs)
    return wrapper
```

### 装饰器顺序

一个函数还可以同时定义多个装饰器，比如：

```python
@a
@b
@c
def f ():
    pass
```

它的执行顺序是从里到外，最先调用最里层的装饰器，最后调用最外层的装饰器，它等效于

```python
f = a(b(c(f)))
```

<!--可以说，到了这里就已经非常之恶臭了。咦惹！！！-->