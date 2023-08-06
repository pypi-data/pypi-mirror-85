# requests_middleware_ali_hmac 
### requests_middleware_ali_hmac demo 
```python
import requests
from requests_middleware import MiddlewareHTTPAdapter
from requests_middleware_ali_hmac import AliHmacGenerate
session = requests.Session()
middlewares = [
    AliHmacGenerate("testid", "testsecret"),
]
adapter = MiddlewareHTTPAdapter(middlewares)
session.mount('http://', adapter)
session.mount('https://', adapter)
```
allow requests methods "GET", "POST", "PUT", "DELETE", "PATCH"