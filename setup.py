# setup files for the package
from setuptools import setup, find_packages

# read requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='bnbserver',
    version='0.1.0',
    description='Python package exposing a REST API to access the BNB data',
    author='Adrien Bufort',
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.6',
)

    