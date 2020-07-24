# Copyright (c) 2020 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.

import json

from setuptools import setup, find_packages


# Package dependencies
requires = [
    'requests',
    'pymongo==3.10.1'
]
test_requires = [
    'tox'
]

license_string = "Apache 2.0"

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

with open('version.json') as f:
    info = json.load(f)

setup(
    name='justice-augment-python-sdk',
    version=info['version'],
    description='Python SDK for Justice Augment',
    long_description=readme,
    long_description_content_type='text/markdown; variant=GFM',
    author='Bahrunnur',
    author_email='bahrunnur@accelbyte.io',
    url='https://bitbucket.org/accelbyte/justice-augment-python-sdk',
    license=license_string,
    packages=['justice', 'datastore'],
    install_requires=requires,
    tests_require=test_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
