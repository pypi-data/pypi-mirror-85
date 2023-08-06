# -*- coding:utf-8 -*-
import os

from setuptools import find_packages, setup

from setup_commands.clean import CleanCommand
from setup_commands.protoc import ProtocCommand

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


with open("README.md") as fh:
    README = fh.read()


def scm_factory():
    from setuptools_scm.version import get_no_local_node  # pylint: disable=import-outside-toplevel

    def clean_scheme(version):
        """ Do not add commit hash to version."""
        return get_no_local_node(version)

    def distance_dev_version(version):
        """Do not try to guess and display next version number.

        Only add distance from previous tag.
        """
        if version.exact:
            return version.format_with("{tag}")

        return version.format_with("{tag}.dev{distance}")

    return {
        "local_scheme": clean_scheme,
        "version_scheme": distance_dev_version,
    }


setup(
    name="protobuf3-models",
    use_scm_version=scm_factory,
    description="Straightforward protobuf 3 handling through Python classes.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mlga/protobuf3-models",
    author="mlga",
    author_email="github@mlga.io",
    license="MIT",
    keywords="protobuf validation serialization",
    setup_requires=[
        "pytest-runner~=5.1",
        "setuptools_scm~=4.1",
    ],
    install_requires=[
        "protobuf~=3.9",
    ],
    tests_require=[
        "pytest~=6.1",
        "pytest-cov~=2.7",
        "pytest-html~=2.1",
    ],
    extras_require={
        "develop": [
            "isort~=5.6",
            "mypy==0.790",
            "pre-commit~=2.8",
            "pylint~=2.3",
            "pytest~=6.1",
            "pytest-cov~=2.7",
            "pytest-html~=2.1",
            "Sphinx==3.0.1",
            "sphinx-rtd-theme==0.4.3",
        ],
    },
    packages=find_packages(exclude=["tests*", "examples*"]),
    include_package_data=True,
    platforms="any",
    zip_safe=False,
    cmdclass={
        "clean": CleanCommand,
        "protoc": ProtocCommand,
    },
    python_requires=">=3.7",
)
