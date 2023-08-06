# -*- coding: utf-8 -*-

from setuptools import setup


version = '1.0.7'


setup(
    name='pyfs-auth',
    version=version,
    keywords='Feishu Auth',
    description='Feishu Auth Module for Python.',
    long_description=open('README.rst').read(),

    url='https://github.com/feishu-sdk-python/pyfs-auth.git',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['pyfs_auth'],
    py_modules=[],
    install_requires=['pyfs-base>=1.0.3', 'pywe-exception', 'pywe-storage'],

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
