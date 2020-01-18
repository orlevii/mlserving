import setuptools

from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

# Pull version from source without importing
# since we can't import something we haven't built yet :)
exec(open('jarvis/version.py').read())

setup(
    # Needed to silence warnings (and to be pythona worthwhile package)
    name='jarvis',
    # Needed to actually package something
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=setuptools.find_packages(exclude='tests'),

    # Project URL
    url='https://github.com/orlevi111/jarvis',

    # author
    author='Or Levi',
    author_email='orlevi128@gmail.com',
    # Needed for dependencies
    install_requires=['Flask==1.1.*', 'cerberus==1.3.*', 'gunicorn==19.*',
                      'python-dotenv==0.10.*', 'click==7.*'],
    # *strongly* suggested for sharing
    version=__version__,
    # The license can be anything you like
    # Choose your license
    license='LICENCE',

    description='Core implementation of the Jarvis Framework',

    data_files=[('', ['README.md'])],

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=['Programming Language :: Python :: 3'],

    # We will also need a readme eventually (there will be a warning)
    long_description_content_type='text/markdown',

    long_description=long_description,

    entry_points={"console_scripts": ["jarvis = jarvis.cli:main"]}
)
