from pdf2txt.utils import get_page_layout
from pdf2txt.components.pdf_page import PDFPage
from pdf2txt.utils import get_fonts_statistics
from collections import Counter, defaultdict
from typing import Callable, Dict, List, Set, Optional, Union, TYPE_CHECKING
from pdf2txt.exceptions import NoTokensOnPageError, PageNotFoundError
from pdf2txt.tokens_filtering import LineList
from pdf2txt.paragraph_list import ParagraphList
from itertools import chain
from pdf2txt.components.paragraphs import Paragraphs

import re



import pandas as pd

class PDFDocument(object):
    def __init__(self, pdf= None, font_mapping= None, regex_flags = 0):

        self.file_path=pdf
        page_number = 0
        self.title=[]

        self._token_list = []
        self._token_indexes_by_font = defaultdict(set)
        self._font_mapping = font_mapping if font_mapping is not None else {}
        self._regex_flags = regex_flags
#        self._ignored_indexes = set()
        self.__pages = {}
        self.font_statistics={}
        self.paragraphs=Paragraphs(self)
        idx=0
        for layout, _ in get_page_layout(pdf):
            page_number += 1
            page=PDFPage(self, layout, page_number=page_number)
            page.detect_semantic_structure()
            self.__pages[page_number]=page

            first_token = None
        for paragrah in self.paragraphs.paragraphs:

            for token in [paragrah.title]+paragrah.pdflines if paragrah.title else paragrah.pdflines:
                token.index=idx
                self._token_list.append(token)
                idx += 1


        self.font_statistics=get_fonts_statistics([line for page in self.pages for line in page.horizental_text_lines])

    @property
    def pages(self) -> List["PDFPage"]:
        """
        A list of all pages in the document.

        Returns:
            list[PDFPage]: All pages in the document.
        """
        return [self.__pages[page_number] for page_number in sorted(self.__pages)]


    @property
    def lines(self) -> "LineList":
        """
        An TokenList containing all tokens in the document.

        Returns:
            LineList: All tokens in the document.
        """
        return LineList(self)


    @property
    def fonts(self) -> Set[str]:
        """
        A set of all the fonts in the document.

        Returns:
            set[str]: All the fonts in the document.
        """
        return set(token.font for token in self.lines)

    def get_page(self, page_number: int) -> "PDFPage":
        """
        Returns the `PDFPage` for the specified `page_number`.

        Args:
            page_number (int): The page number.

        Raises:
            PageNotFoundError: If `page_number` was not found.

        Returns:
            PDFPage: The requested page.
        """
        try:
            return self.__pages[page_number]
        except KeyError as err:
            raise PageNotFoundError(f"Could not find page {page_number}") from err

    def _token_indexes_with_fonts(self, *fonts: str) -> Set[int]:
        """
        Returns all the indexes of tokens with given fonts.
        For internal use only, used to cache fonts. If you want to filter by fonts you
        should use tokens.filter_by_fonts instead.

        Args:
            *fonts (str): The fonts to filter for.

        Returns:
            Set[int]: The tokens indexes.
        """
        non_cached_fonts = [
            font for font in fonts if font not in self._token_indexes_by_font.keys()
        ]
        if non_cached_fonts:
            # If we don't have cached tokens for any of the required fonts, build
            # the cache for the non cached fonts.
            for token in self._token_list:
                if token.font not in non_cached_fonts:
                    continue

                self._token_indexes_by_font[token.font].add(token._index)

        # Returns tokens based on the caching of fonts to tokens indexes.
        return set(
            chain.from_iterable(
                [
                    indexes
                    for font, indexes in self._token_indexes_by_font.items()
                    if font in fonts
                ]
            )
        )


    def get_features(self):
        return pd.DataFrame([feature for page in self.pages for feature in page.get_features()])

    def detect_semantic_structure(self):
        for page in self.pages:
            page.detect_semantic_structure()

    def to_text(self):
        return '\n'.join([p.Text+'\n' for p in self.paragraphs.paragraphs])
