# Clark.py
"""
Generates tab formatted screenplays
"""

class Clark:
    LEFT_MARGIN = 15
    RIGHT_MARGIN = 10
    MAX_WIDTH = 59
    MAX_LENGTH = 55

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.pages = []
        self.current_page = ''
        self.line_count = 0

    def format_margins(self, text, 
                       left=self.LEFT_MARGIN, 
                       right=self.RIGHT_MARGIN, 
                       max_width=self.MAX_WIDTH, 
                       align='LEFT', pagewidth=79):
        """
        returns space padded lines
        """
        tokens = text.split()
        remaining_tokens = len(tokens)
        remaining_width = max_width
        lines = []
        current_line = ''

        for token in tokens:
            token_length = len(token)
            if remaining_width - token_length > 0:
                current_line += token
                remaining_width -= token_length
            else:
                current_line = 
                '\n' + token 
                remaining_width = max_width - token_length
                line_count += 1
