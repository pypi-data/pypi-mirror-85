# villaAuthSdk
> interact with villa authentication backend


## Install

`pip install villaAuthSdk`

## How to use

create an auth object

```
from villaAuthSdk.auth import AuthSdk
from nicHelper.dictUtil import printDict
```

```
authSdk=AuthSdk(user=None,pw=None,region='ap-southeast-1')
## user and pw here are the aws key/secret for your client
```

## login

```
result=authSdk.auth(user='nic1',pw='12345678')
printDict(result)
```

    AccessKeyId : ASIAVX4Z5T
    SecretKey : eyzrqVIXe3
    SessionToken : IQoJb3JpZ2
    Expiration : 1605583141.0
    AccessToken : eyJraWQiOi
    ExpiresIn : 3600
    TokenType : Bearer
    RefreshToken : eyJjdHkiOi
    IdToken : eyJraWQiOi
    NewDeviceMetadata
     DeviceKey : ap-southea
     DeviceGroupKey : -lt0cpemm


## Create new user

```
result=AuthSdk().createUser(user='nic4',phone='+66828773682',pw='12345678',name='nic3')
printDict(result)
```

    success : True
    user : nic4

