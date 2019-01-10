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


if __name__ == "__main__":
    setup(
        name='oradump',
        author='Sdykov Dauren',
        version='1.0',
        py_modules=['oradump'],
        install_requires=read_requirements('requirements.txt'),
        description='Just a package for simple extracting data from Oracle database',
    )
