from pdf2txt.utils import get_fonts, fix_sentences
from enum import Enum, auto
from typing import Callable, Dict, List, Set, Optional, Union, TYPE_CHECKING
from pdf2txt.exceptions import NoTokenFoundError
from collections import Counter
import re
from typing import Iterable,Iterator
from itertools import chain
from pdf2txt.utils import rect_to_edges, line_to_edge
class TokenOrdering(Enum):
    """
    A class enumerating the available presets for token_ordering.
    """

    LEFT_TO_RIGHT_TOP_TO_BOTTOM = auto()
    RIGHT_TO_LEFT_TOP_TO_BOTTOM = auto()
    TOP_TO_BOTTOM_LEFT_TO_RIGHT = auto()
    TOP_TO_BOTTOM_RIGHT_TO_LEFT = auto()


_ELEMENT_ORDERING_FUNCTIONS: Dict[TokenOrdering, Callable[[List], List]] = {
    TokenOrdering.LEFT_TO_RIGHT_TOP_TO_BOTTOM: lambda tokens: sorted(
        tokens, key=lambda elem: (-elem.y0, elem.x0)
    ),
    TokenOrdering.RIGHT_TO_LEFT_TOP_TO_BOTTOM: lambda tokens: sorted(
        tokens, key=lambda elem: (-elem.y0, -elem.x0)
    ),
    TokenOrdering.TOP_TO_BOTTOM_LEFT_TO_RIGHT: lambda tokens: sorted(
        tokens, key=lambda elem: (elem.x0, -elem.y0)
    ),
    TokenOrdering.TOP_TO_BOTTOM_RIGHT_TO_LEFT: lambda tokens: sorted(
        tokens, key=lambda elem: (-elem.x0, -elem.y0)
    ),
}

DECIMAL_ATTRS = {"adv", "height", "linewidth", "pts", "size", "srcsize", "width", "x0", "x1", "y0", "y1"}

ALL_ATTRS = DECIMAL_ATTRS | {"bits", "upright", "font", "fontname", "name", "text", "imagemask", "colorspace",
                             "evenodd", "fill", "non_stroking_color", "path", "stream", "stroke", "stroking_color"}


class TokenIterator(Iterator):
    index: int
    line: "PDFLine"

    def __init__(self, token_list: "TokenList"):
        self.index = 0
        self.line = token_list.line
        self.indexes = iter(sorted(token_list.indexes))

    def __next__(self):
        index = next(self.indexes)
        return self.line.tokens[index]

