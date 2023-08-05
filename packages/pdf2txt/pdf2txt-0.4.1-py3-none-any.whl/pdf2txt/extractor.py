'''
pdf2textbox.py

:param url: A URL pointing at a PDF file with max 3 columns and a header
:returns: Returns a dict containing text items that have been extracted from PDF
:raises NameError
:raises UnboundLocalError
:raises PDFTextExtractionNotAllowed
'''

from pdf2txt.components.pdf_document import *

from pdf2txt.tables import extract_table, extract_table_from_chart

def pdf_to_text_all(pdf, detect_regions=False):
    '''
    Converts PDF documents with up to three columns into text.
    Will convert the whole document, or die trying.
    Determine layout (vertical/horizontal) first.
    Calculate the number of columns:
        - get the width of boxes
        - divide max horizontal width by max box width
          --> nr of columns
    Determine if there is a header. This is done in two steps.
    Create a dictionary organized in pagenumber, header, columns.
    Enter text into dictionary.
    Return dictionary.
    '''


    regex=r"\d{1,2}\s(August)\s\d{4}"


#    layout_kwargs = {}
#   pages_layouts=get_pdf_layout(pdf, **layout_kwargs)

    pdf_doc=PDFDocument(pdf)
    # currency = pdf_doc.lines.filter_by_text_contains("Currency of share class").extract_single_token()#.text()
    #
    # currency_text = pdf_doc.lines.to_the_right_of(currency).extract_single_token()
    #
    # date = pdf_doc.lines.filter_by_regex(r"(Aug)\s\d{2}(,)?\s\d{4}").extract_single_token()#.text()
    #
#    paragraph=pdf_doc.paragraphs.filter_by_text_contains(['SECTOR'], filter_type='all')
#    table= extract_table(paragraph)

#    print(table.to_text())
    return pdf_doc.to_text()
