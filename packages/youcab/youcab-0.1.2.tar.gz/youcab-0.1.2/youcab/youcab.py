import os
import re
from typing import Callable, List, Optional

import MeCab

from .errors import InvalidTokenizerError, NotFoundNodeFormatError
from .word import Word


def _mecab_tagger(
    dicdir: Optional[str] = None,
    node_format: Optional[str] = None,
    unk_format: Optional[str] = None,
) -> MeCab.Tagger:
    """Generate MeCab.Tagger

    Notes
    -----
    ``dicdir`` can also be specified as the environment variable ``MECAB_DICDIR``.

    Parameters
    ----------
    dicdir : str, optional
        Path of MeCab dictionary directory (the default is to not specify).
    node_format : str, optional
        MeCab ``node_format`` (the default is to not specify).
    unk_format : str, optional
        MeCab ``unk_format`` (the default is to not specify).

    Returns
    -------
    MeCab.Tagger
        MeCab.Tagger with optional arguments.

    See Also
    --------
    ``mecab --help``
    """
    options = []

    if dicdir is not None:
        options.append("--dicdir=" + dicdir)
    elif os.getenv("MECAB_DICDIR") is not None:
        options.append("--dicdir=" + os.getenv("MECAB_DICDIR"))

    if node_format is not None:
        options.append("--output-format-type=")  # Dealing with the MeCab bug.
        options.append("--node-format=" + node_format)

    if unk_format is not None:
        options.append("--unk-format=" + unk_format)

    return MeCab.Tagger(" ".join(options))


def _find_index(
    items: List[str], equal_to: Optional[str] = None, include: Optional[str] = None
) -> Optional[int]:
    """Find the index of the first item in an array that satisfies a particular
    condition.

    Parameters
    ----------
    items : list of str
        Search target.
    equal_to : str, optional
        If specified, this function will search the item matching ``equal_to``.
    include : str, optional
        If specified, this function will search the item containing ``include``.

    Returns
    -------
    int or None
        index, or None if not found.
    """
    for i, item in enumerate(items):
        if equal_to is not None and item == equal_to:
            return i
        if include is not None and include in item:
            return i
    return None


def _auto_node_format(dicdir: Optional[str] = None) -> Optional[str]:
    """Find the MeCab ``node_format`` automatically.

    Parameters
    ----------
    dicdir : str, optional
        Path of MeCab dictionary directory (the default is to not specify).

    Returns
    -------
    str or None
        MeCab ``node_format``, or None if not found.

    Raises
    ------
    NotFoundNodeFormatError
        If the ``node-format`` could not be set automatically.
    """
    tagger = _mecab_tagger(dicdir=dicdir, node_format=r"%H\\n")

    text = "こおりつけ"
    csv = tagger.parse(text).splitlines()[0]
    items = re.split(r"[\t,]", csv)
    if items[0] == text:
        items = items[1:]

    pos_i = _find_index(items, equal_to="動詞")
    base_i = _find_index(items, equal_to="こおりつく")
    c_type_i = _find_index(items, include="五段")
    c_form_i = _find_index(items, include="命令")

    if any([i is None for i in (pos_i, base_i, c_type_i, c_form_i)]):
        msg = (
            "Please configure ``node-format`` manually to match the format "
            + r"``node-format=surface,pos,baseForm,cType,cForm\\n``"
        )
        raise NotFoundNodeFormatError(msg)

    node_format = (
        ",".join(
            [
                r"%m",  # surface
                f"%F-[{pos_i},{pos_i + 1},{pos_i + 2},{pos_i + 3}]",  # pos
                f"%f[{base_i}]",  # baseForm
                f"%f[{c_type_i}]",  # cType
                f"%f[{c_form_i}]",  # cForm
            ]
        )
        + r"\\n"
    )

    return node_format


def check_tokenizer(tokenize: Callable[[str], List[Word]]) -> None:
    """Check that the tokenize function is working properly.

    Parameters
    ----------
    tokenize : function
        Tokenize function.

    Returns
    -------
    None
        Return None when the tokenize function is working properly.

    Raises
    ------
    InvalidTokenizerError
        If the tokenize function is not working properly.
    """
    tokens = ["楽しい", "本", "を", "よく", "読み", "ます"]
    conj_tokens = ["楽しい", "読み", "ます"]
    words = tokenize("".join(tokens))
    if len(words) != len(tokens):
        raise InvalidTokenizerError
    for word, token in zip(words, tokens):
        if word.surface != token:
            raise InvalidTokenizerError
        if "詞" not in word.pos[0]:
            raise InvalidTokenizerError
        if word.base == "":
            raise InvalidTokenizerError
        if word.c_type != "" and word.surface not in conj_tokens:
            raise InvalidTokenizerError


def generate_tokenizer(
    dicdir: Optional[str] = None, node_format: Optional[str] = None
) -> Callable[[str], List[Word]]:
    """Generate a function that converts the text into a list of Word objects.

    Parameters
    ----------
    dicdir : str, optional
        Path of MeCab dictionary directory (the default is delegated to MeCab).
    node_format : str, optional
        MeCab ``node_format`` that matches the format
        ``node-format=surface,pos,baseForm,cType,cForm\\n``.
        If not specified, YouCab will try to set it automatically.

    Returns
    -------
    function
        A function that converts the text into a list of Word objects.

    See Also
    --------
    youcab.word.Word :
        A class that represents each word.

    Examples
    --------
    >>> tokenize = generate_tokenizer()
    >>> words = tokenize("毎日とても歩きます")
    >>> assert [word.surface for word in words] == ["毎日", "とても", "歩き", "ます"]
    >>> assert [word.base for word in words if word.pos[0] == "動詞"] == ["歩く"]
    """
    if node_format is None:
        node_format = _auto_node_format(dicdir)

    mecab_tagger = _mecab_tagger(dicdir=dicdir, node_format=node_format)

    blank = ("", " ", "　")

    def _tokenize(text: str) -> List[Word]:
        parsed = mecab_tagger.parse(text)

        if parsed is None:
            return [Word(surface=text, pos=["名詞"])]

        nodes = parsed.splitlines()[:-1]

        words = []
        for node in nodes:
            attrs = node.split(",")

            surface = attrs[0]
            pos = attrs[1].split("-")
            base = attrs[2]
            c_type = attrs[3]
            c_form = attrs[4]

            if c_type in blank and c_form in blank:
                word = Word(surface=surface, pos=pos, base=base)
            else:
                word = Word(
                    surface=surface, pos=pos, base=base, c_type=c_type, c_form=c_form
                )

            words.append(word)

        return words

    check_tokenizer(_tokenize)

    return _tokenize
