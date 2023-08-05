from typing import TYPE_CHECKING, Any, List, Set, Dict, Optional
from pdf2txt.components import TokenBase as BoundingBox
import pandas as pd

from itertools import chain, zip_longest

from .exceptions import (
    TableExtractionError,
    NoTokenFoundError,
    MultipleTokensFoundError,
    InvalidTableError,
    InvalidTableHeaderError,
)

if TYPE_CHECKING:
    from .tokens_filtering import LineList
    from .components import PDFToken


class Table(object):
    """Defines a table with coordinates relative to a left-bottom
    origin. (PDF coordinate space)
    Parameters
    ----------
    cols : list
        List of tuples representing column x-coordinates in increasing
        order.
    rows : list
        List of tuples representing row y-coordinates in decreasing
        order.
    Attributes
    ----------
    df : :class:`pandas.DataFrame`
    shape : tuple
        Shape of the table.
    accuracy : float
        Accuracy with which text was assigned to the cell.
    whitespace : float
        Percentage of whitespace in the table.
    order : int
        Table number on PDF page.
    page : int
        PDF page number.
    """

    def __init__(self):

        self.cells = []
        self.df = None
        self.accuracy = 0
        self.whitespace = 0
        self.order = None
        self.page = None

    def __repr__(self):
        return f"<{self.__class__.__name__} shape={self.shape}>"

    def __lt__(self, other):
        if self.page == other.page:
            if self.order < other.order:
                return True
        if self.page < other.page:
            return True
    @property
    def shape(self):
        return (len(self. cells), len(self.cells[0]) if len(self.cells[0]) else 0)

    def add_row(self, row):
        self.cells.append(row)
        self.df=pd.DataFrame([[col.Text if col else None for col in row] for  row in self.cells])
    @property
    def data(self):
        """Returns two-dimensional list of strings in table.
        """
        d = []
        for row in self.cells:
            d.append([cell.Text for cell in row])
        return d



    def to_pandas(self):
        if self.df is None:
            self.df=pd.DataFrame(self.cells)
        return self.df

    def to_text(self):
       return self.df.to_string()

    def to_json(self, path, **kwargs):
        """Writes Table to a JSON file.
        For kwargs, check :meth:`pandas.DataFrame.to_json`.
        Parameters
        ----------
        path : str
            Output filepath.
        """
        kw = {"orient": "records"}
        kw.update(kwargs)
        json_string = self.df.to_json(**kw)
        with open(path, "w") as f:
            f.write(json_string)

    def to_excel(self, path, **kwargs):
        """Writes Table to an Excel file.
        For kwargs, check :meth:`pandas.DataFrame.to_excel`.
        Parameters
        ----------
        path : str
            Output filepath.
        """
        kw = {
            "sheet_name": f"page-{self.page}-table-{self.order}",
            "encoding": "utf-8",
        }
        kw.update(kwargs)
        writer = pd.ExcelWriter(path)
        self.df.to_excel(writer, **kw)
        writer.save()

    def to_html(self, path, **kwargs):
        """Writes Table to an HTML file.
        For kwargs, check :meth:`pandas.DataFrame.to_html`.
        Parameters
        ----------
        path : str
            Output filepath.
        """
        html_string = self.df.to_html(**kwargs)
        with open(path, "w") as f:
            f.write(html_string)


