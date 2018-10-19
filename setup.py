from setuptools import setup

setup(
    name='bmstu-schedule',
    version='1.1.8',
    author='George Gabolaev',
    author_email='gabolaev98@gmail.com',
    url='https://github.com/BMSTU-Schedule/bmstu-schedule-parser',
    license='MIT',
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
