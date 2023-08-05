# coding: utf-8

import codecs
import os
import sys

from setuptools import setup

if sys.version_info.major < 3:
    stools = 'setuptools<=42.0.2'
else:
    stools = 'setuptools'

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='yandex_tracker_client',
    version='1.9',
    description='Client for Yandex.Tracker',
    #long_description_content_type='text/plain',
    author='Yandex Team',
    author_email='smosker@yandex-team.ru',
    url='https://github.com/yandex/yandex_tracker_client',
    #long_description=read('README.rst'),
    packages=['yandex_tracker_client'],
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 2',
                 ],
    keywords='python yandex.tracker api-client',
    python_requires='>=2.7',
    install_requires=[
        'requests[security]>=2.0',
        stools,
        'six>=1.9',
    ]
)
