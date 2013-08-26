import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here, "readme.txt")).read()
changelog = open(os.path.join(here, "changelog")).read()
requires = [
    "peewee>=0.7.4", #maybe
]

setup(name='pyramid_peewee',
      version='0.0',
      description='peewee for pyramid',
      long_description=readme + "\n\n" + changelog, 
      packages=find_packages(), 
      install_requires=requires,
      test_suite="pyramid_peewee.tests"
      )