class TokenList(Iterable):
    """
    Used to represent a list of tokens, and to enable filtering of those tokens.

    Any time you have a group of tokens, for example pdf_document.tokens or
    page.tokens, you will get an `tokenList`. You can iterate through this, and also
    access specific tokens. On top of this, there are lots of methods which you can
    use to further filter your tokens. Since all of these methods return a new
    LineList, you can chain these operations.

    Internally, we keep a set of indexes corresponding to the PDFTokens in the
    document. This means you can treat TokenLists like sets to combine different
    TokenLists together.


    """

    def __init__(
        self,
        line: "PDFLine",
        indexes = None,
    ):
        self.line = line
        if indexes is not None:
            self.indexes = frozenset(indexes)
        else:
            self.indexes = frozenset(range(0, len(line.tokens)))

    def filter_by_text_equal(self, text: str, stripped: bool = True) -> "TokenList":
        """
        Filter for tokens whose text is exactly the given string.

        Args:
            text (str): The text to filter for.
            stripped (bool, optional): Whether to strip the text of the token before
                comparison. Default: True.

        Returns:
            TokenList: The filtered list.
        """
        new_indexes = set(
            token.index for token in self if token.Text(stripped) == text
        )

        return TokenList(self.line, new_indexes)

    def filter_by_text_contains(self, text: str) -> "TokenList":
        """
        Filter for tokens whose text contains the given string.

        Args:
            text (str): The text to filter for.

        Returns:
            TokenList: The filtered list.
        """


        new_indexes = set(token.index for token in self if text in token.Text)
        return TokenList(self.line, new_indexes)

    def filter_by_regex(
        self,
        regex: str,
        regex_flags: Union[int, re.RegexFlag] = 0,
        substring_match: bool = True,
    ):
        """
        Filter for tokens given a regular expression.

        Args:
            regex (str): The regex to filter for.
            regex_flags (str, optional): Regex flags compatible with the re module.
                Default: 0.
            stripped (bool, optional): Whether to strip the text of the token before
                comparison. Default: True.

        Returns:
            TokenList: The filtered list.
        """

        regex_func=re.search if substring_match else re.match

        new_indexes = set(
            token.index
            for token in self
            if regex_func(regex, token.Text, flags=regex_flags)
        )

        return TokenList(self.line, new_indexes)

    def filter_by_font(self, font: str) -> "TokenList":
        """
        Filter for tokens containing only the given font.

        Args:
            font (str): The font to filter for.

        Returns:
            TokenList: The filtered list.
        """
        return self.filter_by_fonts(font)

    def filter_by_fonts(self, *fonts: str) -> "TokenList":
        """
        Filter for tokens containing only the given font.

        Args:
            *fonts (str): The fonts to filter for.

        Returns:
            TokenList: The filtered list.
        """
        new_indexes = self.indexes & self.line._token_indexes_with_fonts(*fonts)
        return TokenList(self.line, new_indexes)

    def before(self, token: "PDFtoken", inclusive: bool = False) -> "TokenList":
        """
        Returns all tokens before the specified token.

        By before, we mean preceding tokens according to their index. The PDFDocument
        will order tokens according to the specified token_ordering (which defaults
        to left to right, top to bottom).

        Args:
            token (PDFtoken): The token in question.
            inclusive (bool, optional): Whether the include `token` in the returned
                results. Default: False.

        Returns:
            TokenList: The filtered list.
        """
        new_indexes = set(range(0, token.index))
        if inclusive:
            new_indexes.add(token.index)
        return self.__intersect_indexes_with_self(new_indexes)

    def after(self, token: "PDFtoken", inclusive: bool = False) -> "TokenList":
        """
        Returns all tokens after the specified token.

        By after, we mean succeeding tokens according to their index. The PDFDocument
        will order tokens according to the specified token_ordering (which defaults
        to left to right, top to bottom).

        Args:
            token (PDFtoken): The token in question.
            inclusive (bool, optional): Whether the include `token` in the returned
                results. Default: False.

        Returns:
            TokenList: The filtered list.
        """
        new_indexes = set(range(token.index + 1, max(self.indexes) + 1))
        if inclusive:
            new_indexes.add(token.index)
        return self.__intersect_indexes_with_self(new_indexes)

    def between(
        self,
        start_token: "PDFtoken",
        end_token: "PDFtoken",
        inclusive: bool = False,
    ):
        """
        Returns all tokens between the start and end tokens.

        This is done according to the token indexes. The PDFDocument will order
        tokens according to the specified token_ordering (which defaults
        to left to right, top to bottom).

        This is the same as applying `before` with `start_token` and `after` with
        `end_token`.

        Args:
            start_token (PDFtoken): Returned tokens will be after this token.
            end_token (PDFtoken): Returned tokens will be before this token.
            inclusive (bool, optional): Whether the include `start_token` and
                `end_token` in the returned results. Default: False.

        Returns:
            TokenList: The filtered list.
        """
        new_indexes = set(range(start_token.index + 1, end_token.index))
        if inclusive:
            new_indexes = new_indexes.union([start_token.index, end_token.index])
        return self.__intersect_indexes_with_self(new_indexes)

    def extract_single_token(self) -> "PDFtoken":
        """
        Returns only token in the tokenList, provided there is only one token.

        This is mainly for convenience, when you think you've filtered down to a single
        token and you would like to extract said token.

        Raises:
            NotokenFoundError: If there are no tokens in the tokenList
            MultipletokensFoundError: If there is more than one token in the
                tokenList

        Returns:
            PDFtoken: The single token remaining in the list.
        """


        if len(self.indexes) == 0:
            return None

        return self.line._token_list[list(self.indexes)[0]]

    def extract_tokens(self) -> "PDFtoken":
        """
        Returns only token in the tokenList, provided there is only one token.

        This is mainly for convenience, when you think you've filtered down to a single
        token and you would like to extract said token.

        Raises:
            NotokenFoundError: If there are no tokens in the tokenList
            MultipletokensFoundError: If there is more than one token in the
                tokenList

        Returns:
            PDFtoken: The single token remaining in the list.
        """
        if len(self.indexes) == 0:
            raise NoTokenFoundError("There are no tokens in the tokenList")


        return self.line._token_list[list(self.indexes)]


    def __intersect_indexes_with_self(self, new_indexes: Set[int]) -> "TokenList":
        return self & TokenList(self.line, new_indexes)

    def __iter__(self) -> TokenIterator:
        """
        Returns an tokenIterator class that allows iterating through tokens.

        tokens will be returned in order of the tokens in the document,
        left-to-right, top-to-bottom (the same as you read).
        """
        return TokenIterator(self)

    def __contains__(self, token: "PDFtoken") -> bool:
        """
        Returns True if the token is in the tokenList, otherwise False.
        """
        return token.index in self.indexes

    def __repr__(self):
        return f"<tokenList of {len(self.indexes)} tokens>"

    def __getitem__(self, key: Union[int, slice]) -> Union["PDFtoken", "TokenList"]:
        """
        Returns the token in position `key` of the tokenList if an int is given, or
        returns a new tokenList if a slice is given.

        tokens are ordered by their original positions in the document, which is
        left-to-right, top-to-bottom (the same you you read).
        """
        if isinstance(key, slice):
            new_indexes = set(sorted(self.indexes)[key])
            return TokenList(self.line, new_indexes)
        token_index = sorted(self.indexes)[key]
        return self.line.tokens[token_index]

    def __eq__(self, other: object) -> bool:
        """
        Returns True if the two tokenLists contain the same tokens from the same
        document.
        """
        if not isinstance(other, TokenList):
            raise NotImplementedError(f"Can't compare tokenList with {type(other)}")
        return (
                self.indexes == other.indexes
                and self.line == other.line
                and self.__class__ == other.__class__
        )

    def __hash__(self):
        return hash(hash(self.indexes) + hash(self.line))

    def __len__(self):
        """
        Returns the number of tokens in the tokenList.
        """
        return len(self.indexes)

    def __sub__(self, other: "TokenList") -> "TokenList":
        """
        Returns an tokenList of tokens that are in the first tokenList but not in
        the second.
        """
        return TokenList(self.line, self.indexes - other.indexes)

    def __or__(self, other: "TokenList") -> "TokenList":
        """
        Returns an tokenList of tokens that are in either tokenList
        """
        return TokenList(self.line, self.indexes | other.indexes)

    def __xor__(self, other: "TokenList") -> "TokenList":
        """
        Returns an tokenList of tokens that are in either tokenList, but not both.
        """
        return TokenList(self.line, self.indexes ^ other.indexes)

    def __and__(self, other: "TokenList") -> "TokenList":
        """
        Returns an tokenList of tokens that are in both tokenList
        """
        return TokenList(self.line, self.indexes & other.indexes)


