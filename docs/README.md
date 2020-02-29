# Mest
ML Models on REST.

A framework for developing a realtime model-inference service.

Allows you to set up an inference-endpoint for you ML Model easily.

Mest uses `Flask` for creating a lightweight WSGI web application, designed to run on Kubernetes

## Table of Contents:
1. [Installation](#intallation)
2. [Basic Setup](#basic_setup)
3. [Your First Endpoint](#endpoints)
4. [Models](#models)
5. [Logging](#logging)
6. [CLI Commands](#cli_cmd)

<a name="intallation"></a>
## Installation

* Run: `pip install mest`


<a name="basic_setup"></a>
## Basic Setup
```python
from mest.app import Mest, MestConfig
from mest.app.api import Router

# Initialize configuration
conf = MestConfig(service_name='sample_mest',
                  listen_port=1234)

# Setup an application
mest_app = Mest(conf).setup()

# Create a Router and add routes to it
api_v1 = Router('v1')

mest_app.register_router(url='/api/v1',
                         router=api_v1)

# Run development server
mest_app.run()
```

<a name="endpoints"></a>
## Your First Endpoint
When using mest, it is easy to set up new endpoints.

The most basic layer is a `Router`, once you add your routes to your router, you can register it to your application:
```python
import json
from mest.app.api import Router

router = Router('v1')

@router.route(url='hello_world', method='GET')
def hello_world():
    return json.dumps({"hello": "world"})

mest_app.register_router(url='/api/v1',
                         router=router)
```

When using the decorator `@router.route(...)` you can add a new route to your router
By using `register_router`, you register the router under the specified url.

### Request Parameters
mest gives you an easy way to extract and validate your request-parameters:
```python
import json
from mest.app.api import Router, validate_params

router = Router('v1')

# Define a schema for the request body
schema = {'vector': {'type': 'list', 'schema': {'type': 'float'}}}

@router.route(url='predict', method='POST')
@validate_params(schema)
def predict(vector):
    prediction = my_model.predict_proba(vector)
    return json.dumps({"probability": prediction})

mest_app.register_router(url='/api/v1',
                         router=router)
```

mest uses `Cerberus` for schema validation, see https://docs.python-cerberus.org/en/stable/validation-rules.html for schema syntax

<a name="models"></a>
## Models
Implementing your inference business-logic is easy

For convinience reasons, you can inherit from MestModel class and override specifc methods:

```python
import os
import pickle
from mest.models import GenericModel

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

mest will automatically `init` your model instance upon calling `mest_app.setup()`
```python
# Build a Mest Model instance
my_model = MyModel()

conf = MestConfig(service_name='sample_mest',
                  listen_port=1234,
                  # Make mest aware of your instance
                  models_instances=[my_model])

# Setup an application
# Mest will call `init` on your instance -> your model will be loaded here
mest_app = Mest(conf).setup()

api_v1 = Router('v1')

# Add your prediction route
schema = {...}

@api_v1.route(url='predict', method='POST')
@validate_params(schema)
def predict(**params):
    probability = my_model.predict(**params)

    return json.dumps({'probability': probability})

mest_app.register_router(url='/api/v1',
                         router=api_v1)
```

<a name="logging"></a>
## Logging
You can access the logger in 2 way,
One way - you can get the logger with: `logging.getLogger(service_name)`
Another way - the logger is a member of your app: `mest_app.logger`
After you create your app, automatically a new logger is defined (named after your service):
```python
# Initialize configuration
conf = MestConfig(service_name='sample_mest',
                  listen_port=1234)

# Setup an application
mest_app = Mest(conf).setup()

# 1st way:
import logging
logger = logging.getLogger('sample_mest')
logger.info('Message 1')

# 2nd way:
mest_app.logger.info('Message 2')
```


<a name="cli_cmd"></a>
## CLI Commands
When installing mest, you get for free the CLI command `mest`
This command has utilities for both development and production.

Available commands:
* `mest test`
* `mest shell`
* `mest run dev/gunicorn`

The mest commands looks for your application in `app.py` by default, you can modify it by setting the environement variable: `MEST_APP`
