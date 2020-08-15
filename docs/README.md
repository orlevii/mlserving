# Mest
ML Models on REST.

A framework for developing a realtime model-inference service.

Allows you to set up an inference-endpoint for you ML Model easily. 

## Table of Contents:
1. [Installation](#intallation)
2. [Serving Models](#serving_models)
3. [Web Frameworks](#web_frameworks)
4. [Running In Production](#production)

<a name="intallation"></a>
## Installation

* Run: `pip install mest`

<a name="serving_models"></a>
## Serving Models
Serving models is easy, by implementing simple interfaces, you can set up endpoints in no time.
Just implement your business-logic, mest takes care of everything else.

`BaseModel` - Represents your model artifacts and everything needed in order to run inference
`BasePredictor` -  Given a `BaseModel` implements the inference flow:
1. pre_process - receives the payload from the request, makes processing (if needed). Returns post-processed features
2. infer - receives post-process features, returns the prediction
3. post_process - receives the prediction, and returns the final response the client will receive.

Simple example of serving scikit-learn `LogisticRegression` model
```python
from mest import Mest
from mest.predictors import PredictorBase
from mest.api import Response

import joblib # for deserialization saved models 


class MyPredictor(PredictorBase):
    """
    BasePredictor has a constructor that accepts BaseModel
    """
    def __init__(self):
        self.model = joblib.load('./models/logistic_regression.pkl')
    
    def pre_process(self, input_data, req):
        return input_data['features']

    def infer(self, processed_data):
        return self.model.predict_proba(processed_data)[0]
    
    def post_process(self, prediction, req):
        return {'probability': prediction}

app = Mest()
app.add_inference_handler(MyPredictor(), '/api/v1/predict')
app.run()
```
This example assumes your endpoint receives post-processed features.

`app.run()` - Will start up development server, by default it listens on port 5000

<a name="web_frameworks"></a>
## Web Frameworks
Currently, `falcon` is the only WebFramework implemented.
 
You can implement your own web-framework and pass it as a parameter

```python
from mest import Mest
from mest.webframeworks import WebFramework

class MyWebFramework(WebFramework):
    #TODO: Implement abstract methods...
    pass

app = Mest(web_framework=MyWebFramework())
```

<a name="production"></a>
## Running In Production
It's not recommended to use `app.run()` for production.

gunicorn with gevent works well for most use-cases:

`pip install gunicorn[gevent]`

server your application: `app.py`:
```python
from mest import Mest
# other imports ...


app = Mest()
```

Run: `gunicorn -b 0.0.0.0:5000 -k gevent -w 4 app:app`
