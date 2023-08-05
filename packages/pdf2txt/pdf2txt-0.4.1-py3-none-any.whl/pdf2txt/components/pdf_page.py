from pdf2txt.core import TextEdges
from pdf2txt.utils import get_page_parameters, get_text_objects, get_graphical_object, isRectangleOverlap
from collections import namedtuple
from pdf2txt.components.pdf_components import *
from pdf2txt.utils import are_in_same_Line, get_fonts_statistics, has_ovelaping_rectangle
from pdf2txt.components.paragraphs import extract

import copy
import numpy as np
Area = namedtuple('Area', ['x0', 'y0', 'x1', 'y1'])


class PDFPage():
    def __init__(self, parent, layout, page_number, edge_tol=50, **kwargs):
        self.layout = layout
        self.document = parent
        self.number = page_number
        self.edge_tol = edge_tol
        self._init_layout()
        self.header = []
        self.footer = []
        self.paragraphs = []

        self.start_token = None
        self.end_token = None
        if len(self.horizental_text_lines)>0:
            self.font_statistics = get_fonts_statistics(self.horizental_text_lines)

    def _init_layout(self):

        self.width, self.height, self.margin_left, self.margin_right, self.margin_bottom, self.margin_top = get_page_parameters(
            self.layout)
        self.images = get_graphical_object(self.layout, ltype="image")
        self.text_boxes = get_text_objects(self.layout, ltype="text_box")
        self.horizontal_text = get_text_objects(self.layout, ltype="horizontal_text")
        self.vertical_text = get_text_objects(self.layout, ltype="vertical_text")
        self.graphical_lines = get_graphical_object(self.layout, ltype='line')
        self.graphical_rectangles = get_graphical_object(self.layout, ltype='rectangle')
        self.chart_data=get_graphical_object(self.layout, ltype='curve')
        self.fig_data=get_graphical_object(self.layout, ltype='figure')
        if len(self.horizontal_text)>0:
            self.horizental_text_lines = self._find_line_structure(self.horizontal_text)
        else:
            self.horizental_text_lines=[]

        self.regions = self._page_detection_algorithm()
        self.graphical_lines.sort(key=lambda x: -x.y1)
        self.graphical_rectangles.sort(key=lambda x: -x.y1)
    #
    # def _is_visible(self, span):
    #     text_color = span.font['color']
    #     if not span.font['visible']:
    #         return False
    #     surrounding_rectangle = get_bounding_object(span, self.graphical_rectangles)
    #     if surrounding_rectangle is None:
    #         return text_color != 'white'
    #     else:
    #         try:
    #             background_color = get_color_name([int(255 * c) for c in surrounding_rectangle.non_stroking_color])
    #         except Exception as e:
    #             return True
    #         return background_color['name'] != text_color

    # @property
    # def pdf_tokens(self):
    #     """
    #     Returns an `ElementList` containing all elements on the page.
    #
    #     Returns:
    #         ElementList: All the elements on the page.
    #     """
    #     if len(self.paragraphs)>0:
    #         return [tok for p in self.paragraphs for tok in p.pdf_tokens]



    def _find_line_structure(self, textlines):
        textlines.sort(key=lambda x: (-x.y1, x.x0))
        lines = []
        next_text = ""
        i = 0
        while i < len(textlines) - 1:

            text = textlines[i].get_text().strip()

            if len(text) == 0:
                i += 1
                continue

            text = PDFToken(textlines[i], self.document, i, self.number)
            if not text.is_visible:
                i += 1
                continue

            next_text = PDFToken(textlines[i + 1], self.document, i, self.number)
            while not next_text.is_visible:
                i += 1
                next_text = PDFToken(textlines[i + 1], self.document, i, self.number)

            line = PDFLine(self)
            line.tokens.append(text)
            while are_in_same_Line(text, next_text) and i < len(textlines) - 2:
                if len(next_text.Text.strip())==0 or not next_text.is_visible:
                    i += 1
                    next_text = PDFToken(textlines[i + 1], self.document, i, self.number)
                    continue

                separation = abs(text.x1 - next_text.x0)
                if separation <= 1.5 * text.font['width'] and text.font == next_text.font:
                    text.add(next_text)
                else:
                    line.tokens.append(next_text)
                i += 1
                #                text = Span(textlines[i])

                next_text = PDFToken(textlines[i + 1], self.document, i, self.number)

                continue

            line.tokens.sort(key=lambda x: x.x0, reverse=False)
            line.Num = len(lines)
            if len(lines):
                line.space_above = lines[-1].ypos - line.ypos
                lines[-1].space_below = lines[-1].ypos - line.ypos
            line.tokens=sorted(line.tokens, key=lambda elem: elem.x0)
            lines.append(line)

            i += 1
        # handle the last line
        if i == len(textlines) - 1 and next_text not in lines[-1].tokens:
            line = PDFLine(self)
            line.tokens.append(next_text)

            line.Num = len(lines)
            if len(lines):
                line.space_above = lines[-1].ypos - line.ypos
                lines[-1].space_below = lines[-1].ypos - line.ypos
                line.tokens = sorted(line.tokens, key=lambda elem: elem.x0)
            lines.append(line)

        return lines

    def get_features(self):
        return [line.get_feauture() for line in self.horizental_text_lines]

    def _page_detection_algorithm(self):

        textedges = TextEdges(edge_tol=2 * self.edge_tol)
        textedges.page_width = self.margin_right - self.margin_left
        textedges.page_height = self.height
        textedges.left_margin = self.margin_left

        # generate left, middle and right textedges
        textedges.generate2(self.horizental_text_lines)
        # guess vertical areas that are in the midle of a multi-column page
        vertical_bbox = textedges.get_column_separators(self.horizental_text_lines, self.graphical_lines,
                                                        textedges.left())
        table_areas = []


        if len(vertical_bbox) == 0:
            table_areas.append(Area(0, 0, self.width, self.height))
            return table_areas
        else:
            table_areas = self._get_areas_from_separators(vertical_bbox)
        textlines=[span for tl in self.horizental_text_lines for span in tl.tokens]

        if not len(table_areas):
            table_areas.append((0, 0, self.width, self.height))
        return table_areas


    def _get_areas_from_separators(self, separators):
        table_areas = []

        Area = namedtuple('Area', ['x0', 'y0', 'x1', 'y1'])

        # sort vertical lines by desending order of top edge (this allow to form the top area
        separators.sort(key=lambda te: -te.y1)
        #        self.plot_page(separators)
        left = self.margin_left
        top = self.margin_top
        right = self.margin_right

        last_separator = separators[0]
        for separaor in separators:
            bottom = separaor.y1
            # detect top page area
            if bottom < top:
                if last_separator.y0 > bottom:
                    top = last_separator.y0
                if last_separator.y1 > separaor.y1 > last_separator.y0:
                    if last_separator.x0 < separaor.x0:
                        left = last_separator.x0
                    else:
                        right = last_separator.x0
                # top area
                top_area = Area(left, bottom, right, top)
                if not has_ovelaping_rectangle(top_area, table_areas):
                    table_areas.append(top_area)
            #        self.plot_page(table_areas)
            # left area
            top = bottom
            right = separaor.x0
            sep_to_left = self._get_left_separator(separators, separaor)
            if sep_to_left:

                bottom = sep_to_left.y0 if sep_to_left.y0 > separaor.y0 else separaor.y0
                left = sep_to_left.x0

                table_areas.append(Area(left, bottom, right, top))
            #            self.plot_page(table_areas)
            else:
                bottom = separaor.y0
                table_areas.append(Area(left, bottom, right, top))
            #            self.plot_page(table_areas)
            # right area
            left = separaor.x0
            right = self.margin_right
            sep_to_right = self._get_right_separator(separators, separaor)
            if sep_to_right:
                bottom = sep_to_right.y1
                table_areas.append(Area(left, bottom, right, top))
                #            self.plot_page(table_areas)
                if sep_to_right.y0 > separaor.y0:
                    top = sep_to_right.y0
                    bottom = separaor.y0
                    table_areas.append(Area(left, bottom, right, top))
            #                self.plot_page(table_areas)
            else:
                right = self.margin_right
                table_areas.append(Area(left, bottom, right, top))
            #            self.plot_page(table_areas)

            top = separaor.y1
            last_separator = separaor
            left = self.margin_left

        # add area at the bottom. Should be last remaining
        separators.sort(key=lambda te: te.y0)

        top = separators[0].y0
        bottom = self.margin_bottom
        left = self.margin_left
        right = self.margin_right
        if bottom < top:
            table_areas.append(Area(left, bottom, right, top))
        #    self.plot_page(table_areas)

        return table_areas

    def _get_left_separator(self, sparators, separator):
        # separators are sorted acording to  decreasing y0
        for s in sparators:
            if s.x0 < separator.x0 and separator.y1 > s.y1 > separator.y0:
                return s
        return None

    def _get_right_separator(self, sparators, separator):
        # separators are sorted acording to  decreasing y0
        for s in sparators:
            if s.x0 > separator.x0 and separator.y1 > s.y1 > separator.y0:
                return s
        return None

    def _get_region_lines(self, region):
        region_lines = []
        for line in self.horizental_text_lines:
            new_line = PDFLine(self)
            for span in line.tokens:
                if isRectangleOverlap(span, region):
                    new_line.tokens.append(span)
            if len(new_line.tokens) > 0:
                new_line.Num = len(region_lines)
                if len(region_lines)>0:
                    new_line.space_above = region_lines[-1][1].y0 - new_line.y0
                    region_lines[-1][1].space_below = region_lines[-1][1].y0 - new_line.y0
                region_lines.append(('text', new_line))
        for gline in self.graphical_lines:
            if gline.width > 5.0 and isRectangleOverlap(gline, region):
                region_lines.append(['hline', gline])
            if gline.height > 5.0 and isRectangleOverlap(gline, region):
                region_lines.append(['vline', gline])
        region_lines.sort(key=lambda te: -te[1].y1)

        return region_lines

    def detect_semantic_structure(self):
        if len(self.horizental_text_lines)==0:
            return
        # sort in reading order
        NB_LINES_IN_HEADER = 3
        end_of_title = False
        self.regions.sort(key=lambda te: (-te.y1, te.x0))
        paragraphs=[]
        for region_number, region in enumerate(self.regions):
