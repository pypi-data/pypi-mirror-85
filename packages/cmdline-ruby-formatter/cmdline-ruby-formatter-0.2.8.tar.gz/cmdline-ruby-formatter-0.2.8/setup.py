# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('RubyFormatter/formatter.py').read(),
    re.M
).group(1)

with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="cmdline-ruby-formatter",
    packages=["RubyFormatter"],
    entry_points={
        "console_scripts": ['RubyFormatter = RubyFormatter.formatter:main']
    },
    version=version,
    description="Python command line application bare bones template.",
    long_description=long_descr,
    author="Lipsky Danial",
    author_email="lipsky787@gmail.com",
    url="",
)