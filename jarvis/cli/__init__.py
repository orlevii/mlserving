import os
import sys

import click

from ._common import require_app_module, APP_PATH
from .run import Run
from .shell import Shell
from .test import Test


def main():
    sys.path.insert(0, os.getcwd())

    os.environ.setdefault('JARVIS_CLI', 'true')
    obj = {}
    try:
        main_app = __main_app()
        obj['app'] = main_app
    except Exception as e:
        obj['err'] = e

    jarvis_cli(obj=obj)


@click.group()
def jarvis_cli():
    pass


def __main_app():
    import importlib.util

    if os.path.isfile(APP_PATH):
        spec = importlib.util.spec_from_file_location('jarvis_app', APP_PATH)
        app_main = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_main)
        return app_main


Run.register(jarvis_cli)
Test.register(jarvis_cli)
Shell.register(jarvis_cli)
