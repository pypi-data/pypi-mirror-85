# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linlearn']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.1,<4.0',
 'numba>=0.48,<0.49',
 'numpy>=1.17.4,<2.0.0',
 'scikit-learn>=0.22,<0.23',
 'scipy>=1.3.2,<2.0.0',
 'tqdm>=4.36,<5.0']

setup_kwargs = {
    'name': 'linlearn',
    'version': '0.1',
    'description': 'linlear is a python package for machine learning with linear methods, including robust methods',
    'long_description': '\n[![Build Status](https://travis-ci.com/linlearn/linlearn.svg?branch=master)](https://travis-ci.com/linlearn/linlearn)\n[![Documentation Status](https://readthedocs.org/projects/linlearn/badge/?version=latest)](https://linlearn.readthedocs.io/en/latest/?badge=latest)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/linlearn)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/linlearn)\n[![GitHub stars](https://img.shields.io/github/stars/linlearn/linlearn)](https://github.com/linlearn/linlearn/stargazers)\n[![GitHub issues](https://img.shields.io/github/issues/linlearn/linlearn)](https://github.com/linlearn/linlearn/issues)\n[![GitHub license](https://img.shields.io/github/license/linlearn/linlearn)](https://github.com/linlearn/linlearn/blob/master/LICENSE)\n[![Coverage Status](https://coveralls.io/repos/github/linlearn/linlearn/badge.svg?branch=master)](https://coveralls.io/github/linlearn/linlearn?branch=master)\n\n![linlearn](img/linlearn.png)\n\n# linlearn: linear methods in Python\n\nLinLearn is scikit-learn compatible python package for machine learning with linear methods. \nIt includes in particular alternative "strategies" for robust training, including median-of-means for classification and regression.\n\n[Documentation](https://linlearn.readthedocs.io) | [Reproduce experiments](https://linlearn.readthedocs.io/en/latest/linlearn.html) |\n\nLinLearn simply stands for linear learning. It is a small scikit-learn compatible python package for **linear learning** \nwith Python. It provides :\n\n- Several strategies, including empirical risk minimization (which is the standard approach), \nmedian-of-means for robust regression and classification\n- Several loss functions easily accessible from a single class (`BinaryClassifier` for classification and `Regressor` for regression)\n- Several penalization functions, including standard L1, ridge and elastic-net, but also total-variation, slope, weighted L1, among many others\n- All algorithms can use early stopping strategies during training\n- Supports dense and sparse format, and includes fast solvers for large sparse datasets (using state-of-the-art stochastic optimization algorithms) \n- It is accelerated thanks to numba, leading to a very concise, small, but very fast library\n  \n## Installation\n\nThe easiest way to install linlearn is using pip\n\n    pip install linlearn\n\nBut you can also use the latest development from github directly with\n\n    pip install git+https://github.com/linlearn/linlearn.git\n\n## References\n',
    'author': 'Stéphane Gaïffas',
    'author_email': 'stephane.gaiffas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://linlearn.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
