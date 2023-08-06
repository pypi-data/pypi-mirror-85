import setuptools

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="python_bitvavo_api",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version="1.2.1",
    author="Bitvavo",
    description="This is the python wrapper for the Bitvavo API",
    url="https://github.com/bitvavo/python-bitvavo-api",
    packages=setuptools.find_packages(),
    install_requires=[
        'websocket-client>=0.53.0',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
    ],
)