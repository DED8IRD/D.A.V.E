# HAL.py
"""
Generates sentences through Markov chains, using markovify
"""

import markovify
import json
import os


class HAL:
    """
    HAL represents a Markov model.
    """

    def __init__(self, *args):
        """
        Initializes HAL object by combining Markov models from args
        """
        self.model = None

        for arg in args:
            if type(arg) is str and arg.endswith('.json'):
                # generate model
                with open(arg) as f:
                    model = markovify.Text.from_json(f.read())

                if self.model:
                    self.model = markovify.combine(models=[self.model, model])
                else:
                    self.model = model
            

    def generate_sentence(self, max_length=None):
        """
        Generates sentence given a category

        :max_length: int or None : max_length for sentence
        :return: str : markovify generated sentence
        """
        if max_length:
            return self.model.make_short_sentence(max_length)
        return self.model.make_sentence()


    @staticmethod
    def generate_models(source, destination='.'):
        """
        Generates Markov models for each category and saves them as JSON
        """
        if not os.path.exists(destination):
            os.makedirs(destination)

        for filename in os.listdir(source):
            path = os.path.join(source, filename)
            with open(path, encoding='utf-8') as f:
                corpus = f.read()
            if filename.startswith('PAREN'):
                # store parentheticals as list
                model = json.dumps(corpus.split('\n'))
            else:
                # create markov model from file
                try:
                    model = markovify.Text(corpus, retain_original=False).to_json()
                except Exception as e:
                    pass
            export_path = os.path.join(destination, f'{filename}.json')
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(model)
