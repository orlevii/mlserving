import os
import sys

import click

from jarvis.app.jarvis_conf import Environment
from ._common import require_jarvis_app, APP_PATH


class Run(object):
    @staticmethod
    def register(jarvis_cli):
        @jarvis_cli.group(name='run', help='Run development/gunicorn server')
        def run():
            os.environ['JARVIS_CLI'] = 'false'

        @run.command(name='dev', help='Run development server')
        @click.option('--debug/--no-debug', default=False)
        @click.pass_context
        def dev(ctx, debug):
            if debug:
                os.environ.setdefault('FLASK_ENV', Environment.DEVELOPMENT)
            os.environ.setdefault('PRETTY_LOG', 'true')
            jarvis = require_jarvis_app(ctx)
            jarvis.setup()
            jarvis.run()

        @run.command(name='gunicorn', help='Run gunicorn server')
        @click.pass_context
        def gunicorn(ctx):
            jarvis = require_jarvis_app(ctx)
            listen_port = int(jarvis.config.listen_port)

            cmd = 'gunicorn -w 1 -b 0.0.0.0:{listen_port} {app_module}:app --graceful-timeout 30'.format(
                listen_port=listen_port,
                app_module=__parse_app_module())
            exit_code = os.system(cmd)
            sys.exit(exit_code)

        def __parse_app_module():
            return APP_PATH.split('.')[0]
