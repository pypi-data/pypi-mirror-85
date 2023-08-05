from typing import (
    overload,
    Union,
    Set,
    FrozenSet,
    Optional,
    Iterable,
    Iterator,
    TYPE_CHECKING,
)

import re

from pdf2txt.components import TokenBase as BoundingBox
from pdf2txt.exceptions import (
    TokenOutOfRangeError,
    NoTokenFoundError,
    MultipleTokensFoundError,
    ParagraphNotFoundError,
)

if TYPE_CHECKING:
    from .components import PDFDocument, PDFtoken


class ItemIterator(Iterator):
    index: int
    document: "PDFDocument"

    def __init__(self, token_list: "LineList"):
        self.index = 0
        self.document = token_list.document
        self.indexes = iter(sorted(token_list.indexes))

    def __next__(self):
        index = next(self.indexes)
        return self.document._token_list[index]


class LineList(Iterable):
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

    document: "PDFDocument"
    indexes: Union[Set[int], FrozenSet[int]]

    def __init__(
        self,
        document: "PDFDocument",
        indexes: Optional[Union[Set[int], FrozenSet[int]]] = None,
    ):
        self.document = document
        if indexes is not None:
            self.indexes = frozenset(indexes)
        else:
            self.indexes = frozenset(range(0, len(document._token_list)))