def extract_simple_table(
    tokens: "LineList",
    as_text: bool = False,
    strip_text: bool = True,
    allow_gaps: bool = False,
    reference_token: Optional["PDFToken"] = None,
    tolerance: float = 0.0,
    remove_duplicate_header_rows: bool = False,
) -> List[List]:
    """
    Returns tokens structured as a table.

    Given an TokenList, tries to extract a structured table by examining which
    tokens are aligned.

    To use this function, there must be at least one full row and one full column (which
    we call the reference row and column), i.e. the reference row must have an token
    in every column, and the reference column must have an token in every row. The
    reference row and column can be specified by passing the single token in both the
    reference row and the reference column. By default, this is the top left token,
    which means we use the first row and column as the references. Note if you need to
    change the reference_token, that means you have gaps in your table, and as such
    you will need to pass `allow_gaps=True`.

    Important: This function uses the tokens in the reference row and column to scan
    horizontally and vertically to find the rest of the table. If there are gaps in your
    reference row and column, this could result in rows and columns being missed by
    this function.

    There must be a clear gap between each row and between each column which contains no
    tokens, and a single cell cannot contain multiple tokens.

    If there are no valid reference rows or columns, try extract_table() instead. If you
    have tokens spanning multiple rows or columns, it may be possible to fix this by
    using extract_table(). If you fail to satisfy any of the other conditions listed
    above, that case is not yet supported.

    Args:
        tokens (LineList): A list of tokens to extract into a table.
        as_text (bool, optional): Whether to extract the text from each token instead
            of the PDFToken itself. Default: False.
        strip_text (bool, optional): Whether to strip the text for each token of the
                table (Only relevant if as_text is True). Default: True.
        allow_gaps (bool, optional): Whether to allow empty spaces in the table.
        reference_token (PDFToken, optional): An token in a full row and a full
            column. Will be used to specify the reference row and column. If None, the
            top left token will be used, meaning the top row and left column will be
            used. If there are gaps in these, you should specify a different reference.
            Default: None.
        tolerance (int, optional): For tokens to be counted as in the same row or
            column, they must overlap by at least `tolerance`. Default: 0.
        remove_duplicate_header_rows (bool, optional): Remove duplicates of the header
            row (the first row) if they exist. Default: False.

    Raises:
        TableExtractionError: If something goes wrong.

    Returns:
        list[list]: a list of rows, which are lists of PDFTokens or strings
            (depending on the value of as_text).
    """
    if reference_token is None:
        reference_token = tokens[0]
    reference_row = tokens.horizontally_in_line_with(
        reference_token, inclusive=True, tolerance=tolerance
    )
    reference_column = tokens.vertically_in_line_with(
        reference_token, inclusive=True, tolerance=tolerance, all_pages=True
    )

    reference_columns = [
        tokens.vertically_in_line_with(
            token, inclusive=True, tolerance=tolerance, all_pages=True
        )
        for token in reference_row
    ]
    reference_rows = [
        tokens.horizontally_in_line_with(token, inclusive=True, tolerance=tolerance)
        for token in reference_column
    ]

    table: List[List] = []
    for current_row in reference_rows:
        row: List = []
        for current_column in reference_columns:
            token = current_row & current_column
            try:
                row.append(token.extract_single_token())
            except NoTokenFoundError as err:
                if allow_gaps:
                    row.append(None)
                else:
                    raise TableExtractionError(
                        "Token not found, there appears to be a gap in the table. "
                        "If this is expected, pass allow_gaps=True."
                    ) from err
            except MultipleTokensFoundError as err:
                raise TableExtractionError(
                    "Multiple tokens appear to be in the place of one cell in the "
                    "table. Please try extract_table() instead."
                ) from err
        table.append(row)

    table_size = sum(
        len([token for token in row if token is not None]) for row in table
    )
    if table_size != len(tokens):
        raise TableExtractionError(
            f"Number of tokens in table ({table_size}) does not match number of "
            f"tokens passed ({len(tokens)}). Perhaps try extract_table instead of "
            "extract_simple_table, or change you reference token."
        )

    if remove_duplicate_header_rows:
        table = _remove_duplicate_header_rows(table)

    if as_text:
        return get_text_from_table(table, strip_text=strip_text)

    _validate_table_shape(table)
    return table

def vertically_in_line_with( token: "PDFtoken", linelist: "LineList", tolerance: float = 0.0, ):

        page_number = token.page_number
        page = linelist.document.get_page(page_number)

        tolerance = min(token.width / 2, tolerance)
        bounding_box = BoundingBox(
            token.x0 - tolerance,
            token.x1 + tolerance,
            0,
            page.height,
        )
        results = set()


        for line in linelist:
            for tok in line.tokens:
                if tok.partially_within(bounding_box):
                    results.add(tok)
        return frozenset(results)


def horizontally_in_line(row, rows, inclusive: bool = False, tolerance: float = 0.0):

        if len(rows)==0:
            return None

        page = row.page


        tolerance = min(row.height / 2, tolerance)
        bounding_box = BoundingBox(
            0,
            page.width,
            row.y0 + tolerance,
            row.y1 - tolerance,
        )

        for r in rows:
            for token in list(r):
                if token.partially_within(bounding_box):
                    return r
        return None

