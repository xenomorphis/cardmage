#!/usr/bin/env python3

"""
cardmage setup module
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# with open(path.join(here, 'README.md'), encoding='utf-8') as f:
# long_description = f.read()

setup(
    name='cardmage',
    version='0.0.1',
    description='FOSS build tool for playing cards',
    long_description='FOSS build tool for printable playing cards',
    url='https://github.com/condla/pokepy',
    author='Marco R. Wachter',
    author_email='stefan.dun@gmail.com',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache License',
        'Programming Language :: Python :: 3.10',
    ],

    keywords='Pokeapi REST client wrapper command line interface',
    packages=find_packages(),
    install_requires=['toml', 'wand'],
    extras_require={ },
    package_data={},
    data_files=[],

    entry_points={
        'console_scripts': [
            'cardmage = cardmage:cl_main',
        ],
    },
)
