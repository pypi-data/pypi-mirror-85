# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['estrade',
 'estrade.enums',
 'estrade.graph',
 'estrade.graph.indicators',
 'estrade.mixins',
 'estrade.reporting']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.17,<0.18',
 'objgraph>=3.5.0,<4.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2020.4,<2021.0']

setup_kwargs = {
    'name': 'estrade',
    'version': '0.2.0',
    'description': 'Build, Backtest and Go Live your own trading bots',
    'long_description': '<h1 align="center">\n  <a href="https://github.com/cimourdain/estrade"><img src="https://github.com/cimourdain/estrade/raw/master/assets/logo.png" alt="Estrade" width="399"/></a><br>\n  <a href="https://github.com/cimourdain/estrade">Estrade</a>\n</h1>\n\n\n<div align="center">\n<a href="https://travis-ci.com/cimourdain/estrade">\n    <img src="https://travis-ci.com/cimourdain/estrade.svg?branch=master" alt="Build Status" />\n</a>\n<a href=\'https://estrade.readthedocs.io/en/latest\'>\n    <img src=\'https://readthedocs.org/projects/estrade/badge/?version=latest\' alt=\'Documentation Status\' />\n</a>\n<img src="https://badgen.net/badge/python/3.6,3.7,3.8?list=|" alt="python version" />\n<img src="https://badgen.net/badge/version/0.2.0" alt="current app version" />\n<a href="https://pypi.org/project/estrade/">\n    <img src="https://badgen.net/pypi/v/estrade" alt="PyPi version" />\n</a>\n<img src="https://badgen.net/badge/coverage/96%25" alt="Coverage" />\n<img src="https://badgen.net/badge/complexity/A%20%281.9210526315789473%29" alt="Complexity" />\n<a href="https://gitlab.com/pycqa/flake8">\n    <img src="https://badgen.net/badge/lint/flake8/purple" alt="Lint" />\n</a>\n<a href="https://github.com/ambv/black">\n    <img src="https://badgen.net/badge/code%20style/black/000" alt="Code format" />\n</a>\n<a href="https://github.com/python/mypy">\n    <img src="https://badgen.net/badge/static%20typing/mypy/pink" alt="Typing" />\n</a>\n<img src="https://badgen.net/badge/licence/GNU-GPL3" alt="Licence" />\n</div>\n\n\n# Backtest and run your trading strategies\n\nEstrade is a python library that allows you to easily backtest and run stock trading strategies at tick level.\n\nEstrade focus on providing tools so you mainly focus on your strategy definition.\n\n>  **WARNING**: Estrade is still in an alpha state of developpement and very unmature. Do not use it for other purposes than testing.\n\n## Features\n\nEstrade provides a **market environnement**, so you do not have to worry about\n - Trades result calculation\n - Indicators building & calculation (candle sets, graph indicators etc.)\n\nEstrade is build to be extended so you can define your own:\n- Strategies\n- Tick provider (to feed your backtests and/or live trading)\n- Indicators\n- Reporting\n\n\n## What Estrade does NOT provides\n\n- **Data**: You have to define your own data provider (live or static)\n- **Strategies**: Although some very basic (and useless) strategies are provided as examples in samples, Estrade does not provide any financially relevant strategy.\n\n\n## Documentation\n\n[Documentation](https://estrade.readthedocs.io/en/latest)\n',
    'author': 'Gabriel Oger',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/estrade/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
