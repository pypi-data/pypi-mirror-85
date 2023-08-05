# Copyright (C) 2019, 2020 Taler Systems SA
#
# This code is derived from code contributed to GNUnet e.V.
# by ng0 <ng0@n0.is>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE
# LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES
# OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
# ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
# THIS SOFTWARE.
#
# This file is in the public domain.
# SPDX-License-Identifier: 0BSD

from setuptools import setup, find_packages

with open('README', 'r') as f:
    long_description = f.read()

setup(
        name='taler-util',
        version='0.8.0-dev.1',
        license='LGPL3+',
        platforms='any',
        author='Taler Systems SA',
        author_email='ng0@taler.net',
        description='Util library for GNU Taler',
        long_description=long_description,
        url='https://git.taler.net/taler-util.git',
        packages=find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
            'Operating System :: OS Independent',
        ],
        python_requires='>=3.7',
)
