import os
import sys

import click


class Test(object):
    @staticmethod
    def register(mest_cli):
        @mest_cli.command(name='test', help='Run unit tests')
        def test():
            if not os.path.isdir('./tests'):
                click.echo('Could not find "tests" package,' +
                           ' please make sure "tests" exists and is importable (contains __init__.py)')
                sys.exit(1)

            os.environ.setdefault('FLASK_ENV', 'testing')

            import unittest
            loader = unittest.TestLoader()
            tests = loader.discover('./tests', pattern="*.py")
            test_runner = unittest.runner.TextTestRunner(verbosity=2)
            result = test_runner.run(tests)

            has_errors = any(result.errors + result.failures)
            code = -1 if has_errors else 0

            return sys.exit(code)
