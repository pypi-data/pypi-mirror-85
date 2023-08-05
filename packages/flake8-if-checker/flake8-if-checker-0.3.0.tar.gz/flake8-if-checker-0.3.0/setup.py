import collections
import os
from setuptools import setup

CWD = os.path.abspath(os.path.dirname(__file__))

with open("README.md") as fobj:
    long_description = fobj.read()

setup(
    name="flake8-if-checker",
    version="0.3.0",
    author="Daniel Kuruc",
    author_email="daniel@kuruc.dev",
    license="MIT",
    url="https://github.com/danie1k/python-flake8-if-checker",
    project_urls=collections.OrderedDict(
        (
            ("Code", "https://github.com/danie1k/python-flake8-if-checker"),
            (
                "Issue tracker",
                "https://github.com/danie1k/python-flake8-if-checker/issues",
            ),
        )
    ),
    description="Flake8's IF statement complexity linter plugin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="pep8 flake8 conditional complexity",
    py_modules=("flake8_if_checker",),
    python_requires=">=2.7, <3.9",
    install_requires=("flake8>3.2.0",),
    extras_require={
        "lint": ("flake8>=3.0.0", "isort>=4.3.0", "pylint>=1.9.0"),
        "py3lint": ("black>=18.6b2", "mypy>=0.790", "typing"),
        "tests": ("coverage>=5.0", "mock", "pytest>=4.6.0", "pytest-sugar"),
    },
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: Flake8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    entry_points={"flake8.extension": ("IF0 = flake8_if_checker:IfChecker",)},
)
