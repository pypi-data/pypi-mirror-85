# Copyright © 2020 Matthew Burkard
#
# This file is part of Language Formatters
#
# Language Formatters is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Language Formatters is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Language Formatters.  If not, see
# <https://www.gnu.org/licenses/>.
from setuptools import setup

setup(
    name='languageformatters',
    version='0.0.4',
    url='https://gitlab.com/mburkard/language-formatters',
    license='GNU General Public License v3 (GPLv3)',
    author='Matthew Burkard',
    author_email='matthewjburkard@gmail.com',
    description='A collection of formatters for various languages.',
    package_dir={'': 'src'},
    packages=['languageformatters'],
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    zip_safe=False
)
