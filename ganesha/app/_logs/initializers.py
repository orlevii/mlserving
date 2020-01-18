import logging
import sys

from .enrichment import get_request_info
from .formatters import JsonFormatter


def get_stdout_handler(app_name):
    formatter = JsonFormatter(app_name, enrichment_methods=dict(request_info=get_request_info))
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(logging.WARNING)

    return handler
