## Health Check

```ServingApp``` allows to add additional `GET` route for handling health/ping requests

```python
from mlserving import ServingApp

app = ServingApp()

# Using the default health handler
app.add_health_handler('/ping')

app.run()
```

The default handler always returns `200 OK`

```ServingApp``` listens to SIGTERM signal, if SIGTERM signal was sent to the process, all the health routes will start returning `503` (Useful when making a graceful shutdown to the application)

### Custom Health Handlers

```app.add_health_handler``` 2nd argument is an handler, so you just need to implement one.

```python
from mlserving import ServingApp
from mlserving.health import HealthHandler, Healthy, Unhealthy

class CustomHealthHandler(HealthHandler):
        def health_check(self):
            if some_condition:
                return Unhealthy()
            return Healthy()

app = ServingApp()

# Using our custom health handler
app.add_health_handler('/ping', CustomHealthHandler())

app.run()
```
