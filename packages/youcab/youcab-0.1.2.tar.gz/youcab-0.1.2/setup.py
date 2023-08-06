# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['youcab']

package_data = \
{'': ['*']}

install_requires = \
['mecab-python3>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'youcab',
    'version': '0.1.2',
    'description': 'Converts MeCab parsing results to Python objects.',
    'long_description': '# YouCab: Converts MeCab Parsing Results to Python Objects\n\n[![PyPI Version](https://img.shields.io/pypi/v/youcab.svg)](https://pypi.org/pypi/youcab/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/youcab.svg)](https://pypi.org/pypi/youcab/)\n[![License](https://img.shields.io/pypi/l/youcab.svg)](https://github.com/poyo46/youcab/blob/main/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\n## Installation\n\n**Install MeCab**\n\nMeCab is required for YouCab to work.\nIf it is not already installed, [install MeCab](https://taku910.github.io/mecab/) first.\n\n**Install YouCab**\n\n```console\n$ pip install youcab\n```\n\n## Tokenize Japanese sentence\n\nIn this example code, we generate a tokenizer with MeCab\'s default dictionary and run tokenization.\nThe tokenizer converts text into a list of [Word](https://github.com/poyo46/youcab/blob/main/youcab/word.py) objects.\n\n```python\nfrom youcab import youcab\n\ntokenize = youcab.generate_tokenizer()\nwords = tokenize("本を読んだ")\nfor word in words:\n    print("surface: " + word.surface)\n    print("pos    : " + str(word.pos))\n    print("base   : " + word.base)\n    print("c_type : " + word.c_type)\n    print("c_form : " + word.c_form)\n    print("")\n\n```\n\n```console\nsurface: 本\npos    : [\'名詞\', \'一般\']\nbase   : 本\nc_type : \nc_form : \n\nsurface: を\npos    : [\'助詞\', \'格助詞\', \'一般\']\nbase   : を\nc_type : \nc_form : \n\nsurface: 読ん\npos    : [\'動詞\', \'自立\']\nbase   : 読む\nc_type : 五段・マ行\nc_form : 連用タ接続\n\nsurface: だ\npos    : [\'助動詞\']\nbase   : だ\nc_type : 特殊・タ\nc_form : 基本形\n\n```\n\n## Available for any MeCab dictionary\n\nDictionaries such as IPAdic, [UniDic](https://unidic.ninjal.ac.jp/) and [neologd](https://github.com/neologd/mecab-ipadic-neologd) are available.\n\n```python\nfrom youcab import youcab\n\ntokenize = youcab.generate_tokenizer(dicdir="/path/to/mecab/dic/dir/")\n```\n',
    'author': 'poyo46',
    'author_email': 'poyo4rock@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/poyo46/youcab',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
