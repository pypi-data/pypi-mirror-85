import os
import re

from setuptools import find_packages, setup

# cf.
# https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-version
def read(*names, **kwargs):
    with open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8"),
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="jiradls",
    description="A JIRA command line interface for the DLS instance",
    license="BSD",
    url="https://github.com/DiamondLightSource/python-jira",
    author="Markus Gerstel",
    author_email="scientificsoftware@diamond.ac.uk",
    download_url="https://github.com/DiamondLightSource/python-jira/releases",
    version=find_version("jiradls", "__init__.py"),
    install_requires=[
        "colorama",
        "cryptography",
        "jira",
        "prompt_toolkit",
        "pyjwt",
    ],
    entry_points={
        "console_scripts": ["jira=jiradls.command_line:main"],
    },
    packages=find_packages(),
    python_requires=">=3.6",
    tests_require=["pytest"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Bug Tracking",
    ],
)
