#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")
    ) as fh:
        return fh.read()


setup(
    name="coinflip",
    version="0.1.0",
    description="Randomness testing for humans",
    long_description="%s\n%s"
    % (
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
            "", read("README.rst")
        ),
        re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
    ),
    author="Matthew Barber",
    author_email="quitesimplymatt@gmail.com",
    url="https://github.com/Honno/coinflip",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"templates": ["templates/*.html", "templates/randtests/*.html"]},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: BSD License",
        "Topic :: Utilities",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries",
        "Environment :: Console",
    ],
    project_urls={
        "Documentation": "https://coinflip.readthedocs.io/",
        "Changelog": "https://coinflip.readthedocs.io/en/latest/changelog.html",
        "Issue Tracker": "https://github.com/Honno/coinflip/issues",
    },
    keywords=[
        "rng",
        "prng",
        "randomness",
        "nist",
        "statistics",
        "tests",
        "randomness-testing",
        "cryptography",
        "rngtest",
        "diehard",
        "TestU01",
        "pandas",
        "scipy",
        "cli",
        "data-science",
    ],
    python_requires=">=3.7",
    install_requires=[
        "click",
        "numpy",
        "scipy",
        "python-slugify",
        "pandas",
        "tabulate",
        "rich>=6.1.0",
        "jinja2",
        "altair",
        "typing-extensions",
        "more-itertools",
    ],
    test_requires=["pytest", "hypothesis"],
    entry_points={"console_scripts": ["coinflip = coinflip.cli.commands:main"]},
)
