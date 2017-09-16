# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pydown',
    version='0.1.0',
    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='Zhijian Huang',
    author_email='zjhuang.davis@gmail.com',
    url='https://github.com/kennethreitz/samplemod',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[],

    entry_points={
        'console_scripts': [
            'pydown = pydown.__main__:main'
            ]
        },
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
)
