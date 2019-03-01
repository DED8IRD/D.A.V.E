# Stanley.py
"""
Generates tab formatted bot generated screenplays
"""
import os

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
