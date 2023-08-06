import os

from setuptools import setup

from src.PythonDebugTools import version




with open(os.path.abspath("README.md"), "r") as f:
    long_description = f.read()

data_files = [
        'PythonDebugTools/*.py'
        ]

setup(name='PythonDebugTools',
      version=version,
      packages=['PythonDebugTools'],
      url='https://github.com/Jakar510/PythonDebugTools',
      # download_url=f'https://github.com/Jakar510/PythonDebugTools/releases/tag/{version}',
      license='GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007',
      author='Tyler Stegmaier',
      author_email='tyler.stegmaier.510@gmail.com',
      description='A set of helpers for debugging Python 3.x.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=[],
      classifiers=[
              # How mature is this project? Common values are
              #   3 - Alpha
              #   4 - Beta
              #   5 - Production/Stable
              'Development Status :: 4 - Beta',

              # Indicate who your project is intended for
              'Intended Audience :: Developers',
              'Topic :: Software Development :: Build Tools',

              # Pick your license as you wish
              'License :: Free To Use But Restricted',

              # Support platforms
              'Operating System :: MacOS',
              'Operating System :: Microsoft :: Windows',
              'Operating System :: POSIX',

              'Programming Language :: Python :: 3',
              ],
      keywords='switch switch-case case',
      package_dir={ 'PythonDebugTools': 'src/PythonDebugTools' },
      package_data={
              'PythonDebugTools': data_files,
              },
      )
