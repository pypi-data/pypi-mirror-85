# -*- coding: utf-8 -*-

from setuptools import setup


version = '1.0.3'


setup(
    name='pyfs-base',
    version=version,
    keywords='Feishu Base Class',
    description='',
    long_description=open('README.rst').read(),

    url='https://github.com/feishu-sdk-python/pyfs-base.git',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['pyfs_base'],
    py_modules=[],
    install_requires=['pywe-xml', 'requests'],

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
