# !/usr/bin/env/python
# -*- coding:utf-8 -*-


""" 
 Auth:  david <hsioe_david@aliyun.com>
 Date:  2020/11/10


 Desc
    HsioeFlask version 0.0.1 打包
"""

import setuptools

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='HsioeFlask',
    version='0.0.5',
    keywords='Flask, Hsioe, Web',
    author='hsioe',
    author_email='hsioe_david@aliyun.com',
    description='A Simple Flask Business Api Frame!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'flask==1.0.2',
        'flask-restplus==0.13.0',
        'cached-property==0.1.1',
        'werkzeug==0.15.0'
    ]
)
1