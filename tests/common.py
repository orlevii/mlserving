import logging
from random import randint
from unittest.mock import MagicMock
from wsgiref import simple_server
from wsgiref.simple_server import WSGIRequestHandler

logging.getLogger('mlserving').disabled = True


def create_test_server(app):
    port = randint(1000, 9999)
    httpd = simple_server.make_server('0.0.0.0', port, app)
    WSGIRequestHandler.log_message = MagicMock()
    return httpd
