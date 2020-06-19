import setuptools

from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

# Pull version from source without importing
# since we can't import something we haven't built yet :)
exec(open('mest/version.py').read())

setup(
    # Needed to silence warnings (and to be pythona worthwhile package)
    name='mest',
    # Needed to actually package something
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=setuptools.find_packages(exclude='tests'),

    # Project URL
    url='https://github.com/orlevi111/mest',

    # author
    author='Or Levi',
    author_email='orlevi128@gmail.com',
    # Needed for dependencies
    install_requires=['Cerberus==1.3.*'],

    extras_require={
        'falcon': ['falcon==2.*']
    },

    # *strongly* suggested for sharing
    version=__version__,
    # The license can be anything you like
    # Choose your license
    license='LICENCE',

    description='A framework for developing a realtime model-inference service.',

    data_files=[('', ['README.md'])],

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: MacOS :: MacOS X',
                 'Operating System :: POSIX',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3 :: Only',
                 'Topic :: Internet',
                 'Topic :: Utilities',
                 'Topic :: Software Development :: Libraries :: Python Modules'
                 ],

    # We will also need a readme eventually (there will be a warning)
    long_description_content_type='text/markdown',

    long_description=long_description,

    entry_points={"console_scripts": ["mest = mest.cli:main"]}
)
