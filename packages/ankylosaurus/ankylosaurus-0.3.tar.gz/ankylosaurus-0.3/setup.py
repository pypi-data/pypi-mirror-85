import os
import sys
from distutils.sysconfig import get_python_lib

from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("Unsupported Python version, need at least %s " %REQUIRED_PYTHON)
    sys.exit(1)

VERSION='0.3'

setup(
    name='ankylosaurus',
    version=VERSION,
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    #url='https://www.djangoproject.com/',
    author='Matteo Giani',
    author_email='matteo.giani.87@gmail.com',
    description=('Various utils.'),
    #long_description=read('README.rst'),
    #license='BSD',
    packages=find_packages(),
    include_package_data=True,
    #scripts=['django/bin/django-admin.py'],
    entry_points={},
    install_requires=['pylint'
                      ],
    extras_require={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    project_urls={
    },
)
