# coding=utf-8
import sys

from setuptools import find_packages
from setuptools import setup

assert sys.version_info[0] == 3 and sys.version_info[1] >= 5, "aparat requires Python 3.5 or newer"

setup(
    name='aparat',
    version='0.0.1',
    py_modules=['aparat'],
    description='useful utility library for python',
    author='Talha Buğra Bulut',
    author_email='talhabugrabulut@gmail.com',
    long_description=open('README.md').read(),
    packages=find_packages(exclude=("venv",)),
    install_requires=[
        'python-dateutil==2.8.1',
        'pytz==2020.4',
        'validate-email==1.3'
    ])
