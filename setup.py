# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from src import __version__


setup(
    name='FairyBang',
    version=__version__,
    platform='linux',
    author='L',
    author_email='llawlietorigin@gmail.com',
    install_requires=[
        'pyTelegramBotAPI==3.6.7',
        'PySocks==1.7.1',
        'PyYaml==5.3.1',
        'SQLAlchemy==1.3.16',
        'psycopg2==2.8.5',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fairybang = src.__main__.main_loop'
        ]
    }
)
