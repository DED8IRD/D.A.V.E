# HAL.py
"""
Generates tab formatted screenplay using Markov chains
"""
import markovify
import os

def generate_models(source_dir, target_dir='.'):
    """
    Generates markov models for each category and genre 
    and savese them as JSON
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in os.listdir(source_dir):
        print(filename)
        path = os.path.join(source_dir, filename)
        with open(path, encoding='utf-8') as f:
            corpus = f.read()
        # create markov model from file
        model = markovify.Text(corpus, retain_original=False).to_json()
        export_path = os.path.join(target_dir, f'{filename}.json')
        with open(export_path, 'w', encoding='utf-8') as f:
            f.write(model)


def screenwrite(source):
    pass


if __name__ == '__main__':
    source = os.path.join('..','scraper', 'parsed_categories')
    destination = 'markov_models'
    generate_models(source, destination)