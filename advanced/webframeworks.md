---
sort: 1
---

## Web Frameworks
Currently, `falcon` is the only WebFramework implemented.
 
You can implement your own web-framework (if you need to) and pass it as a parameter

```python
from mlserving import ServingApp
from mlserving.webframeworks import WebFramework

class MyWebFramework(WebFramework):
    #TODO: Implement abstract methods...
    pass

app = ServingApp(web_framework=MyWebFramework())
```
