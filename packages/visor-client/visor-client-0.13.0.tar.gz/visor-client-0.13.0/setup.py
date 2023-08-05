#/usr/bin/python3

import setuptools

desc = 'Visor CI is a snapshotting hypervisor designed to speed up tests'

requirements = []
with open('requirements.txt', 'r') as f:
  requirements = f.readlines()

setuptools.setup(
  name='visor-client',
  version='0.13.0',
  author='Visor',
  author_email='serge@parsehub.com',
  description=desc,
  long_description=desc,
  url='https://parsehub.com',
  packages=setuptools.find_packages(),
  classifiers=[],
  python_requires='>=3.6',
  install_requires=requirements,
  py_modules = ['visor'],
  entry_points={
    'console_scripts': ['visor = visor:main'],
  },
)
