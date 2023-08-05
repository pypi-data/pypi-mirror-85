import logging
from collections import namedtuple
import statistics
import matplotlib.pyplot as plt
from matplotlib import patches
from collections import Counter
from pdf2txt.core import TextEdges
from pdf2txt.utils import get_page_parameters, are_in_same_Line, get_fonts
from pdf2txt.utils import get_text_objects, get_graphical_object
from pdf2txt.utils import is_rotated
from pdf2txt.utils import isRectangleOverlap
from pdf2txt.utils import get_fonts_statistics, has_ovelaping_rectangle, segement_overlap
logger = logging.getLogger("camelot")

class Span():
    def __init__(self, textline):
        self.text = textline.get_text().strip()
        self.font = get_fonts(textline)
        self.x0, self.x1, self.y0, self.y1=textline.x0, textline.x1, textline.y0, textline.y1


        self.textlines=[textline]
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Span):
            return self.text == other.text and self.x0==other.x0 and self.y1==other.y1
        return False

    def __repr__(self):
        return '<'+self.text+'>'

    def add(self, other, separator='\n'):
        self.text += separator + other.Text
        self.y0 = min(other.y0, self.y0)
        self.x0 = min(other.x0, self.x0)
        self.y1=max(other.y1, self.y1)
        self.x1 = max(other.x1, self.x1)
        self.textlines.extend(other.textlines)
        return self



class Line():
    def __init__(self):
        self.spans=[]

class PageLayout():

    def __init__(
        self,
            page_number,
        edge_tol=50
    ):

        self.edge_tol = edge_tol
        self.page_number=page_number
        self.page_regions=None
        self.font_statistics=None



    def _set_page_layout(self, page_layout):

        self.layout =page_layout
        self.pdf_width, self.pdf_height, self.margin_left, self.margin_right, self.margin_bottom, self.margin_top=get_page_parameters(page_layout)
#        self.images = get_text_objects(self.layout, ltype="image")
        self.text_boxes=get_text_objects(self.layout, ltype="text_box")
        self.horizontal_text = get_text_objects(self.layout, ltype="horizontal_text")
        self.vertical_text = get_text_objects(self.layout, ltype="vertical_text")
        self.lines=get_graphical_object(self.layout)


    def _page_detection_algorithm2(self, textlines):

        textedges = TextEdges( edge_tol=2*self.edge_tol)
        textedges.page_width=self.margin_right-self.margin_left
        textedges.page_height=self.pdf_height
        textedges.left_margin=self.margin_left

        # generate left, middle and right textedges
        textedges.generate2(textlines)
        # guess vertical areas that are in the midle of a multi-column page
        vertical_bbox = textedges.get_column_separators(textlines, self.lines, textedges.left())
        table_areas=[]

        Area = namedtuple('Area', ['x0', 'y0', 'x1', 'y1'])

        if len(vertical_bbox)==0:
            table_areas.append(Area(0, 0, self.pdf_width, self.pdf_height))
            return table_areas
        else:
            table_areas=self.get_areas_from_separators(vertical_bbox)

        if not len(table_areas):
            table_areas.append((0, 0, self.pdf_width, self.pdf_height))
        return table_areas


    def get_areas_from_separators(self, separators):
        table_areas = []

        Area = namedtuple('Area', ['x0', 'y0', 'x1', 'y1'])

        # sort vertical lines by desending order of top edge (this allow to form the top area
        separators.sort(key=lambda te: -te.y1)
#        self.plot_page(separators)
        left = self.margin_left
        top = self.margin_top
        right = self.margin_right

        # detect top page area
        last_separator=separators[0]
        for separaor in separators:
            bottom = separaor.y1
            if last_separator.y0 > bottom:
                top = last_separator.y0
            if last_separator.y1 > separaor.y1 > last_separator.y0:
                if last_separator.x0 < separaor.x0:
                    left=last_separator.x0
                else:
                    right=last_separator.x0
            #top area
            top_area=Area(left, bottom, right, top)
            if not has_ovelaping_rectangle(top_area, table_areas):
                table_areas.append(top_area)
    #        self.plot_page(table_areas)
            #left area
            top=bottom
            right=separaor.x0
            sep_to_left=self.get_left_separator(separators, separaor)
            if sep_to_left:

                bottom=sep_to_left.y0 if sep_to_left.y0> separaor.y0 else separaor.y0
                left=sep_to_left.x0

                table_areas.append(Area(left, bottom, right, top))
    #            self.plot_page(table_areas)
            else:
                bottom=separaor.y0
                table_areas.append(Area(left, bottom, right, top))
    #            self.plot_page(table_areas)
            # right area
            left=separaor.x0
            right=self.margin_right
            sep_to_right=self.get_right_separator(separators, separaor)
            if sep_to_right:
                bottom=sep_to_right.y1
                table_areas.append(Area(left, bottom, right, top))
    #            self.plot_page(table_areas)
                if sep_to_right.y0>separaor.y0:
                    top=sep_to_right.y0
                    bottom=separaor.y0
                    table_areas.append(Area(left, bottom, right, top))
    #                self.plot_page(table_areas)
            else:
                right=self.margin_right
                table_areas.append(Area(left, bottom, right, top))
    #            self.plot_page(table_areas)

            top=separaor.y1
            last_separator=separaor
            left=self.margin_left

        #add area at the bottom. Should be last remaining
        separators.sort(key=lambda te: te.y0)

        top=separators[0].y0
        bottom=self.margin_bottom
        left=self.margin_left
        right=self.margin_right
        table_areas.append(Area(left, bottom, right, top))
    #    self.plot_page(table_areas)

        return table_areas

    def get_left_separator(self, sparators, separator):
        #separators are sorted acording to  decreasing y0
        for s in sparators:
            if s.x0 < separator.x0 and segement_overlap(s.x0, s.y1, separator.x0, separator.x1):
                return s
        return None

    def get_right_separator(self, sparators, separator):
        #separators are sorted acording to  decreasing y0
        for s in sparators:
            if s.x0 > separator.x0 and segement_overlap(s.x0, s.y1, separator.x0, separator.x1):
                return s
        return None

    def _find_line_structure(self, textlines):
        textlines.sort(key=lambda x: (-x.y1, x.x0))
        lines=[]
        i=0
        while i < len(textlines)-1:



            text=textlines[i].get_text().strip()
            if len(text)<=1 and not text.isupper():
                i+=1
                continue

            text = Span(textlines[i])
            if text.font['visible']==False:
                i+=1
                continue

            next_text = Span(textlines[i+1])
            while  not next_text.font['visible'] and i < len(textlines)-2:
                i+=1
                next_text = Span(textlines[i + 1])

            line=Line()
            line.spans.append(text)
            while are_in_same_Line(text, next_text) and i<len(textlines)-2:
                if len(next_text.text.strip()) <= 1 and not next_text.text.strip().isupper():
                    i += 1
                    next_text = Span(textlines[i + 1])

                    continue
                separation = abs(text.x1 - next_text.x0)
                if separation <= 1.5 * text.font['width'] and text.font==next_text.font:
                    text.add(next_text, separator=' ')
                else:
                    line.spans.append(next_text)
                i += 1
