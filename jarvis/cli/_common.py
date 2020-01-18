import os
import sys
import traceback

import click

from jarvis.app import Jarvis

APP_PATH = os.environ.get('JARVIS_APP')


def require_app_module(ctx):
    error = ctx.obj.get('err')
    if error is not None:
        click.echo('An error occurred while trying to load "{}":'.format(APP_PATH))
        click.echo(error)
        click.echo()
        click.echo(''.join(traceback.format_tb(error.__traceback__)))
        sys.exit(-1)

    app = ctx.obj.get('app')
    if app is None:
        click.echo(f'"{APP_PATH}" could not be found, make sure you run the command from the root directory')
        sys.exit(-1)
    elif app.jarvis_app is None:
        click.echo(f'could not found jarvis application instance under ${APP_PATH}')
        sys.exit(-1)

    return app


def require_jarvis_app(ctx) -> Jarvis:
    return require_app_module(ctx).jarvis_app
