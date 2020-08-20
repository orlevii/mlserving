---
sort: 3
---
## Running In Production
Although you can use `app.run()` in order start up your service, it is only recommended for local development.

We encourage to use `gunicron` for production use.

`gunicorn` with `gevent` is battle-tested works well for most use-cases:

#### Installation
`$ pip install gunicorn[gevent]`

#### Example
Serve your application: `app.py`:
```python
# app.py example

from mlserving import ServingApp
# other imports ...


app = ServingApp()
```

Run: `gunicorn -b 0.0.0.0:5000 -k gevent -w 4 app:app`

Read more [here](https://docs.gunicorn.org/en/stable/index.html)