def extract_table(
    lines: "LineList",
    fix_token_in_multiple_rows: bool = True,
    fix_token_in_multiple_cols: bool = True,
    tolerance: float = 10.0
) -> List[List]:
    """
    Returns tokens structured as a table.

    Given an TokenList, tries to extract a structured table by examining which
    tokens are aligned. There must be a clear gap between each row and between each
    column which contains no tokens, and a single cell cannot contain multiple
    tokens.

    If you fail to satisfy any of the other conditions listed above, that case is not
    yet supported.

    Note: If you satisfy the conditions to use extract_simple_table, then that should be
    used instead, as it's much more efficient.

    Args:
        lines (LineList): A list of tokens to extract into a table.
        as_text (bool, optional): Whether to extract the text from each line instead
            of the PDFToken itself. Default: False.
        fix_token_in_multiple_rows (bool, optional): If a table line is in line
            with tokens in multiple rows, a TableExtractionError will be raised unless
            this argument is set to True. When True, any tokens detected in multiple
            rows will be placed into the first row. This is only recommended if you
            expect this to be the case in your table. Default: False.
        fix_token_in_multiple_cols (bool, optional): If a table line is in line
            with tokens in multiple cols, a TableExtractionError will be raised unless
            this argument is set to True. When True, any tokens detected in multiple
            cols will be placed into the first col. This is only recommended if you
            expect this to be the case in your table. Default: False.
        tolerance (int, optional): For tokens to be counted as in the same row or
            column, they must overlap by at least `tolerance`. Default: 0.


    Raises:
        TableExtractionError: If something goes wrong.

    Returns:
        list[list]: a list of rows, which are lists of PDFTokens or strings
            (depending on the value of as_text).
    """
    table = Table()
    rows = set()
    cols = set()

    for line in lines:
        row = line.tokens
        r=horizontally_in_line(line, rows)
        if r:
            rows.remove(r)
            r=list(r)
            r.extend(row)
            rows.add(frozenset(r))
        else:
            rows.add(frozenset(row))
        for token in line.tokens:
            col = vertically_in_line_with(
                token, lines, tolerance=tolerance
            )
            cols.add(col)

    # Check no line is in multiple rows or columns
    if fix_token_in_multiple_rows:
        _fix_rows(rows, lines)
    if fix_token_in_multiple_cols:
        cols=_fix_cols(cols, lines)
    print(sum([len(row) for row in rows]))
    if sum([len(row) for row in rows]) != len(list(chain.from_iterable(rows))):
        raise TableExtractionError(
            "An line is in multiple rows. If this is expected, you can try passing "
            "fix_token_in_multiple_rows=True"
        )
    if sum([len(col) for col in cols]) != len(list(chain.from_iterable(cols))):
        raise TableExtractionError(
            "An line is in multiple columns. If this is expected, you can try "
            "passing fix_token_in_multiple_cols=True"
        )

    sorted_rows = sorted(
        rows,
        key=lambda row: (
#            row[0].page_number,
            max(-(elem.y1) for elem in row),
        ),
    )
    sorted_cols = sorted(
        cols, key=lambda col: max(elem.x0 for elem in col)
    )

    for row in sorted_rows:
        table_row = []
        for col in sorted_cols:
            try:
                line = row.intersection(col)
            except NoTokenFoundError:
                line = None
            except MultipleTokensFoundError as err:
                raise TableExtractionError(
                    "Multiple tokens appear to be in the place of one cell in the "
                    "table. It could be worth trying to add a tolerance."
                ) from err
            table_row.append(list(line)[0] if len(line) else None)
        table.add_row(table_row)

    _validate_table_shape(table)
    return table


