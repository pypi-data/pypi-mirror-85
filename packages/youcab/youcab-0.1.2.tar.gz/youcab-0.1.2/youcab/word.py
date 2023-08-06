from typing import Dict, List, Optional, Union


class Word:
    """
    Word of the morphological analysis result.
    """

    ATTRS = ("surface", "pos", "base", "c_type", "c_form")

    def __init__(
        self,
        surface: str,
        pos: List[str],
        base: Optional[str] = None,
        c_type: Optional[str] = None,
        c_form: Optional[str] = None,
    ) -> None:
        """Initialize the attributes of a word.

        Notes
        -----
        If the word has a conjugation, ``c_type`` and ``c_form`` must be given together.

        Parameters
        ----------
        surface : str
            Surface form.
        pos : list of str
            Classification list of parts of speech.
        base : str, optional
            Base form (the default is ``surface``, meaning there is no conjugation for
            this word).
        c_type : str, optional
            Conjugation type which is called "活用型" in Japanese (the default is ``""``,
            meaning there is no conjugation for this word).
        c_form : str, optional
            Conjugation form which is called "活用形" in Japanese (the default is ``""``,
            meaning there is no conjugation for this word).

        Examples
        --------
        >>> japan = Word(surface="日本", pos=["名詞", "固有名詞", "地名", "国"])
        >>> assert japan.surface == "日本"
        >>> assert japan.pos == ["名詞", "固有名詞", "地名", "国"]
        >>> assert japan.base == "日本"
        >>> assert japan.c_type == ""
        >>> assert japan.c_form == ""

        >>> move = Word("動け", ["動詞", "一般"], base="動く", c_type="五段-カ行", c_form="命令形")
        >>> assert move.surface == "動け"
        >>> assert move.pos == ["動詞", "一般"]
        >>> assert move.base == "動く"
        >>> assert move.c_type == "五段-カ行"
        >>> assert move.c_form == "命令形"
        """
        self.surface = surface
        self.pos = pos

        if base is not None:
            self.base = base
        else:
            self.base = surface

        if c_type is not None and c_form is not None:
            self.c_type = c_type
            self.c_form = c_form
        else:
            self.c_type = ""
            self.c_form = ""

    def to_dict(self) -> Dict[str, Union[str, List[str]]]:
        """Convert this word to a ``dict`` object.

        Returns
        -------
        dict
            The attributes of this word.
        """
        return {attr: getattr(self, attr) for attr in self.ATTRS}

    def __str__(self) -> str:
        """Represent this word as a string.

        Returns
        -------
        str
            A string representing the attributes of this word.
        """
        return str(self.to_dict())
