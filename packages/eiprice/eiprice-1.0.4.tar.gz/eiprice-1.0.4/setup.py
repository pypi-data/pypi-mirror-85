from setuptools import setup, find_packages
import os

list_dep = [
    'Unidecode',
    'nest_asyncio',
    'backoff',
    'requests-html',
    'user_agent'
]

setup(
    name='eiprice',
    version='1.0.4',
    install_requires=list_dep,
    python_requires='>=3.6',
    packages=find_packages()
)
