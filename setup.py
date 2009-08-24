#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Dentist',
    version='0.1.0',
    description='Apache UserDir log separator',
    author='Alex Lee',
    author_email='lee@ccs.neu.edu',
    url='',
    package_dir={'': 'src'},
    packages=['dentist'],
    scripts=['scripts/dentist'],
    data_files=[('/etc/logrotate.d', ['logrotate/dentist'])],
)
