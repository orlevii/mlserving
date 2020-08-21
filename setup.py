from setuptools import setup

# Pull version from source without importing
# since we can't import something we haven't built yet :)
exec(open('mlserving/__version__.py').read())

setup(
    # Needed for dependency graph on GitHub
    install_requires=['falcon==2.*', 'validr==1.2.*'],

    # Package version - taken from code, cannot be in setup.cfg file
    version=__version__,
)
