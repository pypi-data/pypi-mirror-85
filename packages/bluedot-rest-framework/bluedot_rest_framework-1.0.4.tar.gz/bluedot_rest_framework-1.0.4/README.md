# Bluedot Tools for Django REST framework

# Requirements

- Python (3.5, 3.6, 3.7, 3.8, 3.9)
- Django (2.2, 3.0, 3.1)

# Installation

Install using `pip`...

```
    pip install bluedot_rest_framework
```

Add `'bluedot_rest_framework'` to your `INSTALLED_APPS` setting.

```
    INSTALLED_APPS = [
        ...
        'bluedot_rest_framework',
    ]
```

# Docs

## apps

### analysis

#### monitor

```
router.register(r'analysis/monitor', MonitorView, basename='analysis-monitor')
```

### api_auth

```python
urlpatterns = [
    url(r'^auth/login', login_url),
    url(r'^auth/current-user', current_user_url)
]

router.register(r'auth/menu', MenuViewSet, basename='auth-menu')
router.register(r'auth/user', AuthUserViewSet, basename='auth-user')
router.register(r'auth/group', AuthGroupViewSet, basename='auth-group')
router.register(r'auth/permission',
                AuthPermissionsViewSet, basename='auth-permission')

```

### category

**models.py**

```python
class Category(Document):
    _type = fields.IntField(max_length=10, default=1)
    title = fields.StringField(max_length=100, null=True)
    parent = fields.ReferenceField(
        'self', reverse_delete_rule=PULL)
    sort = fields.SequenceField()

    created = fields.DateTimeField(default=datetime.now)
    updated = fields.DateTimeField(default=datetime.now)

    meta = {'collection': 'category'}
```

**views.py**

```python
@action(detail=False, methods=['post'], url_path='sort', url_name='sort')
    def sort(self, request, *args, **kwargs):
        before_sort = request.data.get('before_sort')
        before_id = request.data.get('before_id')
        after_sort = request.data.get('after_sort')
        after_id = request.data.get('after_id')
        self.model_class.objects.get(pk=before_id).update(sort=after_sort)
        self.model_class.objects.get(pk=after_id).update(sort=before_sort)
        return Response(status=200)
```

### user

**base_model.py**

```python

class Profile(EmbeddedDocument):
    first_name = fields.StringField(max_length=100)
    last_name = fields.StringField(max_length=100)
    email = fields.StringField(max_length=100)
    tel = fields.StringField(max_length=100)
    company = fields.StringField(max_length=100)
    job = fields.StringField(max_length=100)
    country = fields.StringField(max_length=100)
    source_type = fields.StringField(max_length=100, null=True)

    meta = {'abstract': True}


class WechatProfile(EmbeddedDocument):
    nick_name = fields.StringField(max_length=100)
    avatar_url = fields.StringField(max_length=255)
    gender = fields.IntField(max_length=10)

    province = fields.StringField(max_length=100)
    city = fields.StringField(max_length=100)
    country = fields.StringField(max_length=100)

    language = fields.StringField(max_length=100)
    meta = {'abstract': True}


class AbstractUser(Document):
    unionid = fields.StringField(max_length=100)
    openid = fields.StringField(max_length=100)

    wechat_profile = fields.EmbeddedDocumentField(WechatProfile)

    profile = fields.EmbeddedDocumentField(Profile)

    created = fields.DateTimeField(default=datetime.now)
    updated = fields.DateTimeField(default=datetime.now)

    meta = {'allow_inheritance': True, 'abstract': True}

```

## middleware

### log

```python
MIDDLEWARE = [
    'bluedot_rest_framework.middleware.log.ApiLoggingMiddleware'
]
```

## utils

### crypto

```python
from bluedot_rest_framework.utils.crypto import AESEncrypt
```

加密：AESEncrypt.decrypt()

解密：AESEncrypt.encrypt()

### jwt_token

```python
from bluedot_rest_framework.utils import jwt_token
```

**jwt_create_token_wechat**

```python
jwt_token.jwt_create_token_wechat(openid, unionid, userid='')
return token
```

**jwt_get_openid_handler**

```python
jwt_token.jwt_get_openid_handler(auth)
return openid
```

**jwt_get_unionid_handler**

```python
jwt_token.jwt_get_unionid_handler(auth)
return openid
```

**jwt_get_userid_handler**

```python

jwt_token.jwt_get_userid_handler(auth)
return user_id
```

**jwt_get_userinfo_handler**

```python
jwt_token.jwt_get_userinfo_handler(auth)
return openid,unionid,user_id
```

### oss

```python
from bluedot_rest_framework.oss import OSS
```

**put_object_internet**

```python
OSS.put_object_internet(url, path)
return None
```

**put_object_bytes**

```python
OSS.put_object_bytes(data, path)
return None
```

### pagination

```python
from bluedot_rest_framework.utils.pagination import CustomPagination
```

```python
class CustomPagination(PageNumberPagination):
    page_query_param = 'current'
    page_size_query_param = 'pageSize'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'pageSize': self.get_page_size(self.request),
            'current': self.page.number,
            'data': data
        })
```

### serializers

```python
from bluedot_rest_framework.utils.serializers import CustomSerializer
```

**exclude_fields**

```python

```

### viewsets

```python
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet
```

**model_class**

模型名称

**filterset_fields**

URL filter 字段设置

```python
filterset_fields = {
        '_type': {
            'type': 'int',
            'filter': ''
        },
        'title': {
            'type': 'string',
            'filter': '__contains'
        },
        'extend__is_banner': {
            'type': 'boolean',
            'filter': ''
        },
    }
```

**user_perform_create**
创建数据，写入 user_id，openid，unionid 字段

```python
def user_perform_create(token, serializer):
    user_id = jwt_get_userid_handler(token)
    openid = jwt_get_openid_handler(token)
    unionid = jwt_get_unionid_handler(token)
    serializer.save(user_id=user_id, openid=openid, unionid=unionid)
```
