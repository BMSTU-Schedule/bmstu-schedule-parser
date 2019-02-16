# bmstu-schedule-parser
# Copyright (C) 2018 BMSTU Schedule (George Gabolaev)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

setup(
    name='bmstu-schedule',
    version='1.4.3',
    author='George Gabolaev',
    author_email='gabolaev98@gmail.com',
    url='https://github.com/BMSTU-Schedule/bmstu-schedule-parser',
    license='AGPLv3',
    python_requires='>=3.5',
    long_description_content_type='text/markdown',
    description='BMSTU EU Schedule iCal parser',
    long_description=open('README.md').read(),
    packages=['bmstu_schedule', 'bmstu_schedule.configs'],
    install_requires=[
        'lxml',
        'bs4',
        'requests',
        'termcolor'
    ],
    entry_points={
        'console_scripts': [
            'bmstu-schedule = bmstu_schedule.__main__:main'
        ]
    },
)
