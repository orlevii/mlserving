## Running In Production
Although you can use <code>app.run()</code> in order start up your service, it is only recommended for local development.

We encourage to use <code>gunicron</code> for production use.

<code>gunicorn</code> with <code>gevent</code> is battle-tested works well for most use-cases:

#### Gunicorn Installation
`$ pip install gunicorn[gevent]`

#### Example
Serve your application: `app.py`:
```python
# app.py example

from mlserving import ServingApp
# other imports ...


app = ServingApp()
```

Run: <code>$ gunicorn -b 0.0.0.0:5000 -k gevent -w 4 app:app</code>

Read more [here](https://docs.gunicorn.org/en/stable/index.html)
