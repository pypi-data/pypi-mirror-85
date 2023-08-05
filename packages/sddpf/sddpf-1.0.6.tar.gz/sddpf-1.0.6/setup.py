#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="sddpf",
    version='1.0.6',
    author='lcfevr',
    author_email='lcfevr@163.com',
    url='https://github.com/lcfevr/sentry-dingding-feelys',
    description='A Sentry extension which send errors stats to DingDing',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    keywords='sentry dingding',
    include_package_data=True,
    zip_safe=False,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'sentry>=9.0.0',
        'requests',
    ],
    entry_points={
        'sentry.plugins': [
            'sddpf = sentry_dingding.plugin:DingDingPlugin'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
        "License :: OSI Approved :: MIT License",
    ]
)
