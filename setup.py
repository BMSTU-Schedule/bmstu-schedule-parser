from setuptools import setup

setup(
    name='bmstuSchedule',
    version='0.1.1-beta-4',
    author='George Gabolaev',
    author_email='gabolaev98@gmail.com',
    url='https://github.com/gabolaev/bmstuSchedule',
    license='MIT',
    python_requires='>=3.5',
    description='BMSTU EU Schedule iCal parser',
    packages=['bmstuSchedule','bmstuSchedule.configs'],
    install_requires=[
        'lxml',
        'bs4',
        'requests',
        ],
    entry_points={
        'console_scripts': [
            'bmstuSchedule = bmstuSchedule.__main__:main'
            ]
        },
    )
