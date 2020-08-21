## TensorFlow Serving

### Intro
TensorFlow Serving is an high-performance system designed for serving TensorFlow models.

It can load saved models (ProtoBuff format) and expose an endpoint for inference

Sometimes, we can't use TensorFlow serving alone as we need to make some processing before/after the inference.

Read more about TensorFlow Serving: [https://www.tensorflow.org/tfx/guide/serving](https://www.tensorflow.org/tfx/guide/serving)

### Integration
<code>mlserving</code> allows easy integration with <code>TensorFlow Serving</code> model server.

The idea is to have a python layer that can make some processing before invoking the tf-serving endpoint.

<code>TFServingPrediction</code> implements <code>def predict</code> can be used as a mixin that handles the tf-serving request

```python
from mlserving.predictors import RESTPredictor
from mlserving.predictors.tensorflow import TFServingPrediction

class MyPredictor(TFServingPrediction, RESTPredictor):
    def __init__(self):
        # configure the TFServingPrediction with default values.
        super().__init__()
        # Default values: host='127.0.0.1' port=8501 model_name='model'

    def pre_process(self, features: dict, req):
        return {
            "instances": [
                # TODO: fill your tensor inputs here
            ]
        }

    def post_process(self, prediction, req):
        prediction = prediction['prediction']
        return {
            'probabilities': prediction,
        }
```

Since </code>def predict</code> is already implemented, we just need to implement the processing layer that comes before/after the inference
