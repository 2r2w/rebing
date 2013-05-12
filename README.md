#Simple class to use Bing search API

```python
from BingSearch import BingWebsearch

b = BingWebsearch('your key here', False)
print b.websearch("hello", Market="ru-RU")
```