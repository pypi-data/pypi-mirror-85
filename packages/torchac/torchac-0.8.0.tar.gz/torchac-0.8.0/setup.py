from setuptools import setup

with open('README.md', 'r') as f:
  long_description = f.read()

setup(
  name='torchac',
  packages=['torchac'],
  version='0.8.0',
  author='fab-jul',
  author_email='fabianjul@gmail.com',
  description='Fast Arithmetic Coding for PyTorch',
  long_description=long_description,
  long_description_content_type='text/markdown',
  python_requires='>=3.6',
  url='https://github.com/fab-jul/torchac')
