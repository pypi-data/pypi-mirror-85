import os

from setuptools import setup
from setuptools import find_packages

here = os.path.join(os.path.dirname(__file__))

__version__ = None
with open(os.path.join(here, 'hackle', 'version.py')) as _file:
    exec(_file.read())

with open(os.path.join(here, 'requirements', 'sdk.txt')) as _file:
    REQUIREMENTS = _file.read().splitlines()

setup(
    name='hackle-sdk',
    version=__version__,
    author='Hackle',
    author_email='developers@hackle.io',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=REQUIREMENTS,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
