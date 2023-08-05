from setuptools import setup, find_packages

setup(
    name='logger_lib',
    version='0.2.0',
    description='Logger Library for Gauge Test',
    packages=find_packages(),
    install_requires=['wheel', 'colorlog'],
)
