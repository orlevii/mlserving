import logging
import os
import pickle

from ganesha.app import Ganesha, GaneshaConfig
from ganesha.app.api import generate_api_v1
from ganesha.models import GenericModel


# Used for this sample app
class StubModel:
    def predict(self, *vector):
        # Lets say that's a stupid regression
        return sum(vector)


# Can be in a different file
class MySampleModel(GenericModel):
    def init(self, path):
        # Usually you want to load your model artifact here, something like:
        # file_path = os.path.join(path, 'my_model.pkl')
        # with open(file_path, 'rb') as f:
        #     self.model = pickle.load(f)
        self.model = StubModel()

    def pre_process(self, feature1, feature2, feature3):
        # Let's do some processing on the features (normalization, embedding, etc, you name it...)
        feature1 *= 2
        feature2 /= 10
        return [feature1, feature2, feature3]

    def infer(self, *vector):
        return self.model.predict(*vector)

    def post_process(self, prediction):
        return dict(prediction=prediction)


# Create an instance of your model
model = MySampleModel()

# Create your configuration
conf = GaneshaConfig(service_name='sample_ganesha',
                     listen_port=1234,
                     # Pass the model instance!
                     models_instances=[model])

# Setup your application
ganesha_app = Ganesha(conf).setup()


# Usually you want this in a different file
def register_routes(ganesha_app):
    # Out of the box - GET /ping & GET /health
    api_v1 = generate_api_v1()
    # Add POST /predict
    api_v1.simple_predict(model,
                          schema={
                              'feature1': {'type': 'float', 'required': True},
                              'feature2': {'type': 'float', 'required': True},
                              'feature3': {'type': 'float', 'required': True},
                          })

    ganesha_app.register_router(url='/api/v1',
                                router=api_v1)


# Register the routes on your app
register_routes(ganesha_app)

# You can also get the application logger whenever you want
logger = logging.getLogger('sample_ganesha')
logger.debug('Works!')

if __name__ == '__main__':
    ganesha_app.run()

# Now, you can run a simple POST request!
"""
curl -X POST http://localhost:1234/api/v1/predict \
-H 'Content-Type: application/json' \
  -d '{
    "feature1": 10,
    "feature2": 4,
    "feature3": 0.123
}'
"""
