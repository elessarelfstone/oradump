import os
from setuptools import setup


def read_requirements(filename):
    try:
        with open(filename) as f:
            result = [line.rstrip() for line in f]
    except IOError:
        raise IOError(os.getcwd())
    else:
        return result

setup(
    name='OracleDataDump',
    version='1.0',
    py_modules=['oradump'],
    install_requires=read_requirements('requirements.txt'),
    entry_points='''
        [console_scripts]
        oradump=oradump.cli:cli
    ''',
)