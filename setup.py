# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='FairyBang',
    version='0.1.1',
    platform='linux',
    author='L',
    author_email='llawlietorigin@gmail.com',
    install_requires=[
        'pyTelegramBotAPI==3.6.7',
        'PySocks==1.7.1',
        'PyYaml==5.4',
        'SQLAlchemy==1.3.16',
        'psycopg2==2.8.5',
        'aiohttp==3.6.2',
        'loguru==0.5.0',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fairybang = src.__main__:main_loop'
        ]
    }
)
