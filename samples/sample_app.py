import logging

from mest.app import Mest, MestConfig
from mest.app.api import Router
from mest.models import GenericModel


# import os
# import pickle


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
conf = MestConfig(service_name='sample_mest',
                  listen_port=1234,
                  # Pass the model instance!
                  models_instances=[model])

# Setup your application
mest_app = Mest(conf).setup()


# Usually you want this in a different file
def register_routes(mest_app):
    # Create a router
    api_v1 = Router('v1')

    # Add GET /ping route (if needed)
    api_v1.add_ping_route()

    # Add POST /predict
    api_v1.add_predict_route(model,
                             schema={
                                 'feature1': {'type': 'float', 'required': True},
                                 'feature2': {'type': 'float', 'required': True},
                                 'feature3': {'type': 'float', 'required': True},
                             })

    mest_app.register_router(url='/api/v1',
                             router=api_v1)


# Register the routes on your app
register_routes(mest_app)

# You can also get the application logger whenever you want
logger = logging.getLogger('sample_mest')
logger.debug('Works!')

if __name__ == '__main__':
    mest_app.run()

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
