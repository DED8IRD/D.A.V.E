# Clark.py
"""
Generates formatted screenplays
"""
from fpdf import FPDF

class Clark:
    """
    Clark generates whitespace formatted screenplays as plaintext files
    """
    LEFT_MARGIN = 15
    RIGHT_MARGIN = 10
    MAX_WIDTH = 59
    MAX_LENGTH = 55 // 2
    PAGE_WIDTH = 79

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.pages = []
        self.current_page = []
        self.line_count = 0

        left_padding = self.MAX_WIDTH + self.LEFT_MARGIN 
        title_margin = (left_padding - len(self.title)) // 2
        screenplay_margin = (left_padding - len('Screenplay')) // 2
        author_margin = (left_padding - len(self.author)) // 2

        title_page = '\n\n'.join(['\n\n',
                         (' '*title_margin + self.title),
                         (' '*screenplay_margin + 'Screenplay'),
                         (' '*((left_padding - 2) // 2) + 'By'),
                         (' '*author_margin + self.author + '\n'*8)
                     ])

        self.pages.append(title_page) 
        self.line_count += 1

    def __format_line(self, line, align, left, right, page_width):
        """
        formats line to page

        """
        if align == 'LEFT':
            line = ' '*left + line
        else:
            left_pad = page_width - right - len(line)
            line = ' '*left_pad + line
        self.current_page.append(line)
        self.line_count += 1            

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

                # create new page
                if self.line_count % self.MAX_LENGTH == 0:
                    self.pages.append('\n'.join(self.current_page))
                    self.current_page = []

        self.__format_line(current_line, align, left, right, page_width)

    def __write_plaintext(self, path):
        """
        writes screenplay as plaintext file
        """
        pages = ''
        for i in range(len(self.pages)):
            page_number = '\n'*2 + ' '*(self.PAGE_WIDTH - 15) + str(i) + '\n'*2
            pages += page_number + self.pages[i] + '\n'

        with open(path + '.txt', 'w', encoding='utf-8') as f:
            f.write(pages)
            
    def __write_pdf(self, path):
        """
        writes screenplay as pdf
        """
        pdf = FPDF()
        pdf.set_font('Courier', '', 12)
        for page in self.pages:
            page = page.split('\n')
            pdf.add_page()
            for line in page:
                pdf.multi_cell(0, 4, line, 0, 'L')
                pdf.ln()
        pdf.output(path + '.pdf', 'F')

    def write(self, path, filetype):
        """
        writes screenplay to filetype at filepath
        """
        self.pages.append('\n'.join(self.current_page))

        if filetype == 'PLAINTEXT':
            self.__write_plaintext(path)
        elif filetype == 'PDF':
            self.__write_pdf(path)