#                text = Span(textlines[i])
                next_text = Span(textlines[i+1])

                continue

            line.spans.sort(key=lambda x: x.x0, reverse=False)
            lines.append(line)

            i+=1
        #handle the last line
        if i==len(textlines)-1 and next_text not in lines[-1].spans:
            line=Line()
            line.spans.append(next_text)
            lines.append(line)
        self.font_statistics=get_fonts_statistics(lines)
        return lines


    def draw_rect_bbox(self, x0, y0, x1, y1, ax, color):
        """
        Draws an unfilled rectable onto ax.
        """
        ax.add_patch(
            patches.Rectangle(
                (x0, y0),
                x1 - x0,
                y1 - y0,
                fill=False,
                color=color
            )
        )


    def draw_rect(self, rect, ax, color="black"):
        self.draw_rect_bbox(rect[0],rect[1],rect[2],rect[3], ax, color)

    def plot_page(self, rects):


        xmin, ymin, xmax, ymax = self.margin_left, self.margin_bottom, self.margin_right, self.margin_top
        size = 6

        fig, ax = plt.subplots(figsize=(size, size * (ymax / xmax)))

        for rect in rects:
            self.draw_rect(rect, ax)

        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        plt.show()


    def extract_regions(self):

        self.textedges = []
        hor_text = self.horizontal_text
        self.horizontal_lines_text = self._find_line_structure(hor_text)

        # find tables based on nurminen's detection algorithm
        self.page_regions = self._page_detection_algorithm2(self.horizontal_lines_text)

        self.plot_page(self.page_regions)

        return self.page_regions

    def get_region_lines(self, region):
        region_lines=[]
        for line in self.horizontal_lines_text:
            lines = []
            for span in line.spans:
                if isRectangleOverlap(span, region):
                    lines.append(span)
            if len(lines)>0:
                region_lines.append(lines)

        return region_lines

    def parse_region(self, region_lines, region_number):

        print('page---------', self.page_number)
        document_title=[]
        for i, line in enumerate(region_lines):
            if self.page_number==1 and region_number==0 and i<3:
                if len(line)==1 and line[0].font['size']==self.font_statistics['largest_size']:
                    document_title.append(line[0].Text)
                    print('Document Title: ' + line[0].Text)
            elif region_number==0 and i <3:
                if line[0].font['size'] ==self.font_statistics['largest_size']:
                    print('Page Title: ' + line[0].Text)

    def get_text_from_region(self, region):
        texts=[]

        for line in self.horizontal_lines_text:
            text_span=[]
            text = ""
            for span in line.spans:
                if isRectangleOverlap(span, region):
                    text_span.append(span.Text)
            if len(text_span):
                text='\t'.join(text_span)

            if text !="":
                texts.append(text)

        return '\n'.join(texts)
    def extract_texts(self):
        self.page_regions.sort(key=lambda te: (-te.y1, te.x0))
        if not self.page_regions:
            self.page_regions=self.extract_regions()
        texts=[]
        for i, region in enumerate(self.page_regions):
            region_lines=self.get_region_lines(region)
            self.parse_region(region_lines, i)
            texts.append(self.get_text_from_region(region))

        return '\n'.join(texts)


    def extract_simple(self):
        self.horizontal_lines_text = self._find_line_structure(self.horizontal_text)
        texts=[]
        for line in self.horizontal_lines_text:
            text='\t'.join([t.Text for t in line.spans])
            texts.append(text)

        return '\n'.join(texts)