from setuptools import setup

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rifbot',
    version='0.59',
    packages=['rifbot'],
    # scripts=['rifbot'],
    url='https://www.riftrading.com',
    license='',
    author='riftrading',
    author_email='admin@riftrading.com',
    description='Python API for Riftrading Rifbot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'websockets',
        'requests',
        'shortid'
    ],
)
