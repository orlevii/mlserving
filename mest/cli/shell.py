import click
from ._common import require_mest_app
import sys
import os


class Shell(object):
    @staticmethod
    def register(mest_cli):
        @mest_cli.command('shell', short_help='Run a shell in the app context.')
        @click.pass_context
        def shell(ctx):
            """Run an interactive Python shell in the context of a given
            Flask application.  The application will populate the default
            namespace of this shell according to it's configuration.
            This is useful for executing small snippets of management code
            without having to manually configure the application.
            """

            import code

            mest_app = require_mest_app(ctx)
            mest_app.load_models()
            app = mest_app.app

            banner = 'Python %s on %s\nApp: %s [%s]\nInstance: %s' % (
                sys.version,
                sys.platform,
                app.import_name,
                app.env,
                app.instance_path,
            )
            ctx_d = {}

            # Support the regular Python interpreter startup script if someone
            # is using it.
            startup = os.environ.get('PYTHONSTARTUP')
            if startup and os.path.isfile(startup):
                with open(startup, 'r') as f:
                    eval(compile(f.read(), startup, 'exec'), ctx_d)

            ctx_d.update(app.make_shell_context())

            code.interact(banner=banner, local=ctx_d)
