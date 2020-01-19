"""
When using Ganesha CLI, it will look for "app.py" in the current directory

To play around, name this file "app.py", or run:
$ export GANESHA_APP=custom_cli.py

To see all available commands:
$ ganesha --help
Now you can run your "$ ganesha hello" command
-----------------------
"""
from ganesha.app import Ganesha, GaneshaConfig
from ganesha.cli import ganesha_cli


def register_cli_commands():
    # See click for more options
    @ganesha_cli.command(name='hello', help='Prints hello world to the console')
    def hello():
        print('hello world!')

    @ganesha_cli.command(name='download_models', help='Download latest version of the model')
    def download_models():
        # You can implement a CLI command for downloading the models from your storage.
        # Models should be placed under "_models" directory
        pass


conf = GaneshaConfig(service_name='test_ganesha',
                     listen_port=1234)

# This one is required for the CLI to work correctly
ganesha_app = Ganesha(conf).setup()

register_cli_commands()

if __name__ == '__main__':
    ganesha_app.run()


