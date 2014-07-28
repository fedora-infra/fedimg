#!/bin/env python
# -*- coding: utf8 -*-

from setuptools import setup, find_packages

setup(
    name='fedimg',
    version='0.2.1',
    description='A service that listens to the Fedmsg bus and'
                ' automatically uploads built Fedora cloud images'
                ' to internal and external cloud providers.',
    classifiers=[
        "Programming Language :: Python :: 2",
        " License :: OSI Approved :: GNU Affero General Public License"
        " v3 or later (AGPLv3+)",
    ],
    keywords='python Fedora cloud image uploader service',
    author='David Gay',
    author_email='oddshocks@riseup.net',
    url='https://github.com/fedora-infra/fedimg',
    license='AGPLv3+',
    include_package_data=True,
    zip_safe=False,
    install_requires=["fedmsg",
                      "apache-libcloud",
                      "paramiko"],
    tests_require=['nose'],
    packages=find_packages(),
    entry_points="""
    [moksha.consumer]
    kojiconsumer = fedimg.consumers:KojiConsumer
    """,
)
