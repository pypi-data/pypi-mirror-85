import setuptools
import os

__version__ = None
with open(os.path.join(os.path.dirname(__file__), 'apgsa', 'version.py')) as f:
    exec(f.read())

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apgsa",
    version=__version__,
    author="Kelvin Gao",
    author_email="89156201@qq.com",
    description="A wrapper around asyncpg for use with sqlalchemy core",
    long_description=long_description,
    url="https://github.com/kelvingao/apgsa",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='sqlalchemy asyncpg asyncio async',
    install_requires=['asyncpg', 'sqlalchemy'],
    python_requires='>=3.6',
)
