from setuptools import find_packages, setup
import madeira_postgres

import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='madeira_postgres',
    version=madeira_postgres.__version__,
    description='PostgreSQL operation wrappers tied in to AWS Secrets Manager via madeira',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mxmader/madeira-postgres",
    author='Joe Mader',
    author_email='jmader@jmader.com',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=['*.tests', '*.tests.*']),
    install_requires=[
        'madeira'
        'psycopg2-binary'
    ]
)