class PDFContainer(object):
    cached_properties = ["_rect_edges", "_edges", "_objects"]

    def flush_cache(self, properties=None):
        props = self.cached_properties if properties is None else properties
        for p in props:
            if hasattr(self, p):
                delattr(self, p)

    @property
    def rects(self):
        return self.objects.get("rect", [])

    @property
    def lines(self):
        return self.objects.get("line", [])

    @property
    def curves(self):
        return self.objects.get("curve", [])

    @property
    def images(self):
        return self.objects.get("image", [])

    @property
    def chars(self):
        return self.objects.get("char", [])

    @property
    def rect_edges(self):
        if hasattr(self, "_rect_edges"):
            return self._rect_edges
        rect_edges_gen = (rect_to_edges(r) for r in self.rects)
        self._rect_edges = list(chain(*rect_edges_gen))
        return self._rect_edges

    @property
    def edges(self):
        if hasattr(self, "_edges"):
            return self._edges
        line_edges = list(map(line_to_edge, self.lines))
        self._edges = self.rect_edges + line_edges
        return self._edges

    @property
    def horizontal_edges(self):
        def test(x):
            return x["orientation"] == "h"

        return list(filter(test, self.edges))

    @property
    def vertical_edges(self):
        def test(x):
            return x["orientation"] == "v"

        return list(filter(test, self.edges))