#        self.indexes = self.indexes - self.document._ignored_indexes

    def add_tag_to_tokens(self, tag: str) -> None:
        """
        Adds a tag to all tokens in the list.

        Args:
            tag (str): The tag you would like to add.
        """
        for token in self:
            token.add_tag(tag)

    def filter_by_tag(self, tag: str) -> "LineList":
        """
        Filter for tokens containing only the given tag.

        Args:
            tag (str): The tag to filter for.

        Returns:
            LineList: The filtered list.
        """
        new_indexes = set(token.index for token in self if tag in token.tags)
        return LineList(self.document, new_indexes)

    def filter_by_tags(self, *tags: str) -> "LineList":
        """
        Filter for tokens containing any of the given tags.

        Args:
            *tags (str): The tags to filter for.

        Returns:
            LineList: The filtered list.
        """
        new_indexes = set(
            token.index
            for token in self
            if any(tag in token.tags for tag in tags)
        )
        return LineList(self.document, new_indexes)

    def filter_by_text_equal(self, text: str, stripped: bool = True) -> "LineList":
        """
        Filter for tokens whose text is exactly the given string.

        Args:
            text (str): The text to filter for.
            stripped (bool, optional): Whether to strip the text of the token before
                comparison. Default: True.

        Returns:
            LineList: The filtered list.
        """
        new_indexes = set(
            token.index for token in self if token.Text(stripped) == text
        )

        return LineList(self.document, new_indexes)

    def filter_by_text_contains(self, text: str) -> "LineList":
        """
        Filter for tokens whose text contains the given string.

        Args:
            text (str): The text to filter for.

        Returns:
            LineList: The filtered list.
        """


        new_indexes = set(token.index for token in self if text in token.Text)
        return LineList(self.document, new_indexes)

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
            LineList: The filtered list.
        """

        regex_func=re.search if substring_match else re.match

        new_indexes = set(
            token.index
            for token in self
            if regex_func(regex, token.Text, flags=regex_flags)
        )

        return LineList(self.document, new_indexes)

    def filter_by_font(self, font: str) -> "LineList":
        """
        Filter for tokens containing only the given font.

        Args:
            font (str): The font to filter for.

        Returns:
            LineList: The filtered list.
        """
        return self.filter_by_fonts(font)

    def filter_by_fonts(self, *fonts: str) -> "LineList":
        """
        Filter for tokens containing only the given font.

        Args:
            *fonts (str): The fonts to filter for.

        Returns:
            LineList: The filtered list.
        """
        new_indexes = self.indexes & self.document._token_indexes_with_fonts(*fonts)
        return LineList(self.document, new_indexes)

    def filter_by_page(self, page_number: int) -> "LineList":
        """
        Filter for tokens on the given page.

        Args:
            page (int): The page to filter for.

        Returns:
            LineList: The filtered list.
        """
        page = self.document.get_page(page_number)
        new_indexes = set(token.index for token in page.tokens)
        return self.__intersect_indexes_with_self(new_indexes)

    def filter_by_pages(self, *page_numbers: int) -> "LineList":
        """
        Filter for tokens on any of the given pages.

        Args:
            *pages (int): The pages to filter for.

        Returns:
            LineList: The filtered list.
        """
        new_indexes: Set[int] = set()
        for page_number in page_numbers:
            page = self.document.get_page(page_number)
            new_indexes |= set(token.index for token in page.tokens)
        return self.__intersect_indexes_with_self(new_indexes)


    def ignore_tokens(self) -> None:
        """
        Marks all the tokens in the tokenList as ignored.
        """
        self.document._ignored_indexes = self.document._ignored_indexes.union(
            self.indexes
        )

    def to_the_right_of(
        self, token: "PDFtoken", inclusive: bool = False, tolerance: float = 0.0
    ) -> "LineList":
        """
        Filter for tokens which are to the right of the given token.

        If you draw a box from the right hand edge of the token to the right hand
        side of the page, all tokens which are partially within this box are returned.

        Note:
            By "to the right of" we really mean "directly to the right of", i.e. the
            returned tokens all have at least some part which is vertically aligned
            with the specified token.

        Note:
            Technically the token you specify will satisfy the condition, but we
            assume you do not want that token returned. If you do, you can pass
            `inclusive=True`.

        Args:
            token (PDFtoken): The token in question.
            inclusive (bool, optional): Whether the include `token` in the returned
                results. Default: False.
            tolerance (int, optional): To be counted as to the right, the tokens must
                overlap by at least `tolerance` on the Y axis. Tolerance is capped at
                half the height of the token. Default 0.

        Returns:
            LineList: The filtered list.
        """
        page_number = token.page_number
        page = self.document.get_page(page_number)
        tolerance = min(token.height / 2, tolerance)
        bounding_box = BoundingBox(
            token.x1,
            page.width,
            token.y0 + tolerance,
            token.y1 - tolerance,
        )
        results = self.filter_partially_within_bounding_box(bounding_box, page_number)
        if not inclusive:
            results = results.remove_token(token)
        return results

    def to_the_left_of(
        self, token: "PDFtoken", inclusive: bool = False, tolerance: float = 0.0
    ) -> "LineList":
        """
        Filter for tokens which are to the left of the given token.


        If you draw a box from the left hand edge of the token to the left hand
        side of the page, all tokens which are partially within this box are returned.

        Note:
            By "to the left of" we really mean "directly to the left of", i.e. the
            returned tokens all have at least some part which is vertically aligned
            with the specified token.

        Note:
            Technically the token you specify will satisfy the condition, but we
            assume you do not want that token returned. If you do, you can pass
            `inclusive=True`.

        Args:
            token (PDFtoken): The token in question.
            inclusive (bool, optional): Whether the include `token` in the returned
                results. Default: False.
            tolerance (int, optional): To be counted as to the left, the tokens must
                overlap by at least `tolerance` on the Y axis. Tolerance is capped at
                half the height of the token. Default 0.


        Returns:
            LineList: The filtered list.
        """
        page_number = token.page_number
        tolerance = min(token.bounding_box.height / 2, tolerance)
        bounding_box = BoundingBox(
            0,
            token.bounding_box.x0,
            token.bounding_box.y0 + tolerance,
            token.bounding_box.y1 - tolerance,
        )
        results = self.filter_partially_within_bounding_box(bounding_box, page_number)
        if not inclusive:
            results = results.remove_token(token)
        return results

    def below(
        self,
        token: "PDFtoken",
        inclusive: bool = False,
        all_pages: bool = False,
        tolerance: float = 0.0,
    ) -> "LineList":
        """
        Returns all tokens which are below the given token.

        If you draw a box from the bottom edge of the token to the bottom of the page,
        all tokens which are partially within this box are returned. By default, only
        tokens on the same page as the given token are included, but you can pass
        `inclusive=True` to also include the pages which come after (and so are below)
        the page containing the given token.

        Note:
            By "below" we really mean "directly below", i.e. the returned tokens all
            have at least some part which is horizontally aligned with the specified
            token.

        Note:
            Technically the token you specify will satisfy the condition, but we
            assume you do not want that token returned. If you do, you can pass
            `inclusive=True`.

        Args:
            token (PDFtoken): The token in question.
            inclusive (bool, optional): Whether the include `token` in the returned
                results. Default: False.
            all_pages (bool, optional): Whether to included pages other than the page
                which the token is on.
            tolerance (int, optional): To be counted as below, the tokens must
                overlap by at least `tolerance` on the X axis. Tolerance is capped at
                half the width of the token. Default 0.

        Returns:
            LineList: The filtered list.
        """
        page_number = token.page_number
        tolerance = min(token.bounding_box.width / 2, tolerance)
        bounding_box = BoundingBox(
            token.bounding_box.x0 + tolerance,
            token.bounding_box.x1 - tolerance,
            0,
            token.bounding_box.y0,
        )
        results = self.filter_partially_within_bounding_box(bounding_box, page_number)
        if all_pages:
            for page in self.document.pages:
                if page.page_number <= page_number:
                    continue
                # We're on a page which is located below our token, so the bounding
                # box should be the length of the entire page.
                bounding_box = BoundingBox(
                    token.bounding_box.x0 + tolerance,
                    token.bounding_box.x1 - tolerance,
                    0,
                    page.height,
                )
                results = results | self.filter_partially_within_bounding_box(
                    bounding_box, page.page_number
                )
        if not inclusive:
            results = results.remove_token(token)
        return results

    def above(
        self,
        token: "PDFtoken",
        inclusive: bool = False,
        all_pages: bool = False,
        tolerance: float = 0.0,
    ) -> "LineList":
        """
        Returns all tokens which are above the given token.

        If you draw a box from the bottom edge of the token to the bottom of the page,
        all tokens which are partially within this box are returned. By default, only
        tokens on the same page as the given token are included, but you can pass
        `inclusive=True` to also include the pages which come before (and so are above)
        the page containing the given token.

        Note:
            By "above" we really mean "directly above", i.e. the returned tokens all
            have at least some part which is horizontally aligned with the specified
            token.

        Note:
            Technically the token you specify will satisfy the condition, but we
            assume you do not want that token returned. If you do, you can pass
            `inclusive=True`.

        Args:
            token (PDFtoken): The token in question.
            inclusive (bool, optional): Whether the include `token` in the returned
                results. Default: False.
            all_pages (bool, optional): Whether to included pages other than the page
                which the token is on.
            tolerance (int, optional): To be counted as above, the tokens must
                overlap by at least `tolerance` on the X axis. Tolerance is capped at
                half the width of the token. Default 0.

        Returns:
            LineList: The filtered list.
        """
        page_number = token.page_number
        page = self.document.get_page(page_number)
        tolerance = min(token.bounding_box.width / 2, tolerance)
        bounding_box = BoundingBox(
            token.bounding_box.x0 + tolerance,
            token.bounding_box.x1 - tolerance,
            token.bounding_box.y1,
            page.height,
        )
        results = self.filter_partially_within_bounding_box(bounding_box, page_number)
        if all_pages:
            for page in self.document.pages:
                if page.page_number >= page_number:
                    continue
                # We're on a page which is located above our token, so the bounding
                # box should be the length of the entire page.
                bounding_box = BoundingBox(
                    token.bounding_box.x0 + tolerance,
                    token.bounding_box.x1 - tolerance,
                    0,
                    page.height,
                )
                results = results | self.filter_partially_within_bounding_box(
                    bounding_box, page.page_number
                )
        if not inclusive:
            results = results.remove_token(token)
        return results

    def vertically_in_line_with(
        self,
        token: "PDFtoken",
        inclusive: bool = False,
        all_pages: bool = False,
        tolerance: float = 0.0,
    ) -> "LineList":
        """
        Returns all tokens which are vertically in line with the
        given token.

        If you extend the left and right edges of the token to the top and bottom of
        the page, all tokens which are partially within this box are returned. By
        default, only tokens on the same page as the given token are included, but
        you can pass `inclusive=True` to include all pages.

        This is equivalent to doing `foo.above(...) | foo.below(...)`.

        Note:
            Technically the token you specify will satisfy the condition, but we
            assume you do not want that token returned. If you do, you can pass
            `inclusive=True`.

        Args:
            token (PDFtoken): The token in question.
            inclusive (bool, optional): Whether the include `token` in the returned
                results. Default: False.
            all_pages (bool, optional): Whether to included pages other than the page
                which the token is on.
            tolerance (int, optional): To be counted as in line with, the tokens must
                overlap by at least `tolerance` on the X axis. Tolerance is capped at
                half the width of the token. Default 0.

        Returns:
            LineList: The filtered list.
        """
        page_number = token.page_number
        page = self.document.get_page(page_number)
        tolerance = min(token.width / 2, tolerance)
        bounding_box = BoundingBox(
            token.x0 + tolerance,
            token.x1 - tolerance,
            0,
            page.height,
        )
        results = self.filter_partially_within_bounding_box(bounding_box, page_number)
        if all_pages:
            for page_num in range(self[0].page_number, self[-1].page_number + 1):
                page = self.document.get_page(page_num)
                if page.page_number == page_number:
                    # Already handled page containing token
                    continue
                bounding_box = BoundingBox(
                    token.x0 + tolerance,
                    token.x1 - tolerance,
                    0,
                    page.height,
                )
                results = results | self.filter_partially_within_bounding_box(
                    bounding_box, page.page_number
                )

        if not inclusive:
            results = results.remove_token(token)
        return results

    def horizontally_in_line_with(
        self, token: "PDFtoken", inclusive: bool = False, tolerance: float = 0.0
    ) -> "LineList":
        """
        Returns all tokens which are horizontally in line with the given token.

        If you extend the top and bottom edges of the token to the left and right of
        the page, all tokens which are partially within this box are returned.

        This is equivalent to doing
        `foo.to_the_left_of(...) | foo.to_the_right_of(...)`.

        Note:
            Technically the token you specify will satisfy the condition, but we
            assume you do not want that token returned. If you do, you can pass
            `inclusive=True`.

        Args:
            token (PDFtoken): The token in question.
            inclusive (bool, optional): Whether the include `token` in the returned
                results. Default: False.
            tolerance (int, optional): To be counted as in line with, the tokens must
                overlap by at least `tolerance` on the Y axis. Tolerance is capped at
                half the width of the token. Default 0.

        Returns:
            LineList: The filtered list.
        """
        page_number = token.page_number
        page = self.document.get_page(page_number)
        tolerance = min(token.height / 2, tolerance)
        bounding_box = BoundingBox(
            0,
            page.width,
            token.y0 + tolerance,
            token.y1 - tolerance,
        )
        results = self.filter_partially_within_bounding_box(bounding_box, page_number)
        if not inclusive:
            results = results.remove_token(token)
        return results

    def filter_partially_within_bounding_box(
        self, bounding_box: BoundingBox, page_number: int
    ) -> "LineList":
        """
        Returns all tokens on the given page which are partially within the given box.

        Args:
            bounding_box (BoundingBox): The bounding box to filter within.
            page_number (int): The page which you'd like to filter within the box.

        Returns:
            LineList: The filtered list.
        """
        new_indexes: Set[int] = set()
        for elem in self.filter_by_page(page_number):
            if elem.partially_within(bounding_box):
                new_indexes.add(elem.index)
        return self.__intersect_indexes_with_self(new_indexes)

    def before(self, token: "PDFtoken", inclusive: bool = False) -> "LineList":
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
            LineList: The filtered list.
        """
        new_indexes = set(range(0, token.index))
        if inclusive:
            new_indexes.add(token.index)
        return self.__intersect_indexes_with_self(new_indexes)

    def after(self, token: "PDFtoken", inclusive: bool = False) -> "LineList":
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
            LineList: The filtered list.
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
            LineList: The filtered list.
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

        return self.document._token_list[list(self.indexes)[0]]

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


        return self.document._token_list[list(self.indexes)]

    def add_token(self, token: "PDFtoken") -> "LineList":
        """
        Explicitly adds the token to the tokenList.

        Note:
            If the token is already in the tokenList, this does nothing.

        Args:
            token (PDFtoken): The token to add.

        Returns:
            LineList: A new list with the additional token.
        """
        return LineList(self.document, self.indexes | set([token.index]))

    def add_tokens(self, *tokens: "PDFtoken") -> "LineList":
        """
        Explicitly adds the tokens to the tokenList.

        Note:
            If the tokens is already in the tokenList, this does nothing.

        Args:
            *tokens (PDFtoken): The tokens to add.

        Returns:
            LineList: A new list with the additional tokens.
        """
        return LineList(
            self.document, self.indexes | set([token.index for token in tokens])
        )

    def remove_token(self, token: "PDFtoken") -> "LineList":
        """
        Explicitly removes the token from the tokenList.

        Note:
            If the token is not in the tokenList, this does nothing.

        Args:
            token (PDFtoken): The token to remove.

        Returns:
            LineList: A new list without the token.
        """
        return LineList(self.document, self.indexes - set([token.index]))

    def remove_tokens(self, *tokens: "PDFtoken") -> "LineList":
        """
        Explicitly removes the tokens from the tokenList.

        Note:
            If the tokens are not in the tokenList, this does nothing.

        Args:
            *tokens (PDFtoken): The tokens to remove.

        Returns:
            LineList: A new list without the tokens.
        """
        return LineList(
            self.document, self.indexes - set(token.index for token in tokens)
        )

    def move_forwards_from(
        self, token: "PDFtoken", count: int = 1, capped: bool = False
    ) -> "PDFtoken":
        """
        Returns the token in the token list obtained by moving forwards from
        `token` by `count`.

        Args:
            token (PDFtoken): The token to start at.
            count (int, optional): How many tokens to move from `token`. The default
                of 1 will move forwards by one token. Passing 0 will simply return the
                token itself. You can also pass negative integers to move backwards.
            capped (bool, optional): By default (False), if the count is high enough
                that we try to move out of range of the list, an exception will be
                raised. Passing `capped=True` will change this behaviour to instead
                return the token at the start or end of the list.

        Raises:
            tokenOutOfRangeError: If the count is large (or large-negative) enough
                that we reach the end (or start) of the list. Only happens when
                capped=False.
        """
        indexes = sorted(self.indexes)
        new_index = indexes.index(token.index) + count
        if new_index < 0 or new_index >= len(indexes):
            # Out of range. We could simply catch the index error for large new_index,
            # but we have to handle the negative case like this anyway, so might as well
            # do both cases while we're at it.
            if capped:
                new_index = max(min(new_index, len(indexes) - 1), 0)
                token_index = indexes[new_index]
                return self.document._token_list[token_index]
            raise TokenOutOfRangeError(
                f"Requested token is {'before' if new_index < 0 else 'after'} the "
                f"{'start' if new_index < 0 else 'end'} of the tokenList"
            )

        # We avoid just returning self[new_index] here since getitem will do an
        # additional sorted(self.indexes), which we have already computed here.
        token_index = indexes[new_index]
        return self.document._token_list[token_index]

    def move_backwards_from(
        self, token: "PDFtoken", count: int = 1, capped: bool = False
    ) -> "PDFtoken":
        """
        Returns the token in the token list obtained by moving backwards from
        `token` by `count`.

        Args:
            token (PDFtoken): The token to start at.
            count (int, optional): How many tokens to move from `token`. The default
                of 1 will move backwards by one token. Passing 0 will simply return
                the token itself. You can also pass negative integers to move
                forwards.
            capped (bool, optional): By default (False), if the count is high enough
                that we try to move out of range of the list, an exception will be
                raised. Passing `capped=True` will change this behaviour to instead
                return the token at the start or end of the list.

        Raises:
            tokenOutOfRangeError: If the count is large (or large-negative) enough
                that we reach the start (or end) of the list. Only happens when
                capped=False.
        """
        return self.move_forwards_from(token, count=-count, capped=capped)

    def __intersect_indexes_with_self(self, new_indexes: Set[int]) -> "LineList":
        return self & LineList(self.document, new_indexes)

    def __iter__(self) -> ItemIterator:
        """
        Returns an tokenIterator class that allows iterating through tokens.

        tokens will be returned in order of the tokens in the document,
        left-to-right, top-to-bottom (the same as you read).
        """
        return ItemIterator(self)

    def __contains__(self, token: "PDFtoken") -> bool:
        """
        Returns True if the token is in the tokenList, otherwise False.
        """
        return token.index in self.indexes

    def __repr__(self):
        return f"<tokenList of {len(self.indexes)} tokens>"

    @overload
    def __getitem__(self, key: int) -> "PDFtoken":
        pass  # This is for type checking only

    @overload
    def __getitem__(self, key: slice) -> "LineList":
        pass  # This is for type checking only

    def __getitem__(self, key: Union[int, slice]) -> Union["PDFtoken", "LineList"]:
        """
        Returns the token in position `key` of the tokenList if an int is given, or
        returns a new tokenList if a slice is given.

        tokens are ordered by their original positions in the document, which is
        left-to-right, top-to-bottom (the same you you read).
        """
        if isinstance(key, slice):
            new_indexes = set(sorted(self.indexes)[key])
            return LineList(self.document, new_indexes)
        token_index = sorted(self.indexes)[key]
        return self.document._token_list[token_index]

    def __eq__(self, other: object) -> bool:
        """
        Returns True if the two tokenLists contain the same tokens from the same
        document.
        """
        if not isinstance(other, LineList):
            raise NotImplementedError(f"Can't compare tokenList with {type(other)}")
        return (
            self.indexes == other.indexes
            and self.document == other.document
            and self.__class__ == other.__class__
        )

    def __hash__(self):
        return hash(hash(self.indexes) + hash(self.document))

    def __len__(self):
        """
        Returns the number of tokens in the tokenList.
        """
        return len(self.indexes)

    def __sub__(self, other: "LineList") -> "LineList":
        """
        Returns an tokenList of tokens that are in the first tokenList but not in
        the second.
        """
        return LineList(self.document, self.indexes - other.indexes)

    def __or__(self, other: "LineList") -> "LineList":
        """
        Returns an tokenList of tokens that are in either tokenList
        """
        return LineList(self.document, self.indexes | other.indexes)

    def __xor__(self, other: "LineList") -> "LineList":
        """
        Returns an tokenList of tokens that are in either tokenList, but not both.
        """
        return LineList(self.document, self.indexes ^ other.indexes)

    def __and__(self, other: "LineList") -> "LineList":
        """
        Returns an tokenList of tokens that are in both tokenList
        """
        return LineList(self.document, self.indexes & other.indexes)



