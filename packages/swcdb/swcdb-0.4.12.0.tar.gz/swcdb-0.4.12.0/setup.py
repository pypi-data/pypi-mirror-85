# -*- coding: utf-8 -*-

import os
import sys
from distutils.core import setup, Extension
from distutils import sysconfig

with open('README.md') as readme:
    long_description = readme.read()


install_path = '/opt/swcdb'
include_dirs = [install_path+'/include',
                sysconfig.get_python_inc(plat_specific=True),
                '/usr/local/include', '/usr/include'] + \
                ''.split(';') + \
                ''.split(';') + \
                '/usr/local/include'.split(';')
include_dirs = list(set(include_dirs))

extra_compile_args = [a for a in set([a.strip() 
                      for a in " -D_LARGEFILE_SOURCE -m64 -D_FILE_OFFSET_BITS=64 -DASIO_STANDALONE -DASIO_NO_DEPRECATED -Wall -Werror -Wextra -Wformat -Wformat-security -O3 -flto -fuse-linker-plugin -ffat-lto-objects  -D_LARGEFILE_SOURCE -m64 -D_FILE_OFFSET_BITS=64 -Wall -Werror -Wformat -Wformat-security -O3 -flto -fuse-linker-plugin -ffat-lto-objects".split(' ')]) if a]

libraries=[l.split('/')[-1].split('.')[0][3:] 
           for l in '/usr/local/lib/libtcmalloc_minimal.so'.split(';') 
           if '/' in l]

extensions = []


setup(
    name='swcdb',
    version='0.4.12.0',
    description='The SWC-DB Python Package',
    long_description=long_description,
    long_description_content_type='text/markdown',

    # install_requires=['thrift==0.13.0'],

    url='https://github.com/kashirin-alex/swc-db',
    license='GPLv3',
    package_dir={'swcdb': 'swcdb'},
    packages=[
        'swcdb',
        'swcdb.thrift',
        'swcdb.thrift.native',
        'swcdb.thrift.tornado',
        'swcdb.thrift.twisted',
        'swcdb.thrift.zopeif'
    ],
    maintainer='Kashirin Alex',
    maintainer_email='kashirin.alex@gmail.com',
    ext_modules=extensions,
    
    classifiers=(
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Environment :: Console",
        "Framework :: Twisted",
        "Framework :: Zope",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Zope",
        
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Database :: Front-Ends",
        "Topic :: Scientific/Engineering",
    ),
    platforms=['any'],
)


# /
# setup.py
# swcdb/
#    __init__.py
#    thrift/
#         __init__.py
#         service.py
#         native/
#         tornado/
#         twisted/
#         zopeif/
#
