# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiger_coins']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.0.0,<21.0.0',
 'funcy>=1.13,<2.0',
 'py-aiger-bv>=4.4.0,<5.0.0',
 'py-aiger-discrete>=0.1.2,<0.2.0',
 'py-aiger>=6.1.1,<7.0.0']

extras_require = \
{'bdd': ['py-aiger-bdd>=3.0.0,<4.0.0',
         'mdd>=0.3.4,<0.4.0',
         'numpy>=1.19.4,<2.0.0'],
 'sat': ['py-aiger-sat>=3.0.4,<4.0.0']}

setup_kwargs = {
    'name': 'py-aiger-coins',
    'version': '3.2.0',
    'description': 'Library for creating circuits that encode discrete distributions.',
    'long_description': "# py-aiger-coins\n\n**warning** 3.0.0 and greater are a **major** rewrite of this code\nbase. I am trying to port most of the useful features.\n\n\n[![Build Status](https://cloud.drone.io/api/badges/mvcisback/py-aiger-coins/status.svg)](https://cloud.drone.io/mvcisback/py-aiger-coins)\n[![codecov](https://codecov.io/gh/mvcisback/py-aiger-coins/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/py-aiger-coins)\n[![Updates](https://pyup.io/repos/github/mvcisback/py-aiger-coins/shield.svg)](https://pyup.io/repos/github/mvcisback/py-aiger-coins/)\n[![PyPI version](https://badge.fury.io/py/py-aiger-coins.svg)](https://badge.fury.io/py/py-aiger-coins)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n\nLibrary for creating circuits that encode discrete distributions and\nMarkov Decision Processes. The name comes from the random bit model of\ndrawing from discrete distributions using coin flips.\n\n<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->\n**Table of Contents**\n\n- [py-aiger-coins](#py-aiger-coins)\n- [Install](#install)\n- [Usage](#usage)\n\n<!-- markdown-toc end -->\n\n\n# Install\n\nTo install this library run:\n\n`$ pip install py-aiger-coins`\n\nNote that to actually compute probabilities, one needs to install with the bdd option.\n\n`$ pip install py-aiger-coins[bdd]`\n\nFor developers, note that this project uses the\n[poetry](https://poetry.eustace.io/) python package/dependency\nmanagement tool. Please familarize yourself with it and then run:\n\n`$ poetry install`\n\n# Usage\n\n`py-aiger-coins` extends the standard `py-aiger-bv` and\n`py-aiger-discrete` abstractions to allow for certain bits to be set\nvia **biased** coins.\n\nThe library centers around the `PCirc` object. The easiest way to use\n`py-aiger-coins` is to throught the `pcirc` function.\n\n\n```python\nimport aiger_bv as BV\nimport aiger_coins as C\n\n\nexpr1 = BV.uatom(2, 'x') + BV.uatom(2, 'y')\n\n# Create distribution over bits.\nmy_pcirc = C.pcirc(expr1) \\\n            .randomize({'x': {0: 1/6, 1: 2/6, 2: 3/6}})\n\nassert my_pcirc.outputs == {expr1.output}\n\n# This probablistic circuit uses 2 biased coins to represent this input.\nassert my_pcirc.num_coins == 2\nassert my_pcirc.coin_biases == (1/3, 1/2)\n\n# 'x' input is replaced with coinflips.\nassert my_pcirc.inputs == {'y'}\n\n# Underlying circuit now has a single input representing coin inputs.\nunderlying_circ = my_pcirc.circ\n\nassert underlying_circ.inputs == {'y', my_pcirc.coins_id}\n```\n\nNote that `aiger_coins.PCirc` implements the same API as `aiger_bv`\nand `aiger_coins`.\n\n## Sequential Circuit API\n\nFor example, sequential and parallel composition allow combining\nprobablistic circuits.\n\n```python\nincr = (BV.uatom(2, 'z') + 1)\nadder = (BV.uatom(2, 'x') + BV.uatom(2, 'y')).with_output('z')\n\n# Create distribution over bits.\npcirc = C.pcirc(adder)                                         \\\n         .randomize({'x': {0: 1/6, 1: 2/6, 2: 3/6}})\npcirc >>= incr\n```\n\nor\n\n```python\ninc_x = C.pcirc(BV.uatom(2, 'x') + 1)          \\\n         .randomize({'x': {0: 1/3, 2: 2/3}})                      # Pr(x=2) = 2/3\n\ninc_y = C.pcirc(BV.uatom(3, 'y') + 1)          \\\n         .randomize({'y': {0: 1/3, 5: 1/3, 3: 1/3}})\n\ninc_xy = inc_x | inc_y  #\n```\n\nSimilarly, `unroll`, `loopback` are also implemented.\n\n**note** `unroll` combines all coin flips into a *single* input in\ntemporal order.\n\n\n## Finite Functions\n\n`py-aiger-coins` also works well with the `py-aiger-discrete` API for\nworking with arbitrary functions over finite sets. For example:\n\n```python\nfrom bidict import bidict  # `pip install bidict`\n\n# Create encoder/decoder for dice.\nlookup = bidict({0: '⚀', 1: '⚁', 2: '⚂', 3: '⚃'})     # invertable dictionary.\nencoder = aiger_discrete.Encoding(decode=lookup.get, encode=lookup.inv.get)\n\n# Represent dice with a 2 bit vector.\nexpr1 = BV.uatom(2, '🎲')\n\n# Add encoded dice to x. Because why not.\nexpr2 = BV.uatom(2, 'x') + expr1\nfunc = aiger_discrete.from_aigbv(\n    expr2.aigbv, input_encodings={'🎲': encoder}\n)\n\n# Create distribution over bits.\ncirc = C.pcirc(func) \\\n        .randomize({'🎲': {'⚀': 1/6, '⚁': 2/6, '⚂': 3/6}})\n\nassert circ.inputs == {'x'}\nassert circ.outputs == {expr2.output}\nassert circ.coin_biases == (Fraction(1, 3), Fraction(1, 2))\n```\n",
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mvcisback/py-aiger-coins',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
