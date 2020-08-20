import setuptools

from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

# Pull version from source without importing
# since we can't import something we haven't built yet :)
exec(open('mlserving/__version__.py').read())

setup(
    name='mlserving',
    packages=setuptools.find_packages(exclude=['tests*', 'examples*']),

    # Project URL
    url='https://github.com/orlevii/mlserving',

    # Author
    author='Or Levi',
    author_email='orlevi128@gmail.com',
    # Needed for dependencies
    install_requires=['falcon==2.*', 'validr==1.2.*'],

    # Package version
    version=__version__,
    license='MIT',
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
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3 :: Only',
                 'Topic :: Internet',
                 'Topic :: Utilities',
                 'Topic :: Software Development :: Libraries :: Python Modules'
                 ],

    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    long_description=long_description
)
