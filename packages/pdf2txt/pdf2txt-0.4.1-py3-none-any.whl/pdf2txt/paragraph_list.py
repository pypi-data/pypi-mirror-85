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

from pdf2txt.exceptions import (
    ParagraphNotFoundError
)

if TYPE_CHECKING:
    from .components import PDFDocument, PDFparagraph


class ParagraphIterator(Iterator):
    index: int
    document: "PDFDocument"

    def __init__(self, paragraph_list: "ParagraphList"):
        self.index = 0
        self.document = paragraph_list.document
        self.indexes = iter(sorted(paragraph_list.indexes))

    def __next__(self):
        index = next(self.indexes)
        return self.document._paragraph_list[index]


class ParagraphList(Iterable):
    """
    Used to represent a list of paragraphs, and to enable filtering of those paragraphs.

    Any time you have a group of paragraphs, for example pdf_document.paragraphs or
    page.paragraphs, you will get an `paragraphList`. You can iterate through this, and also
    access specific paragraphs. On top of this, there are lots of methods which you can
    use to further filter your paragraphs. Since all of these methods return a new
    ParagraphList, you can chain these operations.

    Internally, we keep a set of indexes corresponding to the PDFParagraphs in the
    document. This means you can treat ParagraphLists like sets to combine different
    ParagraphLists together.

   
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
            self.indexes = frozenset(range(0, len(document._paragraph_list)))
        self.indexes = self.indexes - self.document._ignored_indexes

    def add_tag_to_paragraphs(self, tag: str) -> None:
        """
        Adds a tag to all paragraphs in the list.

        Args:
            tag (str): The tag you would like to add.
        """
        for paragraph in self:
            paragraph.add_tag(tag)

    def filter_by_tag(self, tag: str) -> "ParagraphList":
        """
        Filter for paragraphs containing only the given tag.

        Args:
            tag (str): The tag to filter for.

        Returns:
            ParagraphList: The filtered list.
        """
        new_indexes = set(paragraph._index for paragraph in self if tag in paragraph.tags)
        return ParagraphList(self.document, new_indexes)

    def filter_by_tags(self, *tags: str) -> "ParagraphList":
        """
        Filter for paragraphs containing any of the given tags.

        Args:
            *tags (str): The tags to filter for.

        Returns:
            ParagraphList: The filtered list.
        """
        new_indexes = set(
            paragraph._index
            for paragraph in self
            if any(tag in paragraph.tags for tag in tags)
        )
        return ParagraphList(self.document, new_indexes)

    def filter_by_title_equal(self, text: str, stripped: bool = True) -> "ParagraphList":
        """
        Filter for paragraphs whose text is exactly the given string.

        Args:
            text (str): The text to filter for.
            stripped (bool, optional): Whether to strip the text of the paragraph before
                comparison. Default: True.

        Returns:
            ParagraphList: The filtered list.
        """
        new_indexes = set(
            paragraph._index for paragraph in self if paragraph.Text(stripped) == text
        )

        return ParagraphList(self.document, new_indexes)

    def filter_by_text_contains(self, text: str) -> "ParagraphList":
        """
        Filter for paragraphs whose text contains the given string.

        Args:
            text (str): The text to filter for.

        Returns:
            ParagraphList: The filtered list.
        """


        new_indexes = set(paragraph._index for paragraph in self if text in paragraph.Text)
        return ParagraphList(self.document, new_indexes)

    def filter_by_regex(
        self,
        regex: str,
        regex_flags: Union[int, re.RegexFlag] = 0,
        substring_match: bool = True,
    ):
        """
        Filter for paragraphs given a regular expression.

        Args:
            regex (str): The regex to filter for.
            regex_flags (str, optional): Regex flags compatible with the re module.
                Default: 0.
            stripped (bool, optional): Whether to strip the text of the paragraph before
                comparison. Default: True.

        Returns:
            ParagraphList: The filtered list.
        """

        regex_func=re.search if substring_match else re.match

        new_indexes = set(
            paragraph._index
            for paragraph in self
            if regex_func(regex, paragraph.Text, flags=regex_flags)
        )

        return ParagraphList(self.document, new_indexes)


    def filter_by_paragraph_names(self, *paragraph_names: str) -> "ParagraphList":
        """
        Filter for paragraphs within any paragraph with any of the given names.

        See the paragraphing documentation for more details.

        Args:
            *paragraph_names (str): The paragraph names to filter for.

        Returns:
            ParagraphList: The filtered list.
        """
        new_indexes: Set[int] = set()
        for paragraph_name in paragraph_names:
            for paragraph in self.document.paragraphs.get_paragraphs_with_name(
                paragraph_name
            ):
                new_indexes |= set(paragraph._index for paragraph in paragraph.paragraphs)
        return self.__intersect_indexes_with_self(new_indexes)


    def to_the_right_of(
        self, paragraph: "PDFparagraph", inclusive: bool = False, tolerance: float = 0.0
    ) -> "ParagraphList":
        """
        Filter for paragraphs which are to the right of the given paragraph.

        If you draw a box from the right hand edge of the paragraph to the right hand
        side of the page, all paragraphs which are partially within this box are returned.

        Note:
            By "to the right of" we really mean "directly to the right of", i.e. the
            returned paragraphs all have at least some part which is vertically aligned
            with the specified paragraph.

        Note:
            Technically the paragraph you specify will satisfy the condition, but we
            assume you do not want that paragraph returned. If you do, you can pass
            `inclusive=True`.

        Args:
            paragraph (PDFparagraph): The paragraph in question.
            inclusive (bool, optional): Whether the include `paragraph` in the returned
                results. Default: False.
            tolerance (int, optional): To be counted as to the right, the paragraphs must
                overlap by at least `tolerance` on the Y axis. Tolerance is capped at
                half the height of the paragraph. Default 0.

        Returns:
            ParagraphList: The filtered list.
        """
        page_number = paragraph.page_number
        page = self.document.get_page(page_number)
        tolerance = min(paragraph.height / 2, tolerance)
        bounding_box = BoundingBox(
            paragraph.x1,
            page.width,
            paragraph.y0 + tolerance,
            paragraph.y1 - tolerance,
        )
        results = self.filter_partially_within_bounding_box(bounding_box, page_number)
        if not inclusive:
            results = results.remove_paragraph(paragraph)
        return results

    def to_the_left_of(
        self, paragraph: "PDFparagraph", inclusive: bool = False, tolerance: float = 0.0
    ) -> "ParagraphList":
        """
        Filter for paragraphs which are to the left of the given paragraph.


        If you draw a box from the left hand edge of the paragraph to the left hand
        side of the page, all paragraphs which are partially within this box are returned.

        Note:
            By "to the left of" we really mean "directly to the left of", i.e. the
            returned paragraphs all have at least some part which is vertically aligned
            with the specified paragraph.

        Note:
            Technically the paragraph you specify will satisfy the condition, but we
            assume you do not want that paragraph returned. If you do, you can pass
            `inclusive=True`.

        Args:
            paragraph (PDFparagraph): The paragraph in question.
            inclusive (bool, optional): Whether the include `paragraph` in the returned
                results. Default: False.
            tolerance (int, optional): To be counted as to the left, the paragraphs must
                overlap by at least `tolerance` on the Y axis. Tolerance is capped at
                half the height of the paragraph. Default 0.


        Returns:
            ParagraphList: The filtered list.
        """
        page_number = paragraph.page_number
        tolerance = min(paragraph.bounding_box.height / 2, tolerance)
        bounding_box = BoundingBox(
            0,
            paragraph.bounding_box.x0,
            paragraph.bounding_box.y0 + tolerance,
            paragraph.bounding_box.y1 - tolerance,
        )
        results = self.filter_partially_within_bounding_box(bounding_box, page_number)
        if not inclusive:
            results = results.remove_paragraph(paragraph)
        return results

    def below(
        self,
        paragraph: "PDFparagraph",
        inclusive: bool = False,
        all_pages: bool = False,
        tolerance: float = 0.0,
    ) -> "ParagraphList":
        """
        Returns all paragraphs which are below the given paragraph.

        If you draw a box from the bottom edge of the paragraph to the bottom of the page,
        all paragraphs which are partially within this box are returned. By default, only
        paragraphs on the same page as the given paragraph are included, but you can pass
        `inclusive=True` to also include the pages which come after (and so are below)
        the page containing the given paragraph.

        Note:
            By "below" we really mean "directly below", i.e. the returned paragraphs all
            have at least some part which is horizontally aligned with the specified
            paragraph.

        Note:
            Technically the paragraph you specify will satisfy the condition, but we
            assume you do not want that paragraph returned. If you do, you can pass
            `inclusive=True`.

        Args:
            paragraph (PDFparagraph): The paragraph in question.
            inclusive (bool, optional): Whether the include `paragraph` in the returned
                results. Default: False.
            all_pages (bool, optional): Whether to included pages other than the page
                which the paragraph is on.
            tolerance (int, optional): To be counted as below, the paragraphs must
                overlap by at least `tolerance` on the X axis. Tolerance is capped at
                half the width of the paragraph. Default 0.

        Returns:
            ParagraphList: The filtered list.
        """
        page_number = paragraph.page_number
        tolerance = min(paragraph.bounding_box.width / 2, tolerance)
        bounding_box = BoundingBox(
            paragraph.bounding_box.x0 + tolerance,
            paragraph.bounding_box.x1 - tolerance,
            0,
            paragraph.bounding_box.y0,
        )
        results = self.filter_partially_within_bounding_box(bounding_box, page_number)
        if all_pages:
            for page in self.document.pages:
                if page.page_number <= page_number:
                    continue
                # We're on a page which is located below our paragraph, so the bounding
                # box should be the length of the entire page.
                bounding_box = BoundingBox(
                    paragraph.bounding_box.x0 + tolerance,
                    paragraph.bounding_box.x1 - tolerance,
                    0,
                    page.height,
                )
                results = results | self.filter_partially_within_bounding_box(
                    bounding_box, page.page_number
                )
        if not inclusive:
            results = results.remove_paragraph(paragraph)
        return results

    def above(
        self,
        paragraph: "PDFparagraph",
        inclusive: bool = False,
        all_pages: bool = False,
        tolerance: float = 0.0,
    ) -> "ParagraphList":
        """
        Returns all paragraphs which are above the given paragraph.

        If you draw a box from the bottom edge of the paragraph to the bottom of the page,
        all paragraphs which are partially within this box are returned. By default, only
        paragraphs on the same page as the given paragraph are included, but you can pass
        `inclusive=True` to also include the pages which come before (and so are above)
        the page containing the given paragraph.

        Note:
            By "above" we really mean "directly above", i.e. the returned paragraphs all
            have at least some part which is horizontally aligned with the specified
            paragraph.

        Note:
            Technically the paragraph you specify will satisfy the condition, but we
            assume you do not want that paragraph returned. If you do, you can pass
            `inclusive=True`.

        Args:
            paragraph (PDFparagraph): The paragraph in question.
            inclusive (bool, optional): Whether the include `paragraph` in the returned
                results. Default: False.
            all_pages (bool, optional): Whether to included pages other than the page
                which the paragraph is on.
            tolerance (int, optional): To be counted as above, the paragraphs must
                overlap by at least `tolerance` on the X axis. Tolerance is capped at
                half the width of the paragraph. Default 0.

        Returns:
            ParagraphList: The filtered list.
        """
        page_number = paragraph.page_number
        page = self.document.get_page(page_number)
        tolerance = min(paragraph.bounding_box.width / 2, tolerance)
        bounding_box = BoundingBox(
            paragraph.bounding_box.x0 + tolerance,
            paragraph.bounding_box.x1 - tolerance,
            paragraph.bounding_box.y1,
            page.height,
        )
        results = self.filter_partially_within_bounding_box(bounding_box, page_number)
        if all_pages:
            for page in self.document.pages:
                if page.page_number >= page_number:
                    continue
                # We're on a page which is located above our paragraph, so the bounding
                # box should be the length of the entire page.
                bounding_box = BoundingBox(
                    paragraph.bounding_box.x0 + tolerance,
                    paragraph.bounding_box.x1 - tolerance,
                    0,
                    page.height,
                )
                results = results | self.filter_partially_within_bounding_box(
                    bounding_box, page.page_number
                )
        if not inclusive:
            results = results.remove_paragraph(paragraph)
        return results


    def before(self, paragraph: "PDFparagraph", inclusive: bool = False) -> "ParagraphList":
        """
        Returns all paragraphs before the specified paragraph.

        By before, we mean preceding paragraphs according to their index. The PDFDocument
        will order paragraphs according to the specified paragraph_ordering (which defaults
        to left to right, top to bottom).

        Args:
            paragraph (PDFparagraph): The paragraph in question.
            inclusive (bool, optional): Whether the include `paragraph` in the returned
                results. Default: False.

        Returns:
            ParagraphList: The filtered list.
        """
        new_indexes = set(range(0, paragraph._index))
        if inclusive:
            new_indexes.add(paragraph._index)
        return self.__intersect_indexes_with_self(new_indexes)

    def after(self, paragraph: "PDFparagraph", inclusive: bool = False) -> "ParagraphList":
        """
        Returns all paragraphs after the specified paragraph.

        By after, we mean succeeding paragraphs according to their index. The PDFDocument
        will order paragraphs according to the specified paragraph_ordering (which defaults
        to left to right, top to bottom).

        Args:
            paragraph (PDFparagraph): The paragraph in question.
            inclusive (bool, optional): Whether the include `paragraph` in the returned
                results. Default: False.

        Returns:
            ParagraphList: The filtered list.
        """
        new_indexes = set(range(paragraph._index + 1, max(self.indexes) + 1))
        if inclusive:
            new_indexes.add(paragraph._index)
        return self.__intersect_indexes_with_self(new_indexes)


    def extract_single_paragraph(self) -> "PDFparagraph":
        """
        Returns only paragraph in the paragraphList, provided there is only one paragraph.

        This is mainly for convenience, when you think you've filtered down to a single
        paragraph and you would like to extract said paragraph.

        Raises:
            NoparagraphFoundError: If there are no paragraphs in the paragraphList
            MultipleparagraphsFoundError: If there is more than one paragraph in the
                paragraphList

        Returns:
            PDFparagraph: The single paragraph remaining in the list.
        """
        if len(self.indexes) == 0:
            raise NoParagraphFoundError("There are no paragraphs in the paragraphList")

        return self.document._paragraph_list[list(self.indexes)[0]]

    def extract_paragraphs(self) -> "PDFparagraph":
        """
        Returns only paragraph in the paragraphList, provided there is only one paragraph.

        This is mainly for convenience, when you think you've filtered down to a single
        paragraph and you would like to extract said paragraph.

        Raises:
            NoparagraphFoundError: If there are no paragraphs in the paragraphList
            MultipleparagraphsFoundError: If there is more than one paragraph in the
                paragraphList

        Returns:
            PDFparagraph: The single paragraph remaining in the list.
        """
        if len(self.indexes) == 0:
            raise NoParagraphFoundError("There are no paragraphs in the paragraphList")


        return self.document._paragraph_list[list(self.indexes)]

    def remove_paragraph(self, paragraph: "PDFparagraph") -> "ParagraphList":
        """
        Explicitly removes the paragraph from the paragraphList.

        Note:
            If the paragraph is not in the paragraphList, this does nothing.

        Args:
            paragraph (PDFparagraph): The paragraph to remove.

        Returns:
            ParagraphList: A new list without the paragraph.
        """
        return ParagraphList(self.document, self.indexes - set([paragraph._index]))

    def remove_paragraphs(self, *paragraphs: "PDFparagraph") -> "ParagraphList":
        """
        Explicitly removes the paragraphs from the paragraphList.

        Note:
            If the paragraphs are not in the paragraphList, this does nothing.

        Args:
            *paragraphs (PDFparagraph): The paragraphs to remove.

        Returns:
            ParagraphList: A new list without the paragraphs.
        """
        return ParagraphList(
            self.document, self.indexes - set(paragraph._index for paragraph in paragraphs)
        )

    def __iter__(self) -> ParagraphIterator:
        """
        Returns an paragraphIterator class that allows iterating through paragraphs.

        paragraphs will be returned in order of the paragraphs in the document,
        left-to-right, top-to-bottom (the same as you read).
        """
        return ParagraphIterator(self)

    def __contains__(self, paragraph: "PDFparagraph") -> bool:
        """
        Returns True if the paragraph is in the paragraphList, otherwise False.
        """
        return paragraph._index in self.indexes

    def __repr__(self):
        return f"<paragraphList of {len(self.indexes)} paragraphs>"

    @overload
    def __getitem__(self, key: int) -> "PDFparagraph":
        pass  # This is for type checking only

    @overload
    def __getitem__(self, key: slice) -> "ParagraphList":
        pass  # This is for type checking only

    def __getitem__(self, key: Union[int, slice]) -> Union["PDFparagraph", "ParagraphList"]:
        """
        Returns the paragraph in position `key` of the paragraphList if an int is given, or
        returns a new paragraphList if a slice is given.

        paragraphs are ordered by their original positions in the document, which is
        left-to-right, top-to-bottom (the same you you read).
        """
        if isinstance(key, slice):
            new_indexes = set(sorted(self.indexes)[key])
            return ParagraphList(self.document, new_indexes)
        paragraph_index = sorted(self.indexes)[key]
        return self.document._paragraph_list[paragraph_index]

    def __eq__(self, other: object) -> bool:
        """
        Returns True if the two paragraphLists contain the same paragraphs from the same
        document.
        """
        if not isinstance(other, ParagraphList):
            raise NotImplementedError(f"Can't compare paragraphList with {type(other)}")
        return (
            self.indexes == other.indexes
            and self.document == other.document
            and self.__class__ == other.__class__
        )

    def __hash__(self):
        return hash(hash(self.indexes) + hash(self.document))

    def __len__(self):
        """
        Returns the number of paragraphs in the paragraphList.
        """
        return len(self.indexes)

    def __sub__(self, other: "ParagraphList") -> "ParagraphList":
        """
        Returns an paragraphList of paragraphs that are in the first paragraphList but not in
        the second.
        """
        return ParagraphList(self.document, self.indexes - other.indexes)

    def __or__(self, other: "ParagraphList") -> "ParagraphList":
        """
        Returns an paragraphList of paragraphs that are in either paragraphList
        """
        return ParagraphList(self.document, self.indexes | other.indexes)

    def __xor__(self, other: "ParagraphList") -> "ParagraphList":
        """
        Returns an paragraphList of paragraphs that are in either paragraphList, but not both.
        """
        return ParagraphList(self.document, self.indexes ^ other.indexes)

    def __and__(self, other: "ParagraphList") -> "ParagraphList":
        """
        Returns an paragraphList of paragraphs that are in both paragraphList
        """
        return ParagraphList(self.document, self.indexes & other.indexes)
