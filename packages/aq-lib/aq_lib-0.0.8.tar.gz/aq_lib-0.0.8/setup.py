import setuptools

try: # for pip >= 10
    from pip._internal.req import parse_requirements
    from  pip._internal.network.session import PipSession
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
    from pip.download import PipSession

from aq_lib import __version__

from setuptools import setup
import os
import re

requires = [
    "amqp==2.2.2",
    "enum34==1.1.6",
    "jsonpickle==0.9.5",
    "kombu==4.2.1",
    "vine==1.1.4",
    "redis==2.10.6",
    "requests==2.22.0",
]


setup(name='aq_lib',
      version=__version__,
      description='public lib for arquants',
      url='https://gitlab.com/arquants/aq-lib.git',
      author='ArQuants',
      author_email='info@arquants.trading',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=requires,
      zip_safe=False
)
