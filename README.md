# Jarvis
A framework for developing a realtime model-inference service.

Allows you to set up an inference-endpoint for you ML Model easily.

## Table of Contents:
1. [Installation](#intallation)
2. [Basic Setup](#basic_setup)
3. [Your First Endpoint](#endpoints)
4. [Models](#models)
5. [Logging](#logging)
6. [CLI Commands](#cli_cmd)

<a name="intallation"></a>
## Installation

* Run: `pip install jarvis`


<a name="basic_setup"></a>
## Basic Setup
```python
from jarvis.app import Jarvis, JarvisConfiguration
from jarvis.app.api import generate_api_v1

# Initialize configuration
conf = JarvisConfiguration(service_name='sample_jarvis',
                           listen_port=1234)

# Setup an application
jarvis_app = Jarvis(conf).setup()

# Get pre-made ping/health methods for free!
api_v1 = generate_api_v1()
jarvis_app.register_router(url='/api/v1',
                           router=api_v1)

# Run development server
jarvis_app.run()
```

<a name="endpoints"></a>
## Your First Endpoint
When using jarvis, it is easy to set up new endpoints.

The most basic layer is a `Router`, once you add your routes to your router, you can register it to your application:
```python
import json
from jarvis.app.api import Router

router = Router('v1')

@router.route(url='hello_world', method='GET')
def hello_world():
    return json.dumps({"hello": "world"})

jarvis_app.register_router(url='/api/v1',
                           router=router)
```

When using the decorator `@router.route(...)` you can add a new route to your router
By using `register_router`, you register the router under the specified url.

### Request Parameters
jarvis gives you an easy way to extract and validate your request-parameters:
```python
import json
from jarvis.app.api import Router, validate_params

router = Router('v1')

# Define a schema for the request body
schema = {'vector': {'type': 'list', 'schema': {'type': 'float'}}}

@router.route(url='predict', method='POST')
@validate_params(schema)
def predict(vector):
    prediction = my_model.predict_proba(vector)
    return json.dumps({"hello": "world"})

jarvis_app.register_router(url='/api/v1',
                           router=router)
```

jarvis uses `Cerberus` for schema validation, see https://docs.python-cerberus.org/en/stable/validation-rules.html for schema syntax


### Pre-Made API
Most of the time, your aplication may want a ping+health route, jarvis gives that for free:
```python
from jarvis.app.api import generate_api_v1, validate_params

api_v1 = generate_api_v1() # Returns a pre-made Router with /ping and /health
```
What's left? just register your own route in:
```python
@api_v1.route(url='predict', method='POST')
@validate_params(schema)
def predict(**params):
    # code

jarvis_app.register_router(url='/api/v1',
                           router=api_v1)
```

<a name="models"></a>
## Models
Implementing your inference business-logic is easy

For convinience reasons, you can inherit from JarvisModel class and override specifc methods:

```python
from jarvis.models import GenericModel

class SampleModel(GenericModel):
    def init(self, directory_path):
        load_path = os.path.join(directory_path, 'sample_model.pkl')
        with open(load_path, 'r') as f:
            # self.model should be defined here
            self.model = pickle.load(f)

    def infer(self, ...):
        # Implement
        pass

    # You can add as many methods as you wish, like pre-procssing methods & infer method...
```

jarvis will automatically `init` your model instance upon calling `jarvis_app.setup()`
```python
# Build a Jarvis Model instance
my_model = MyModel()

conf = JarvisConfiguration(service_name='sample_jarvis',
                           listen_port=1234,
                           # Make jarvis aware of your instance
                           models_instances=[my_model])

# Setup an application
# Jarvis will call `init` on your instance -> your model will be loaded here
jarvis_app = Jarvis(conf).setup()

# Get pre-made ping/health methods for free!
api_v1 = generate_api_v1()

# Add your prediction route
schema = {...}

@api_v1.route(url='predict', method='POST')
@validate_params(schema)
def predict(**params):
    probability = my_model.predict(**params)

    return json.dumps({'probability': probability})

jarvis_app.register_router(url='/api/v1',
                           router=api_v1)
```

<a name="logging"></a>
## Logging
You can access the logger in 2 way,
One way - you can get the logger with: `logging.getLogger(service_name)`
Another way - the logger is a member of your app: `jarvis_app.logger`
After you create your app, automatically a new logger is defined (named after your service):
```python
# Initialize configuration
conf = JarvisConfiguration(service_name='sample_jarvis',
                           listen_port=1234)

# Setup an application
jarvis_app = Jarvis(conf).setup()

# 1st way:
import logging
logger = logging.getLogger('sample_jarvis')
logger.info('Message 1')

# 2nd way:
jarvis_app.logger.info('Message 2')
```


<a name="cli_cmd"></a>
## CLI Commands
When installing jarvis, you get for free the CLI command `jarvis`
This command has utilities for both development and production.

Available commands:
* `jarvis test`
* `jarvis shell`
* `jarvis run dev/gunicorn`

The jarvis commands looks for your application in `app.py` by default, you can modify it by setting the environement variable: `JARVIS_APP`
