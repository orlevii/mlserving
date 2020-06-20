import logging
import os
import signal
import sys
from http import HTTPStatus
from typing import Union
from wsgiref import simple_server

from .api import Response
from .app.state import runtime_state
from .webframeworks import WebFramework, WebFrameworkFactory

os.environ.setdefault('MEST_APP', 'app.py')


class Mest(object):
    def __init__(self,
                 framework: Union[str, WebFramework] = 'falcon'):
        if isinstance(framework, WebFramework):
            self.web_framework = framework
        else:
            self.web_framework = WebFrameworkFactory.create(framework)

        self._logger = self.__init_logger()
        self._handle_sigterm(self.logger)

        err_handler = self.get_default_error_handler()
        self.web_framework.set_error_handler(err_handler)

    # def setup(self):
    #     if self.__is_cli:
    #         self._expose_app_for_gunicorn()
    #         return self
    #     if self._setup:
    #         return self
    #
    #     _handle_sigterm(self.logger)
    #     _register_error_handler(self.app)
    #
    #     self._setup = True
    #
    #     return self

    def run(self, host='0.0.0.0', port=5000):
        with simple_server.make_server(host, port, self.web_framework.app) as httpd:
            self.logger.info(f'Running development server on: http://{host}:{port}/')
            self.logger.warning(f'NOTICE! Running development on production environment is not recommended.')
            httpd.serve_forever()

    @property
    def logger(self):
        return self._logger

    @property
    def __is_cli(self) -> bool:
        cli = os.environ.get('MEST_CLI', '')

        return cli.lower() == 'true'

    @staticmethod
    def __init_logger():
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
        stdout_handler.setFormatter(formatter)

        logger = logging.getLogger('mest')
        logger.setLevel(logging.INFO)
        logger.addHandler(stdout_handler)
        return logger

    def _expose_app_for_gunicorn(self):
        main_app_module = os.environ.get('MEST_APP').split('.')[0]
        main_module = __import__(main_app_module)
        main_module.app = self.app

    @staticmethod
    def _handle_sigterm(logger):
        def sigterm_handler(_signum, _frame):
            logger.info('SIGTERM ACCEPTED')
            runtime_state.set_to_shutting_down()

        signal.signal(signal.SIGTERM, sigterm_handler)

    def get_default_error_handler(self):
        def handler(e: Exception) -> Response:
            self.logger.exception(e)
            return Response(data={'message': str(e)},
                            status=HTTPStatus.INTERNAL_SERVER_ERROR)

        return handler
