# Stanley.py
"""
Directs bot generated screenplays
"""

import json
import os
import time
from random import choice
from DAVE.nlp.HAL import HAL # markov model generator
from DAVE.nlp.Clark import Clark # text formatter

class Stanley:
    """
    Stanley generates tab formatted Markov chain generated screenplays
    """
    HEADINGS = 'HEADINGS'
    PARENTHETICALS = 'PARENTHETICALS'
    DIALOGUE = 'DIALOGUE'
    ACTIONS = 'ACTIONS'

    def __init__(self, genres, characters, 
                directory='.', title='Untitled', author='Anonymous'):
        """
        Initializes HAL objects by deserializing Markov models

        :genres: list : genre(s) for Markov models
        :characters: list : list of characters for screenplay 
        """
        start = time.time()
        genres = [genre.upper() for genre in genres]
        self.title = title
        self.author = author
        self.directory = directory
        self.headings = HAL(*self.__filenames(self.HEADINGS, genres))
        self.parentheticals = []
        self.dialogue = HAL(*self.__filenames(self.DIALOGUE, genres))
        self.actions = HAL(*self.__filenames(self.ACTIONS, genres))
        self.characters = [char.upper() for char in characters]
        self.transitions = [
            'CUT TO:', 'CONTINUED:', 'FADE TO BLACK:', 'FADE IN:', 'FADE OUT:', 
            'PAN IN:', 'PAN OUT:', 'DISSOLVE TO:', 'FLASH CUT:', 'SMASH CUT:', 
            'TIME CUT:', 'MATCH CUT:'
        ]
        self.__get_parentheticals(self.__filenames(self.PARENTHETICALS, genres))
        self.writer = Clark(title, author)
        print(f'Completed model rehydration in {time.time() - start} s.')

    def __filenames(self, category, genres):
        """
        returns list of filepaths from directory, category, and genres
        :category: str : name of category
        :genres: list : list of genres
        """
        return [os.path.join(self.directory, f'{category}_{genre}.json')
                for genre in genres]

    def __get_parentheticals(self, files):
        """
        loads parentheticals from json
        """
        for file in files:
            if type(file) is str and file.endswith('.json'):
                # join json
                with open(file) as f:
                    model = json.loads(f.read())
                self.parentheticals += model

    def generate(self, attr, max_length=None):
        """
        generates from markov model matching attr
        """
        model = getattr(self, attr)
        sentence = None
        while not sentence:
            sentence = model.generate_sentence(max_length)
        return sentence

    def generate_heading(self, max_length=45):
        """ generates heading """
        prefix = choice(['INT.', 'EXT.'])
        return prefix +' '+ self.generate('headings', max_length)

    def generate_parenthetical(self, max_length=45):
        """ generates parenthetical """
        return '(' +choice(self.parentheticals)+ ')'

    def generate_dialogue(self, max_length=500):
        """ generates dialogue """
        return self.generate('dialogue', max_length)

    def generate_action(self, max_length=250):
        """ generates action """
        return self.generate('actions', max_length)

    def generate_character(self):
        """ randomly selects character """
        return choice(self.characters)

    def generate_transition(self):
        """ randomly selects transition """
        return choice(self.transitions)

    def direct(self, length=100):
        """
        generate tab formatted screenplay
        """
        HEADING_MARGIN = (15, 10, 59, 'LEFT')
        CHARACTER_MARGIN = (42, 10, 33, 'LEFT')
        PARENTHETICAL_MARGIN = (36, 29, 20, 'LEFT')
        DIALOGUE_MARGIN = (29, 23, 33, 'LEFT')
        ACTION_MARGIN = (15, 10, 59, 'LEFT')
        TRANSITION_MARGIN = (59, 10, 15, 'RIGHT')

        def dialogue(amount):
            """
            generates dialogue between characters
            """
            characters = [self.generate_character() for _ in range(choice([1,2,3]))]
            prev_character = None
            for _ in range(amount):
                character = choice(characters)
                if character != prev_character:
                    self.writer.format(character, *CHARACTER_MARGIN)
                    self.writer.format(self.generate_parenthetical(), *PARENTHETICAL_MARGIN)
                    prev_character = character
                self.writer.format(self.generate_dialogue(), *DIALOGUE_MARGIN)                           

        for _ in range(length):
            self.writer.format(self.generate_transition(), *TRANSITION_MARGIN)
            self.writer.format(self.generate_heading(), *HEADING_MARGIN)
            self.writer.format(self.generate_action(), *ACTION_MARGIN)
            dialogue(choice([1,2,3,4]))

        self.writer.write(self.title, 'PLAINTEXT')
        self.writer.write(self.title, 'PDF')
