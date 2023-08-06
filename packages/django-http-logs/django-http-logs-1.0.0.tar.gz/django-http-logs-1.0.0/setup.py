"""
Author:     LanHao
Date:       2020/11/17
Python:     python3.6

"""

import os
from setuptools import find_packages, setup

with open('README.rst', "r") as readme:
    README = readme.read()

# allow setup.py to be run from any path
# os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-http-logs',
    version='1.0.0',
    packages=["django_http_logs"],  # find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='django logs ',
    long_description=README,
    author='bigpangl',
    author_email='bigpangl@163.com',
    setup_requires=[
        "django",
        "celery",
        "django-rest-framework"
    ],
)
