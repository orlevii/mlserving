import json

from falcon import Request, Response

from mest.app.health import get_app_health
from mest.models import BaseModel


class HealthResource:
    def __init__(self, model: BaseModel):
        self.model = model

    def on_get(self, _: Request, res: Response):
        health_resp = get_app_health([self.model])

        res.status = health_resp.status_string
        res.body = json.dumps(health_resp.text)