def extract_table_from_chart(
    lines: "LineList",
    fix_token_in_multiple_rows: bool = True,
    fix_token_in_multiple_cols: bool = True,
    tolerance: float = 10.0
) -> List[List]:

    table = Table()
    rows = set()
    cols = set()

    for line in lines:
        row = sorted(line.tokens, key=lambda token:token.x0)
        r=horizontally_in_line(line, rows)
        if r:
            rows.remove(r)
            r=list(r)
            r.extend(row)
            rows.add(frozenset(r))
        else:
            rows.add(frozenset(row))

    cols=set(map(frozenset, zip_longest(*[line.tokens for line in lines], fillvalue=None)))




    if sum([len(row) for row in rows]) != len(list(chain.from_iterable(rows))):
        raise TableExtractionError(
            "An line is in multiple rows. If this is expected, you can try passing "
            "fix_token_in_multiple_rows=True"
        )
    if sum([len(col) for col in cols]) != len(list(chain.from_iterable(cols))):
        raise TableExtractionError(
            "An line is in multiple columns. If this is expected, you can try "
            "passing fix_token_in_multiple_cols=True"
        )

    sorted_rows = sorted(
        rows,
        key=lambda row: (
#            row[0].page_number,
            max(-(elem.y1) for elem in row),
        ),
    )
    sorted_cols = sorted(
        cols, key=lambda col: max(elem.x0 for elem in col)
    )

    for row in sorted_rows:
        table_row = []
        for col in sorted_cols:
            try:
                line = row.intersection(col)
            except NoTokenFoundError:
                line = None
            except MultipleTokensFoundError as err:
                raise TableExtractionError(
                    "Multiple tokens appear to be in the place of one cell in the "
                    "table. It could be worth trying to add a tolerance."
                ) from err
            table_row.append(list(line)[0] if len(line) else None)
        table.add_row(table_row)

    _validate_table_shape(table)
    return table


def add_header_to_table(
    table: List[List[str]], header: Optional[List[str]] = None
) -> List[Dict[str, str]]:
    """
    Given a table (list of lists) of strings, returns a list of dicts mapping the
    table header to the values.

    Given a table, a list of rows which are lists of strings, returns a new table
    which is a list of rows which are dictionaries mapping the header values to the
    table values.

    Args:
        table: The table (a list of lists of strings).
        header (list, optional): The header to use. If not provided, the first row of
            the table will be used instead. Your header must be the same width as your
            table, and cannot contain the same entry multiple times.

    Raises:
        InvalidTableHeaderError: If the width of the header does not match the width of
            the table, or if the header contains duplicate entries.

    Returns:
        list[dict]: A list of dictionaries, where each entry in the list is a row in the
        table, and a row in the table is represented as a dictionary mapping the header
        to the values.
    """
    _validate_table_shape(table)
    header_provided = bool(header)
    if len(table) == 0:
        return []
    if header is None:
        header = table[0]
    elif len(header) != len(table[0]):
        raise InvalidTableHeaderError(
            f"Header length of {len(header)} does not match the width of the table "
            f"({len(table[0])})"
        )
    if len(header) != len(set(header)):
        raise InvalidTableHeaderError("Header contains repeated tokens")
    new_table = []
    for row in table:
        new_row = {header[idx]: token for idx, token in enumerate(row)}
        new_table.append(new_row)

    if not header_provided:
        # The first row was the header, and we still mapped it. Remove it.
        # Note: We don't want to do table.pop(0) at the top as that would modify the
        # object that we were passed.
        new_table.pop(0)
    return new_table


def _validate_table_shape(table: Table):
    """
    Checks that all rows (and therefore all columns) are the same length.
    """
    if len(table.cells) < 1:
        return
    first_row_len = len(table.cells[0])
    for idx, row in enumerate(table.cells[1:]):
        if not len(row) == first_row_len:
            raise InvalidTableError(
                f"Table not rectangular, row 0 has {first_row_len} tokens but row "
                f"{idx + 1} has {len(row)}."
            )


