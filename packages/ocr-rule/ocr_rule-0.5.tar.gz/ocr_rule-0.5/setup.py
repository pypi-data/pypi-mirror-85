from setuptools import setup, find_packages
from ocr_rule import *
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ocr_rule',  # Required
    version=version,  # Required
    description='qoala ocr rule',  # Required
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='qoala-ai-team',  # Optional
    author_email='fatchur.rahman@qoala.id', #optional
    packages=["ocr_rule"],  # Required
)
