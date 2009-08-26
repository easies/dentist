#!/usr/bin/env python

from distutils.core import setup, Extension

setup(
    name='Dentist',
    version='0.2.0',
    description='Apache UserDir log separator',
    author='Alex Lee',
    author_email='lee@ccs.neu.edu',
    url='',
    ext_package='dentist',
    ext_modules=[Extension('_inotify', ['src/dentist/_inotify.c'])],
    package_dir={'': 'src'},
    packages=['dentist'],
    scripts=['scripts/dentist'],
    data_files=[('/etc/logrotate.d', ['logrotate/dentist']),
                ('/etc/init.d', ['init/dentist'])],
)
