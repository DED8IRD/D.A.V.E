# Stanley.py
"""
Generates tab formatted bot generated screenplays
"""
import os
from random import choice
from HAL import HAL

class Stanley:
    """
    Stanley generates tab formatted Markov chain generated screenplays
    """
    HEADINGS = 'HEADINGS'
    PARENTHETICALS = 'PARENTHETICALS'
    DIALOGUE = 'DIALOGUE'
    ACTIONS = 'ACTIONS'

    def __init__(self, genres, characters, directory='.'):
        """
        Initializes HAL objects by deserializing Markov models

        :genres: list : genre(s) for Markov models
        :characters: list : list of characters for screenplay 
        """
        self.directory = directory
        self.headings = HAL(*self.__filenames(self.HEADINGS, genres))
        self.parentheticals = HAL(*self.__filenames(self.PARENTHETICALS, genres))
        self.dialogue = HAL(*self.__filenames(self.DIALOGUE, genres))
        self.action = HAL(*self.__filenames(self.ACTIONS, genres))
        self.characters = [char.upper() for char in characters]
        self.transitions = [
            'CUT TO:', 'CONTINUED:', 'FADE TO BLACK:', 'FADE IN:', 'FADE OUT:', 
            'PAN IN:', 'PAN OUT:', 'DISSOLVE TO:', 'FLASH CUT:', 'SMASH CUT:', 
            'TIME CUT:', 'MATCH CUT:'
        ]

    def __filenames(self, category, genres):
        """
        returns list of filepaths from directory, category, and genres
        :category: str : name of category
        :genres: list : list of genres
        """
        return [os.path.join(self.directory, f'{category}_{genre}.json')
                for genre in genres]

    def generate(self, attr, max_length):
        """
        generates from markov model matching attr
        """
        model = getattr(self, attr)
        sentence = None
        count = 0
        while not sentence:
            sentence = model.generate_sentence(max_length)
            count += 1
            print(count)
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
        return '(' +self.generate('parentheticals', max_length) + ')'

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