class TokenBase:
    """
    Token base define the common features of all the pdf extracted tokens namely the coordinate
    Args:
        x0 (int): The x coordinate of the bottom left corner.
        x1 (int): The x coordinate of the top right corner.
        y0 (int): The y coordinate of the bottom left corner.
        y1 (int): The y coordinate of the top right corner.

    Raises:
        InvalidCoordinatesError: if x1 is smaller than x0 or y1 is smaller than y0.

    Attributes:
        x0 (int): The x coordinate of the bottom left corner.
        x1 (int): The x coordinate of the top right corner.
        y0 (int): The y coordinate of the bottom left corner.
        y1 (int): The y coordinate of the top right corner.
        width (int): The width of the box, equal to x1 - x0.
        height (int): The height of the box, equal to y1 - y0.
    """

    def __init__(self, x0: float=None, x1: float=None, y0: float=None, y1: float=None):


        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TokenBase):
            raise NotImplementedError(f"Can't compare BoundingBox with {type(other)}")

        return all(
            [
                self.x0 == other.x0,
                self.x1 == other.x1,
                self.y0 == other.y0,
                self.y1 == other.y1,
            ]
        )
    @property
    def width(self):
        return (self.x1 - self.x0)

    def height(self):
        return (self.y1 - self.y0)

    def entirely_within(self, other_token) -> bool:
        """
        Whether the entire element is within the bounding box.

        Args:
            other_token (BoundingBox): The bounding box to check whether the element
                is within.

        Returns:
            bool: True if the element is entirely contained within the bounding box.
        """
        return all(
            [
                self.x0 >= other_token.x0,
                self.x1 <= other_token.x1,
                self.y0 >= other_token.y0,
                self.y1 <= other_token.y1,
            ]
        )

    def partially_within(self, other_token) -> bool:
        """
        Whether any part of the element is within the bounding box.

        Args:
            other_token (BoundingBox): The bounding box to check whether the element
                is partially within.

        Returns:
            bool: True if any part of the element is within the bounding box.
        """
        return all(
            [
                other_token.x0 <= self.x1,
                other_token.x1 >= self.x0,
                other_token.y0 <= self.y1,
                other_token.y1 >= self.y0,
            ]
        )

    def __repr__(self):
        return f"<BoundingBox x0={self.x0}, x1={self.x1}, y0={self.y0}, y1={self.y1}>"

class PDFToken(TokenBase):
    document: "PDFDocument"
    original_token: "LTTextLineHorizontal"
    tags: Set[str]
    _index: int
    __font_name: Optional[str] = None
    __font_size: Optional[float] = None
    __font_size_precision: int
    __font: Optional[str] = None
    __page_number: int
    def __init__(self, token,
                 document: "PDFDocument",
                 index: int,
                 page_number: int,
                 font_size_precision: int = 1,
                 ):

        self.font = get_fonts(token)

        super().__init__(x0=token.x0, x1=token.x1, y0=token.y0, y1=token.y1)
        self.document = document
        self.original_tokens = [token]
        self._index = index
        self.__page_number = page_number
        self.__font_size_precision = font_size_precision
        self.__font_visible=None

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, PDFToken):
            return self.Text == other.Text and self.x0 == other.x0 and self.y1 == other.y1
        return False

    def __repr__(self):
        return '<' + self.Text + '>'

    def __str__(self):
        return self.Text

    def __hash__(self):
        return hash(str(self)+str(self._index))

    @property
    def index(self):
        return self._index
    @index.setter
    def index(self, val):
        self._index=val

    @property
    def page_number(self):
        return self.__page_number

    @property
    def Text(self):
        return  ' '.join([e.get_text().strip() for e in self.original_tokens])

    def add(self, other):

        self.y0 = min(other.y0, self.y0)
        self.x0 = min(other.x0, self.x0)
        self.y1=max(other.y1, self.y1)
        self.x1 = max(other.x1, self.x1)
        self.original_tokens.extend(other.original_tokens)
        return self
    @property
    def font_name(self) -> str:
        """
        The name of the font.

        This will be taken from the pdf itself, using the most common font within all
        the characters in the element.

        Returns:
            str: The font name of the element.
        """
        if self.__font_name is not None:
            return self.__font_name

        counter = Counter(
            (
                character.fontname
                for line in self.original_tokens
                for character in line
                if hasattr(character, "fontname")
            )
        )
        self.__font_name = counter.most_common(1)[0][0]
        return self.__font_name


    @property
    def is_visible(self) -> bool:
        """
        The name of the font.

        This will be taken from the pdf itself, using the most common font within all
        the characters in the element.

        Returns:
            str: The font name of the element.
        """
        if self.__font_visible is not None:
            return self.__font_visible


        counter = Counter(
            (
                character.graphicstate.linewidth>0 or (character.graphicstate.linewidth==0 and character.graphicstate.ncolor not in [(0,0,0), (1,0,1)])
                for line in self.original_tokens
                for character in line
                if hasattr(character, "graphicstate")
            )
        )
        self.__font_visible = counter.most_common(1)[0][0]

        return self.__font_visible
    @property
    def font_size(self) -> float:
        """
        The size of the font.

        This will be taken from the pdf itself, using the most common size within all
        the characters in the element.

        Returns:
            float: The font size of the element, rounded to the font_size_precision of
                the document.
        """
        if self.__font_size is not None:
            return self.__font_size

        counter = Counter(
            (
                character.height
                for line in self.original_tokens
                for character in line
                if hasattr(character, "height")
            )
        )
        self.__font_size = round(
            counter.most_common(1)[0][0], self.__font_size_precision
        )
        return self.__font_size

    @property
    def font_(self) -> str:
        """
        The name and size of the font, separated by a comma with no spaces.

        This will be taken from the pdf itself, using the first character in the
        element.

        If you have provided a font_mapping, this is the string you should map. If
        the string is mapped in your font_mapping then the mapped value will be
        returned. font_mapping can have regexes as keys.

        Returns:
            str: The font of the element.
        """
        if self.__font is not None:
            return self.__font

        font = f"{self.font_name},{self.font_size}"
        self.__font = self.document._font_mapping.get(font) or font
        return self.__font

    @property
    def ignored(self) -> bool:
        """
        A flag specifying whether the element has been ignored.
        """
        return self._index in self.document._ignored_indexes

    def add_tag(self, new_tag: str):
        """
        Adds the `new_tag` to the tags set.

        Args:
            new_tag (str): The tag you would like to add.
        """
        self.tags.add(new_tag)

    def ignore(self):
        """
        Marks the element as ignored.

        The element will no longer be returned in any newly instantiated `ElementList`.
        Note that this includes calling any new filter functions on an existing
        `ElementList`, since doing so always returns a new `ElementList`.
        """
        self.document._ignored_indexes.add(self._index)


