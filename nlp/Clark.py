# Clark.py
"""
Generates formatted screenplays
"""

class Clark:
    """
    Clark generates whitespace formatted screenplays as plaintext files
    """
    LEFT_MARGIN = 15
    RIGHT_MARGIN = 10
    MAX_WIDTH = 59
    MAX_LENGTH = 55

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.pages = []
        self.current_page = []
        self.line_count = 0


        title_margin = (self.MAX_WIDTH - len(self.title)) // 2
        screenplay_margin = (self.MAX_WIDTH - len('Screenplay')) // 2
        author_margin = (self.MAX_WIDTH - len(self.author)) // 2

        title_page = '\n\n'.join(['\n\n',
                         (' '*title_margin + self.title),
                         (' '*screenplay_margin + 'Screenplay'),
                         (' '*((self.MAX_WIDTH - 2) // 2) + 'By'),
                         (' '*author_margin + self.author + '\n'*8)
                     ])

        self.pages.append(title_page) 

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
               max_width=MAX_WIDTH, align='LEFT', page_width=79):
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
                    self.current_page = [' '*(self.MAX_WIDTH - 5) + str(len(self.pages))]
        self.__format_line(current_line, align, left, right, page_width)
        self.current_page.append('\n')

    def write(self, path):
        """
        writes screenplay to filepath
        """
        self.pages.append('\n'.join(self.current_page))
        pages = '\n'.join(self.pages)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(pages)
            