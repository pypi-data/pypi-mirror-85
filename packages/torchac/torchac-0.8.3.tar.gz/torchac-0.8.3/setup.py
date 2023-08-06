from setuptools import setup, Extension


def _get_long_description():
  with open('README.md', 'r') as f:
    long_description_lines = []
    skip = False
    for line in f:
      if '<div>' in line:
        skip = True
      if '</div>' in line:
        skip = False
      if skip:
        print('Skipping', line)
        continue
      long_description_lines.append(line)
    return '\n'.join(long_description_lines)


setup(
  name='torchac',
  packages=['torchac'],
  # scripts=['torchac/torchac_backend.cpp'],
  package_data={
    'torchac': ['torchac/torchac_backend.cpp']
  },
  version='0.8.3',
  author='fab-jul',
  author_email='fabianjul@gmail.com',
  description='Fast Arithmetic Coding for PyTorch',
  long_description=_get_long_description(),
  long_description_content_type='text/markdown',
  python_requires='>=3.6',
  url='https://github.com/fab-jul/torchac')
