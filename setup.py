#! -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from alask import __version__

setup(name='alask',
      version='%d.%d.%d' % __version__,
      author='Kang Hyojun',
      author_email='hyojun@admire.kr',
      install_requires=[
          'flask==0.10.1', 'flask-script==0.5.3', 'sqlalchemy==0.8.2',
          'alembic==0.6.0', 'pytest==2.3.5',
      ],
      packages=find_packages(),
      entry_points={
          'console_scripts': ['alaskic = alask.script:run']
      })
