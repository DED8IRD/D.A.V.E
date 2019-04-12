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
                if arg.find('PARENTHETICALS') > -1:
                    # join json
                    with open(arg) as f:
                        model = json.loads(f.read())
                    if self.model:
                        self.model += model
                    else:
                        self.model = model
                else:
                    # generate model
                    with open(arg) as f:
                        model = markovify.Text.from_json(f.read())

                    if self.model:
                        self.model = markovify.combine(models=[self.model, model])
                    else:
                        self.model = model
                
            # else:
            #     raise 


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
    def generate_models(source_dir, target_dir='.'):
        """
        Generates Markov models for each category and genre 
        and saves them as JSON
        """
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        for filename in os.listdir(source_dir):
            print(filename)
            path = os.path.join(source_dir, filename)
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
                    print(e.message)
                    pass
            export_path = os.path.join(target_dir, f'{filename}.json')
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(model)
