#    sizzlews
#    Copyright (C) 2020 Dmitry Berezovsky
#    The MIT License (MIT)
#    
#    Permission is hereby granted, free of charge, to any person obtaining
#    a copy of this software and associated documentation files
#    (the "Software"), to deal in the Software without restriction,
#    including without limitation the rights to use, copy, modify, merge,
#    publish, distribute, sublicense, and/or sell copies of the Software,
#    and to permit persons to whom the Software is furnished to do so,
#    subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from os import path
from setuptools import setup, find_packages

import sizzlews.__version__

src_dir = path.abspath(path.dirname(__file__))
root_dir = path.join(src_dir, '..')

version = sizzlews.__version__.__version__

readme_file = path.join(root_dir, 'README.md')

try:
    from m2r import parse_from_file

    long_description = parse_from_file(readme_file)
except ImportError:
    # m2r may not be installed in user environment
    with open(readme_file) as f:
        long_description = f.read()

setup(
    name='ws-sizzle',
    # Semantic versioning should be used:
    # https://packaging.python.org/distributing/?highlight=entry_points#semantic-versioning-preferred
    version=version,
    description='Lightweight library for streamlining JSON RPC client and server creating. '
                'Supports WebSockets and HTTP transport',
    long_description=long_description,
    url='https://github.com/corvis/ws-sizzle',
    keywords='json, json-rpc, rpc, jsonrpc, jsonrpc-websockets, bidirectional-jsonrpc',
    # Author
    author='Dmitry Berezovsky',

    # License
    license='MIT',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',

        # License (should match "license" above)
        'License :: OSI Approved :: MIT License',
        # Python versions support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],

    # Structure
    packages=find_packages(include=['sizzlews', 'sizzlews.*']),

    # Mandatory requirements
    install_requires=[
        'json-rpc>=1.13.0',
        'pydantic>=1.6',
        'typing>=3.6',
    ],
    # Extra dependencies might be installed with:
    # pip install ws-sizzle[tornado,websockets,etc]
    extras_require={
        'tornado': ['tornado'],
        'websockets': ['websockets'],
        'requests-client': ['requests'],
        'aiohttp': ['aiohttp']
    },

)
