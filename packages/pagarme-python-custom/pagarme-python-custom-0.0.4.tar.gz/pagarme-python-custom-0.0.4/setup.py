# -*- coding: utf-8 -*-
import os
import re
from setuptools import setup, find_packages

__description__ = 'Pagar.me Python'
__long_description__ = 'Python library for Pagar.me API'

__author__ = 'Murilo Henrique, Victor Messina'
__author_email__ = 'suporte@pagar.me'
__special_things__ = 'Derek Stavis, Rodrigo Amaral'


testing_extras = [
    'pytest',
    'pytest-cov',
]


install_requires = open('requirements.txt').read().strip().split('\n')


setup(
    name='pagarme-python-custom',
    version='0.0.4',
    author=__author__,
    author_email=__author_email__,
    packages=find_packages(),
    license='MIT',
    description=__description__,
    long_description=__long_description__,
    special_things=__special_things__,
    url='https://github.com/alefhsousa/pagarme-python',
    keywords='Payment, pagarme',
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    tests_require=['pytest'],
    extras_require={
        'testing': testing_extras,
    },
)
