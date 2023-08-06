#!/usr/bin/python3

import large_index
from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    "requests>=2",
    "click",
]

setup(
  name = "large-index",
  version = large_index.__version__,
  author = "Anton Turko",
  author_email = "anton_turko@mail.ru",
  url = "https://github.com/antohhh93/large_index",
  description = "Rollover big indexes ilm in Elasticsearch",
  long_description = readme,
  long_description_content_type = "text/markdown",
  packages = find_packages(),
  install_requires = requirements,
  license = "MIT",
  classifiers = [
      "Programming Language :: Python :: Implementation",
      "Programming Language :: Python :: 3",
      "Natural Language :: English",
      "License :: OSI Approved :: MIT License"
  ],
  entry_points = {
    "console_scripts": [
        "large-index = large_index.main:cli",
    ],
  },
)
