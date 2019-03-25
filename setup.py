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


def read_long_description():
    with open("README.md", "r", encoding="utf8") as fh:
        long_description = fh.read()
    return long_description


if __name__ == "__main__":
    setup(
        name='oradump',
        author='Dauren Sdykov',
        url="https://github.com/elessarelfstone/oradump",
        version='1.0.0',
        packages=['oradump'],
        install_requires=read_requirements('requirements.txt'),
        long_description=read_long_description(),
        long_description_content_type="text/markdown",
        description='Just a package for simple extracting data from Oracle database',
    )
