import os
import json
from .dict import DictFormatter


def _is_pretty_log():
    return bool(os.environ.get('PRETTY_LOG', False))


class JsonFormatter(DictFormatter):
    PRETTY_LOG_INDENTION = 4

    def format(self, record):
        message_json = super().format(record)
        indent = self.PRETTY_LOG_INDENTION if _is_pretty_log() else None

        return json.dumps(message_json, indent=indent)
