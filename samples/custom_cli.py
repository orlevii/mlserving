"""
When using Mest CLI, it will look for "app.py" in the current directory

To play around, name this file "app.py", or run:
$ export MEST_APP=custom_cli.py

To see all available commands:
$ mest --help
Now you can run your "$ mest hello" command
-----------------------
"""
from mest.app import Mest, MestConfig
from mest.cli import mest_cli


def register_cli_commands():
    # See click for more options
    @mest_cli.command(name='hello', help='Prints hello world to the console')
    def hello():
        print('hello world!')

    @mest_cli.command(name='download_models', help='Download latest version of the model')
    def download_models():
        # You can implement a CLI command for downloading the predictors from your storage.
        # Models should be placed under "_models" directory
        pass


conf = MestConfig(service_name='test_mest',
                  listen_port=1234)

# This one is required for the CLI to work correctly
mest_app = Mest(conf).setup()

register_cli_commands()

if __name__ == '__main__':
    mest_app.run()
