from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys


NAME = "compile-minifier"
VERSION = "0.1.4"


def readme():
    """print long description"""
    with open("README.md") as f:
        return f.read()


with open("requirements/base.txt") as f:
    REQUIRES = f.read().strip().split("\n")

with open("requirements/ci.txt") as f:
    CI_REQUIRES = f.read().strip().split("\n")


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = "verify that the git tag matches our version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG")

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name=NAME,
    version=VERSION,
    description="Python compiler and minifier",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author_email="contact@bimdata.io",
    url="https://github.com/bimdata/compile-minifier",
    install_requires=REQUIRES,
    extras_require={"ci": CI_REQUIRES,},
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.5, <4",
    include_package_data=True,
    entry_points={"console_scripts": ["compileminify=compileminify.main:entrypoint",],},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    cmdclass={"verify": VerifyVersionCommand,},
)
