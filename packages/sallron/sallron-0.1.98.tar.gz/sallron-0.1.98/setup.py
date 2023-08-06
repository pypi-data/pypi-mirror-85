#!/usr/bin/env python

# PyPi publish flow
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload dist/*

from setuptools import setup, find_packages
from os.path import join, dirname

here = dirname(__file__)

_VERSION = '0.1.98'

setup(name='sallron',
      version=_VERSION,
      description="Collected data middleware for DB.",
      long_description=open(join(here, 'README.rst')).read(),
      license='proprietary',
      author='elint-tech',
      author_email='contato@elint.com.br',
      url='https://github.com/elint-tech/sallron/',
      download_url = 'https://github.com/elint-tech/e-raptor/dist/sallron-' + _VERSION + 'tar.gz',
      install_requires=list(map(
        lambda string: string.strip("\n"),
        open("requirements.txt", "r")
      )),
      packages=find_packages(),
      keywords = ['sallron', 'sauron', 'data-middleware', 'data-aggregator', 'pymongo',
      'schedule', 'walrus'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',
        'Topic :: Software Development',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Utilities',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
      ],
      )