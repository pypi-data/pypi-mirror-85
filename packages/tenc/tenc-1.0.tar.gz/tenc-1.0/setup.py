
#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tenc',
      version='1.0',
      description='A small package to de- and encrypt strings',
      author='Philip Stapelfeldt',
      author_email='p.stapelfeldt@nanogiants.de',
      packages=find_packages(exclude=["tests"]),
      entry_points={
              'console_scripts': [
                  'tenc = tenc.cli:main',
              ],
      },
      install_requires=[
          'PyCryptodome',
      ],
      python_requires='>=3.6'
      )
