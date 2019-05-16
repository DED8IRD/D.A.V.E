# Clark.py
"""
Generates formatted screenplays
"""
from fpdf import FPDF

class PDF(FPDF):
    """
    PDF writer class with page number in top right margin
    """
    def footer(self):
        # ignore title page
        if self.page_no() > 1:
            # position at 0.5in from top
            self.set_y(0.5)
            # page number
            self.cell(0, 0.5, str(self.page_no() - 1), 0, 0, 'R')


class Clark:
    """
    Clark generates whitespace formatted screenplays as plaintext files
    """
    LEFT_MARGIN = 15
    RIGHT_MARGIN = 10
    MAX_WIDTH = 59
    MAX_LENGTH = 55
    PAGE_WIDTH = 79

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.lines = []

        left_padding = self.MAX_WIDTH + self.LEFT_MARGIN 
        title_margin = (left_padding - len(self.title)) // 2
        screenplay_margin = (left_padding - len('Screenplay')) // 2
        author_margin = (left_padding - len(self.author)) // 2

        self.title_page = '\n\n'.join(['\n\n',
                         (' '*title_margin + self.title),
                         (' '*screenplay_margin + 'Screenplay'),
                         (' '*((left_padding - 2) // 2) + 'By'),
                         (' '*author_margin + self.author + '\n'*8)
                         ])

    def __format_line(self, line, align, left, right, page_width):
        """
        formats line to page

        """
        if align == 'LEFT':
            line = ' '*left + line
        else:
            left_pad = page_width - right - len(line)
            line = ' '*left_pad + line
        self.lines.append(line + '\n')

    def format(self, text, left=LEFT_MARGIN, right=RIGHT_MARGIN, 
               max_width=MAX_WIDTH, align='LEFT', page_width=PAGE_WIDTH):
        """
        returns space padded lines
        """
        tokens = text.split()
        remaining_tokens = len(tokens)
        remaining_width = max_width
        current_line = ''

        for token in tokens:
            token_length = len(token)

            if remaining_width - token_length > 0:
                current_line += token + ' '
                remaining_width -= token_length + 1
            else:
                self.__format_line(current_line, align, left, right, page_width)
                current_line = token + ' '
                remaining_width = max_width - len(current_line)

        self.__format_line(current_line, align, left, right, page_width)
        self.lines.append('\n')

    def __write_plaintext(self, path):
        """
        writes screenplay as plaintext file
        """
        pages = self.title_page

        for i in range(0, len(self.lines), self.MAX_LENGTH):
            page = ''.join(self.lines[i:i+self.MAX_LENGTH])
            page_number = '\n'*2 + ' '*(self.PAGE_WIDTH - self.LEFT_MARGIN) + \
                          str(i // self.MAX_LENGTH + 1) + '\n'*2
            pages += page_number + page + '\n' * 4

        with open(path + '.txt', 'w', encoding='utf-8') as f:
            f.write(pages)
            
    def __write_pdf(self, path):
        """
        writes screenplay as pdf
        """
        pdf = PDF(orientation='P', unit='in', format='Letter')
        pdf.set_font(family='Courier', size=12)
        pdf.set_margins(left=0, top=1, right=0.5)
        pdf.alias_nb_pages()
        pdf.set_auto_page_break(auto=True, margin=1)

        # tile page
        pdf.add_page()
        title_page = '\n'*4 + '\n'.join(self.title_page.split())
        pdf.multi_cell(0, 0.5, title_page, 0, 'C')
        pdf.add_page()

        for line in self.lines:
            pdf.multi_cell(0, 0.1, line, 0, 'L')
            pdf.ln()

        pdf.output(path + '.pdf', 'F')

    def write(self, path, filetype):
        """
        writes screenplay to filetype at filepath
        """
        if filetype == 'PLAINTEXT':
            self.__write_plaintext(path)
        elif filetype == 'PDF':
            self.__write_pdf(path)