class PDFLine(TokenBase):
    def __init__(self, page):
        super().__init__()
        self.Num=-1
        self.page=page
        self.tokens=[]
        self.space_above=-1
        self.space_below=-1
        self.index = None

    @property
    def x0(self):
        if len(self.tokens):
            return self.tokens[0].x0
    @x0.setter
    def x0(self, val):
        self._x0=val

    @property
    def x1(self):
        if len(self.tokens):
            return self.tokens[-1].x1
    @x1.setter
    def x1(self, val):
        self._x1=val
    @property
    def y0(self):
        if len(self.tokens):
            return min(self.tokens[0].y0, self.tokens[-1].y0)

    @y0.setter
    def y0(self, val):
        self._y0=val

    @property
    def y1(self):
        if len(self.tokens):
            return max(self.tokens[0].y1, self.tokens[-1].y1)

    @y1.setter
    def y1(self, val):
        self._y1=val

    @property
    def height(self):
        if len(self.tokens):
            return max([t.y1 for t in self.tokens])-min([t.y0 for t in self.tokens])

    @property
    def width(self):
        if len(self.tokens):
            return max([t.x1 for t in self.tokens])-min([t.x0 for t in self.tokens])


    @property
    def xpos(self):
        return (self.x1+self.x0)/2

    @property
    def ypos(self):
        return (self.y1+self.y0)/2

    @property
    def yposPage(self):
        return 1-(self.ypos / self.page.height)

    @property
    def Text(self):
        return '\t'.join(t.Text for t in self.tokens)
    @property
    def yposDoc(self):
        return self.Num+self.yposPage

    @property
    def page_number(self):
        return self.page.number



    def __eq__(self, other):
        return self.Text==other.Text

    def get_feauture(self):
        return {'Page': self.page_number,
                'x0': self.x0,
                'y0': self.y0,
                'x1': self.x1,
                'y1': self.y1,
                'Text': self.Text,
                'lineNumber': self.Num,
                'xpos': self.xpos,
                'ypos': self.ypos,
                'yposPage': self.yposPage,
                'yposDoc': self.yposDoc}