def _fix_rows(rows: Set["LineList"], tokens: "LineList") -> None:
    """
    Sometimes an token may span over multiple rows. For example:
    ---------
    | A | B |
    ----|   |
    | C |   |
    ---------
    In this, case, when extract_table scans for token in line with A it will pick up
    A and B. When it scans B it will get A, B and C, and when it scans C it will get B
    and C. This results in three distinct rows, AB, ABC, BC. This function will fix
    this by putting any merged cells into the top row, resulting in one row AB and the
    other with just C.

    To do this, we check which token is in multiple rows, get which rows it is in,
    and then remove it from the lower rows. This should fix the problem. It can result
    in empty rows (since in my example we begin with 3 'rows' when there are only
    really 2), but these can simply be removed.
    """
    if sum([len(row) for row in rows]) == len(set(chain.from_iterable(rows))):
        # No tokens are in multiple rows, return.
        return

    sorted_rows = sorted(
        rows,
        key=lambda row: (
            row[0].page_number,
            max(-(elem.y1) for elem in row),
        ),
    )

    for token in tokens:
        num_rows = sum(token in row for row in rows)
        if num_rows == 1:
            continue
        # If we reach here, we've found an token in multiple rows.

        rows_with_token = [row for row in rows if token in row]
        sorted_rows_with_token = sorted(
            rows_with_token, key=lambda row: sorted_rows.index(row)
        )
        # Remove the token from all but the first row.
        for row in sorted_rows_with_token[1:]:
            rows.remove(row)
            new_row = row.remove_token(token)
            if new_row:
                rows.add(new_row)
                # Update sorted rows
                sorted_rows = [
                    new_row if some_row == row else some_row for some_row in sorted_rows
                ]
            else:
                sorted_rows.remove(row)


def _fix_cols(cols: Set["LineList"], tokenlines: "LineList") -> None:
    """
    The same as _fix_rows, but when an token is in multiple columns, for example
    ---------
    | A | B |
    --------|
    |   C   |
    ---------
    """


    if sum([len(col) for col in cols]) == len(set(list(chain.from_iterable(cols)))):
        # No tokens are in multiple cols, return.
        return cols

    # We sort by looking at all the tokens and choosing the token which starts
    # most to the right. The ones with tokens which start most to the right
    # will be later on in the sorted list.

    cols=list(cols)

    sorted_columns = sorted(
        cols, key=lambda col: max(elem.x0 for elem in col)
    )
    for line in tokenlines:
        for token in line.tokens:
            num_cols = sum(token in list(col) for col in cols)
            if num_cols == 1:
                continue
            # If we reach here, we've found an token in multiple cols.

            cols_with_token = [col for col in cols if line in list(col)]
            sorted_cols_with_token = sorted(
                cols_with_token, key=lambda col: sorted_columns.index(col)
            )
            # Remove the token from all but the first col.
            for col in sorted_cols_with_token[1:]:
                cols.remove(col)
                new_col = list(col).remove(token)
                new_col=col
                if new_col:
                    set(cols).add(new_col)
                    cols=list(cols)
                    # Update sorted columns
                    sorted_columns = [
                        new_col if some_col == col else some_col
                        for some_col in sorted_columns
                    ]
                else:
                    sorted_columns.remove(col)
    return cols


def _remove_duplicate_header_rows(table: List[List[Any]]) -> List[List[Any]]:
    """
    Removes rows which are duplicates of the header (i.e., the first) row.
    A row is considered duplicate if all of its tokens have the same text and font of
    their correspondent tokens (i.e., same index) in the header row.

    Args:
        table (List[List[Any]]): The table to remove the duplicate headers from.

    Returns:
        List[List[Any]]: The table without the duplicate header rows.
    """
    if len(table) <= 1:
        return table

    header = table[0]
    rows_without_duplicate_header = [
        row
        for row in table[1:]
        if any(
            not _are_tokens_equal(token, header[index])
            for index, token in enumerate(row)
        )
    ]
    return [header] + rows_without_duplicate_header


def _are_tokens_equal(
    elem_1: Optional["PDFToken"], elem_2: Optional["PDFToken"]
) -> bool:
    """
    Checks if two tokens are equal.
    Two tokens are considered equal if they are both None or they have the same text
    and font.

    Args:
        elem_1 (PDFToken, optional): The first token to compare.
        elem_2 (PDFToken, optional): The second token to compare.

    Returns:
        bool: True if tokens are equal, False otherwise.
    """
    if elem_1 is None and elem_2 is None:
        return True

    if elem_1 is None or elem_2 is None:
        return False

    if elem_1.Text() != elem_2.Text() or elem_1.font != elem_2.font:
        return False

    return True
