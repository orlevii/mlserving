## Serving Models
Serving models is easy, by implementing simple interfaces, you can set up endpoints in no time.
Just implement your business-logic, mlserving takes care of everything else.

Simple example of serving scikit-learn `LogisticRegression` model
```python
from mlserving import ServingApp
from mlserving.predictors import RESTPredictor

import joblib # for deserialization saved models 


class MyPredictor(RESTPredictor):
    def __init__(self):
        # Loading a saved model
        self.model = joblib.load('./models/logistic_regression.pkl')

    def pre_process(self, input_data, req):
        return input_data['features']

    def predict(self, processed_data, req):
        return self.model.predict_proba(processed_data)[0]

    def post_process(self, prediction, req):
        return {'probability': prediction}

app = ServingApp()
app.add_inference_handler(MyPredictor(), '/api/v1/predict')
app.run()
```
This example assumes your endpoint receives post-processed features.

<code>app.run()</code> - Will start up development server, by default it listens on port 5000
