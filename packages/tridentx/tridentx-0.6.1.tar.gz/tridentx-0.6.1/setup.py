from setuptools import setup, find_packages
from setuptools.extension import Library

from pkg_resources import get_distribution, DistributionNotFound
import subprocess
import distutils.command.clean
import distutils.spawn
import glob
import shutil
import os

with open("trident.rst", "r") as fh:
    long_description = fh.read()



NAME = "tridentx"
DIR = '.'
EXCLUDE_FROM_PACKAGES = ["tests", "examples"]
PACKAGES = find_packages(exclude=EXCLUDE_FROM_PACKAGES)


setup(name=NAME,
      version='0.6.1',
      description='Multiverse for Deep Learning Developers without Pitfall',
      long_description=long_description,
      author= 'Allan Yiin',
      author_email= 'allan@datadecision.ai',
      download_url= 'https://test.pypi.org/project/tridentx',
      license='MIT',
      install_requires=['numpy>=1.13.3',
                        'scikit-image >= 0.14',
                        'opencv-python>=3.2.0',
                        'matplotlib>=3.1.1',
                        'pillow >= 4.1.1',
                        'scipy>=1.2',
                        'six>=1.9.0',
                        'tqdm',
                        'pyyaml',
                        'h5py',
                        'requests'],
      extras_require={
          'visualize': ['pydot>=1.2.4'],
          'tests': ['pytest',
                    'pytest-pep8',
                    'markdown'],
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      python_requires='>=3',

      packages=PACKAGES,
      package_data={
        '': ['*.txt'], },
      include_package_data=True,
      scripts=[],

      )

