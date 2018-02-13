from setuptools import setup

setup(
    name='bmstu-schedule',
    version='0.1.1-beta-6',
    author='George Gabolaev',
    author_email='gabolaev98@gmail.com',
    url='https://github.com/gabolaev/bmstuSchedule',
    license='MIT',
    python_requires='>=3.5',
    description='BMSTU EU Schedule iCal parser',
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
