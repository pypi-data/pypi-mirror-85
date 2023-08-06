from setuptools import setup, Extension
from torch.utils.cpp_extension import BuildExtension, CppExtension


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
    return ''.join(long_description_lines)


setup(
  name='torchac',
  packages=['torchac'],
  # ext_modules=[CppExtension(
  #   name='torchac_backend',
  #   sources=['torchac/torchac_backend.cpp']),
  # ],
  # cmdclass={'build_ext': BuildExtension.with_options(use_ninja=True)},
  # scripts=['torchac/torchac_backend.cpp'],
  data_files=[('backend', ['torchac/backend/torchac_backend.cpp', 'torchac/backend/important_data.json'])],
  version='0.8.9',
  author='fab-jul',
  author_email='fabianjul@gmail.com',
  description='Fast Arithmetic Coding for PyTorch',
  long_description=_get_long_description(),
  long_description_content_type='text/markdown',
  python_requires='>=3.6',
  url='https://github.com/fab-jul/torchac')
