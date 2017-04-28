# -*- coding: utf-8 -*-
import re
from os import path
from setuptools import find_packages, setup

ROOT_DIR = path.abspath(path.dirname(__file__))

DESCRIPTION = 'Sanic-CookieSession - Simple Cookie-based Session for Sanic'
LONG_DESCRIPTION = open(path.join(ROOT_DIR, 'README.rst')).read()
VERSION = re.search(
    "__version__ = '([^']+)'",
    open(path.join(ROOT_DIR, 'sanic_cookiesession', '__init__.py')).read()
).group(1)


setup(
    name='Sanic-CookieSession',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='https://github.com/pyx/sanic-cookiesession/',
    author='Philip Xu and contributors',
    author_email='pyx@xrefactor.com',
    license='BSD-New',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        'itsdangerous',
        'sanic',
    ],
    extras_require={
        'dev': [
            'aiohttp',
            'flake8',
            'pytest',
            'pytest-cov',
            'Sphinx',
            'tox',
            'twine',
        ],
    },
    zip_safe=False,
    platforms='any',
)
