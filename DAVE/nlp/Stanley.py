# Stanley.py
"""
Directs bot generated screenplays
"""

import json
import os
import time
from random import choice
from DAVE.scraper import Sentinel # parser
from DAVE.nlp.HAL import HAL # markov model generator
from DAVE.nlp.Clark import Clark # text formatter

def get_or_create_dir(*args):
    """
    creates directory if it does not exist
    """
    path = os.path.join(*args)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


class Stanley:
    """
    Stanley generates tab formatted Markov chain generated screenplays
    """
    HEADINGS = 'HEADINGS'
    PARENTHETICALS = 'PARENTHETICALS'
    DIALOGUE = 'DIALOGUE'
    ACTIONS = 'ACTIONS'

    def __init__(self, sources, characters, target='.', 
                title='Untitled', author='Anonymous'):
        """
        Parses source screenplays
        Generates Markov models
        Initializes HAL objects by deserializing models

        :sources: list : directory(s) for Markov models
        :characters: list : list of characters for screenplay 
        """
        self.title = title
        self.author = author
        self.target = target
        
        start = time.time()
        parsed = get_or_create_dir(target, 'parsed')
        Sentinel.parse(*sources, destination=parsed, write=True)
        print(f'Parsing screenplays in {time.time() - start} s.')

        start = time.time()
        models = get_or_create_dir(target, 'models')
        HAL.generate_models(parsed, models)
        print(f'Generating Markov models in {time.time() - start} s.')

        start = time.time()
        self.headings = HAL(os.path.join(models, self.HEADINGS + '.json'))
        self.parentheticals = []
        self.dialogue = HAL(os.path.join(models, self.DIALOGUE + '.json'))
        self.actions = HAL(os.path.join(models, self.ACTIONS + '.json'))
        self.characters = [char.upper() for char in characters]
        self.transitions = [
            'CUT TO:', 'CONTINUED:', 'FADE TO BLACK:', 'FADE IN:', 'FADE OUT:', 
            'PAN IN:', 'PAN OUT:', 'DISSOLVE TO:', 'FLASH CUT:', 'SMASH CUT:', 
            'TIME CUT:', 'MATCH CUT:'
        ]
        self.__get_parentheticals(os.path.join(models, self.PARENTHETICALS + '.json'))
        self.writer = Clark(title, author)
        print(f'Completed model rehydration in {time.time() - start} s.')

    def __filenames(self, category, directory):
        """
        returns list of filepaths from directory, category, and source
        :category: str : name of category
        :directory: list : list of sources
        """
        return [os.path.join(directory, f'{category}_{source}.json')
                for source in directory]

    def __get_parentheticals(self, file):
        """
        loads parentheticals from json
        """
        # for file in files:
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

        path = os.path.join(self.target, self.title)
        self.writer.write(path, 'PLAINTEXT')
        self.writer.write(path, 'PDF')