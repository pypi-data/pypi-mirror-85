# YouCab: Converts MeCab Parsing Results to Python Objects

[![PyPI Version](https://img.shields.io/pypi/v/youcab.svg)](https://pypi.org/pypi/youcab/)
[![Python Versions](https://img.shields.io/pypi/pyversions/youcab.svg)](https://pypi.org/pypi/youcab/)
[![License](https://img.shields.io/pypi/l/youcab.svg)](https://github.com/poyo46/youcab/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## Installation

**Install MeCab**

MeCab is required for YouCab to work.
If it is not already installed, [install MeCab](https://taku910.github.io/mecab/) first.

**Install YouCab**

```console
$ pip install youcab
```

## Tokenize Japanese sentence

In this example code, we generate a tokenizer with MeCab's default dictionary and run tokenization.
The tokenizer converts text into a list of [Word](https://github.com/poyo46/youcab/blob/main/youcab/word.py) objects.

```python
from youcab import youcab

tokenize = youcab.generate_tokenizer()
words = tokenize("本を読んだ")
for word in words:
    print("surface: " + word.surface)
    print("pos    : " + str(word.pos))
    print("base   : " + word.base)
    print("c_type : " + word.c_type)
    print("c_form : " + word.c_form)
    print("")

```

```console
surface: 本
pos    : ['名詞', '一般']
base   : 本
c_type : 
c_form : 

surface: を
pos    : ['助詞', '格助詞', '一般']
base   : を
c_type : 
c_form : 

surface: 読ん
pos    : ['動詞', '自立']
base   : 読む
c_type : 五段・マ行
c_form : 連用タ接続

surface: だ
pos    : ['助動詞']
base   : だ
c_type : 特殊・タ
c_form : 基本形

```

## Available for any MeCab dictionary

Dictionaries such as IPAdic, [UniDic](https://unidic.ninjal.ac.jp/) and [neologd](https://github.com/neologd/mecab-ipadic-neologd) are available.

```python
from youcab import youcab

tokenize = youcab.generate_tokenizer(dicdir="/path/to/mecab/dic/dir/")
```
