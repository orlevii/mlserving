---
sort: 2
---

## Predictors

`PredictorBase` presents a simple interface:

<img width="600" alt="Request Flow" src="https://user-images.githubusercontent.com/13447456/90832827-58cd6a00-e34f-11ea-84df-83f9e2a1c6ad.png">

---

* `before_request` - Things to do before starting the ml-business logics (like parsing, validations, etc...) 
* `pre_process` - Used for feature processing (string embedding, normalizations, etc...)
* `predict` - Predicting a result with your loaded model
* `post_process` - Formatting a response for your client, the return value of this method will be sent back in the response

This interface is very intuitive, and makes it easy to integrate other serving-apps like `TensorFlow Serving`.

These methods are called one after the other, the output of a method will become the input of the next one in line.

Since the most common format of transmitting data over HTTP/1.1 is JSON, mlserving accepts & returns JSONs only

### RESTPredictor
This class implements `PredictorBase` and the go-to class to inherit from.

#### Usage:
When you inherit from `RESTPredictor`, you usually want to load relevant resources on `def __init__`

```python

from mlserving.predictors import RESTPredictor

import joblib

class MyPredictor(RESTPredictor):
    def __init__(self):
        # Loading resources
        self.model = joblib.load('./models/my_trained_model.pkl')

```

RESTPredictor also adds validations to the input request in `before_request`

The validation is done with `validr`, a fast(and easy to use python library.

In order to define your request schema, you'll need to add a decorator above your predictor class:

```python
from mlserving.api import request_schema
from mlserving.predictors import RESTPredictor

SCHEMA = {
    # floats only list
    'features': [
        'list',
        'float'
    ]
}

@request_schema(SCHEMA)
class MyPredictor(RESTPredictor):
    # TODO: Implement "def predict" & override methods (if needed)
    pass
```

`validr` syntax can be found here: https://github.com/guyskk/validr/wiki/Schema-Syntax
