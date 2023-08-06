#!/usr/bin/env python
# -*-coding:utf-8-*-


from setuptools import setup, find_packages
import os
import my_python_module

REQUIREMENTS = []
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='my_python_module',
    version=my_python_module.__version__,
    description='a general purpose python module.',
    url='https://github.com/a358003542/my_python_module',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='wanze',
    author_email='a358003542@gmail.com',
    maintainer='wanze',
    maintainer_email='a358003542@gmail.com',
    license='MIT',
    platforms='Linux, windows',
    keywords=['python'],
    classifiers=['License :: OSI Approved :: MIT License',
                 'Operating System :: Microsoft',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python :: 3'],
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    install_requires=REQUIREMENTS,
)
