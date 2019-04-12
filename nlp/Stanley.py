# Stanley.py

import os
from random import choice
from HAL import HAL
from Clark import Clark

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
        genres = [genre.upper() for genre in genres]
        self.title = title
        self.author = author
        self.directory = directory
        self.headings = HAL(*self.__filenames(self.HEADINGS, genres))
        self.parentheticals = HAL(*self.__filenames(self.PARENTHETICALS, genres))
        self.dialogue = HAL(*self.__filenames(self.DIALOGUE, genres))
        self.actions = HAL(*self.__filenames(self.ACTIONS, genres))
        self.characters = [char.upper() for char in characters]
        self.transitions = [
            'CUT TO:', 'CONTINUED:', 'FADE TO BLACK:', 'FADE IN:', 'FADE OUT:', 
            'PAN IN:', 'PAN OUT:', 'DISSOLVE TO:', 'FLASH CUT:', 'SMASH CUT:', 
            'TIME CUT:', 'MATCH CUT:'
        ]
        self.writer = Clark()

    def __filenames(self, category, genres):
        """
        returns list of filepaths from directory, category, and genres
        :category: str : name of category
        :genres: list : list of genres
        """
        return [os.path.join(self.directory, f'{category}_{genre}.json')
                for genre in genres]

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
        """
        generates heading
        """
        prefix = choice(['INT.', 'EXT.'])
        return prefix +' '+ self.generate('headings', max_length)

    def generate_parenthetical(self, max_length=45):
        """
        generates parenthetical
        """
        return '(' +choice(self.parentheticals)+ ')'

    def generate_dialogue(self, max_length=500):
        """
        generates dialogue
        """
        return self.generate('dialogue', max_length)

    def generate_action(self, max_length=250):
        """
        generates action
        """
        return self.generate('actions', max_length)

    def generate_character(self):
        """
        randomly selects character
        """
        return choice(self.characters)

    def generate_transition(self):
        """
        randomly selects transition
        """
        return choice(self.transitions)

    def direct(self):
        """
        generate tab formatted screenplay
        """
        HEADINGS_MARGIN = (15, 10, 59, 'LEFT')
        CHARACTER_MARGIN = (42, 10, 33, 'LEFT')
        PARENTHETICAL_MARGIN = (36, 29, 20, 'LEFT')
        DIALOGUE_MARGIN = (29, 23, 33, 'LEFT')
        ACTION_MARGIN = (15, 10, 59, 'LEFT')
        TRANSITION_MARGIN = (59, 10, 15, 'RIGHT')
