## django-request-sign

对django请求进行签名效验

### 安装

`pip install django-request-sign`

### 使用

将 `request_sign.middleware.RequestSignMiddleware` 放置到中间件第一位

``` python
# django settings
MIDDLEWARE = [
    'request_sign.middleware.RequestSignMiddleware',
    ...
    ...
]
```

### 前端支持与示例

需要在header头中增加的参数，这里以[axios](./example/axios/index.js)作为参考,前端签名参考[示例js文件](./example/sign/index.js)

实际使用前请不要忘了删除示例文件中输出的日志信息


| 参数  | 说明  |
| ------------ | ------------ |
| timestamp  | 请求时间戳  |
| nonce  |  请求ID（随机生成） |
| sign | 本次请求签名 |


### 配置参数

 配置参数  | 说明 | 类型|默认值 |示例
------------ | ------------ | ------------ | ------------ |------------ 
  ENABLE_REQUEST_SIGNATURE |  是否开启 | Boolean |`False`| `True`/`False`
  SIGNATURE_SECRET | 签名秘钥  | Str|`None`|`e6QGz7AhFzFAFsR9jYoCUnZGsqDrQI`
  SIGNATURE_ALLOW_TIME_ERROR|允许请求时间前后误差|Int|`600`|`600`
  SIGNATURE_RESPONSE|签名不通过返回方法|Str|`request_sign.utils.default_response`|`you_project.you_app.file.function`
  SIGNATURE_PASS_URL|不需要验证签名的url|List|[]|`['/api/v1/mcn/content/download']`
  SIGNATURE_PASS_URL_NAME|不需要验证签名的url名称|List|[]|`['DownloadContent']`
  SIGNATURE_PASS_URL_REGULAR|不需要验证签名的url正则|List|[]|`['/app/*']`

  SIGNATURE_METHOD|效验请求类型|List|['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']|['get']
  NONCE_CACHE_KEY|唯一性检查缓存key名称|Str|"django_request_sign_nonce_{nonce}"|"test_{nonce}"
  
##### 参数说明：SIGNATURE_RESPONSE

```python
from django.http import HttpResponse

# request_sign.utils.default_response
def default_response():
    """
        Must return django HttpResponse type
    :return: HttpResponse
    """
    return HttpResponse()
```

`request_sign.utils.default_response` 方法默认返回http状态码为200的空信息，你可以自行实现一个返回函数，更改 `SIGNATURE_RESPONSE`配置
即可，但请一定注意，自行实现的函数一定要返回一个django的`HttpResponse`对象，否则django会异常。

##### 参数说明：SIGNATURE_PASS_LIST
在此名单中的请求地址将不会效验签名，如`http://example.com/a/b/c?p=1` 填写：`/a/b/c`即可，主机与请求参数不用填写

1. 在urls.py中配置name属性 `re_path('content/download', views.DownloadContent.as_view(), name='DownloadContent')`，配置中填写name值即可(推荐) 
2. 直接写url(不推荐)

##### 参数说明：NONCE_CACHE_KEY
传入的key名称会以format函数解析，所以你必须在字符串中包括`{nonce}`
请求唯一性检查需要设置django-redis，每次请求都会插入一个key来判断唯一性，如果没有安装django-redis则此配置无效

### 签名参数sign生成的方法

1. 拼接字符串，首先去除sign参数本身，然后去除值是空的参数p3，剩下p2=v2&p1=v1&method=cancel&pn=vn，
然后按参数名字符升序排序，method=cancel&p1=v1&p2=v2&pn=vn.
2. 然后做参数名和值的拼接，最后得到methodcancelp1v1p2v2pnvn
3. 在上面拼接得到的字符串后加上验证密钥key，我们假设是abc，得到新的字符串methodcancelp1v1p2v2pnvnabc
4. 然后将这个字符串换为小写进行md5计算，假设得到的是abcdef，这个值即为sign签名值。




### 参考

* https://www.jianshu.com/p/ad410836587a
* https://www.cnblogs.com/yoyoketang/p/11742187.html