#            table= self.extract_tables([region])
#            print(table)
            region_lines = self._get_region_lines(region)

 #           if self.number == 1:
#                list_of_sizes = [line[1].spans[0].font['size'] for line in region_lines if line[0] == "text"]
#                index_of_line_with_max_size = list_of_sizes.index(max(list_of_sizes))
#                if index_of_line_with_max_size >= 3 and index_of_line_with_max_size <= 5:
 #               NB_LINES_IN_HEADER = 3#index_of_line_with_max_size + 1

            # find document title or page header
            title_font_cut_off = 12#self.document.font_statistics['second_largest_size']
            if len(self.font_statistics['all_sizes_by_frequency']) == 3:
                title_font_cut_off = self.font_statistics['largest_size']  # -0.1 #as we are comparing

            if title_font_cut_off < 11:  # titles souldn't be smaller than 11 pts.
                title_font_cut_off = 12

            if region_number == 0 and self.font_statistics['second_largest_size'] > 0:  # if second largest font doens not exist (-1), then there is only one font size in the page --> no title or sub title in this page:
                candidates_title = [line for line in region_lines[:NB_LINES_IN_HEADER] if line[0]]
                #look for title
                currentLine=0
                for i, line in enumerate(candidates_title):
                    if line[0] == "hline":
                        break
                    if (i==0 and np.isclose(line[1].tokens[0].x1, self.margin_right, 20)) or line[1].tokens[0].font['size']>= title_font_cut_off:
                        currentLine += 1
                        if self.number == 1:
                            self.document.title.append(line[1])
                        elif line[0] != "hline":
                            self.header.append(line[1])

                #look for paragraphs
                remaininglines=[l[1] for l in region_lines[currentLine:] if l[0] == "text"]
                if len (remaininglines):
                    virtical_lines = [l[1] for l in region_lines if l[0] == "vline"]
                    self.fill_paragraphs(extract(remaininglines, virtical_lines))
            else:
                remaininglines=[l[1] for l in region_lines if l[0]=="text"]
                virtical_lines=[l[1] for l in region_lines if l[0]=="vline"]
                self.fill_paragraphs(extract(remaininglines, virtical_lines))

    def fill_paragraphs(self, paragraphs):
        next_paragraph_tile = None
        last_line=None
        last_line_font_size=0
        for p in paragraphs:
            #try to combine small paragraphs
            if len(p) <= 2 and p[0].tokens[0].font_size == last_line_font_size:
                self.document.paragraphs.get_last_paragraph().pdflines.extend(p)
                continue
            # test if the first line is a title:
            paragraph = self.document.paragraphs.create_paragraph("paragraph")
            i=0
            if self.start_token is None:
                self.start_token=p[0]
            if last_line and p[0]==last_line:
                del(p[0])
            if next_paragraph_tile:
                paragraph.title = copy.copy(next_paragraph_tile)
                next_paragraph_tile = None

            elif len(p) > 2 and (p[0].tokens[0].font_size > p[1].tokens[0].font_size or p[0].tokens[0].font['bold']):
                paragraph.title = p[0]

                i=1
            last_line_font_size=100
            for l in p[i:-1]:
                paragraph.pdflines.append(l)
                last_line_font_size=l.tokens[0].font_size
            if p[-1].tokens[0].font_size > last_line_font_size:
                next_paragraph_tile = p[-1]
            else:
                paragraph.pdflines.append(p[-1])

        self.end_token=p[-1]

    def to_text(self):
        return '\n'.join([p.Text() + '\n' for p in self.paragraphs])

    @property
    def page_number(self):
        return self.number

    @property
    def tokens(self) -> "TokenList":
        """
        Returns an `ElementList` containing all elements on the page.

        Returns:
            ElementList: All the elements on the page.
        """
        return self.document.lines.between(
            self.start_token, self.end_token, inclusive=True
        )


    def __repr__(self):
        return f"<Page:{self.page_number}>"