# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysketcher',
 'pysketcher.backend',
 'pysketcher.backend.matplotlib',
 'pysketcher.composition']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0', 'numpy>=1.18.2,<2.0.0', 'scipy>=1.4.1,<2.0.0']

entry_points = \
{'console_scripts': ['beam1 = examples.beam1:main']}

setup_kwargs = {
    'name': 'pysketcher',
    'version': '0.0.3',
    'description': 'Geometric Sketching Utility for Python',
    'long_description': '============\n PySketcher\n============\n.. image:: https://api.codeclimate.com/v1/badges/eae2c2aa97080fbfed7e/maintainability\n    :target: https://codeclimate.com/github/rvodden/pysketcher/maintainability\n\n.. image:: https://api.codeclimate.com/v1/badges/eae2c2aa97080fbfed7e/test_coverage\n    :target: https://codeclimate.com/github/rvodden/pysketcher/test_coverage\n\n.. image:: https://circleci.com/gh/rvodden/pysketcher.svg?style=shield\n    :target: https://app.circleci.com/pipelines/github/rvodden/pysketcher\n\n.. image:: https://readthedocs.org/projects/pysketcher/badge/?version=latest&style=flat\n    :target: https://pysketcher.readthedocs.io/en/latest/\n.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n    :target: https://github.com/pre-commit/pre-commit\n\n.. image:: https://img.shields.io/badge/hypothesis-tested-brightgreen.svg\n    :target: https://hypothesis.readthedocs.io/\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\n.. image:: https://api.dependabot.com/badges/status?host=github&repo=rvodden/pysketcher\n    :target: https://dependabot.com\n\n**This is alpha software - the interface is likely to change with every release prior to 0.1.0.**\n\nTool for creating sketches of physical and mathematical problems in terms of Python code.\n\nThis library is very heavily based on the thinking of Hans Petter Langtangen however\nvery little if any of his code remains. Significant deviations from his library are:\n\n1. The MatlibplotDraw object is no longer global and is no longer tightly coupled to the shape object. There is now a DrawingTool interface which this class implements.\n\n2. Code is organised into multiple files and published on pypi.\n\n3. Shapes are immutable. This means functions such as ``rotate`` return modified copies of the original shape, rather than altering the shape on which they are called.\n\n4. Angles are in radians not degrees.\n\n5. The Composition object is used more consistently. Previously objects such as Beam where direct children of Shape which led to code repetition.\n\n`Please see the documentation for more information <https://pysketcher.readthedocs.io/en/latest/index.html>`_.\n',
    'author': 'Richard Vodden',
    'author_email': 'richard@vodden.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rvodden/pysketcher',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
