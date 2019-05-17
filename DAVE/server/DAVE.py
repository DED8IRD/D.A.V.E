# DAVE.py
"""
Server side logic for D.A.V.E, the screenplay generating bot
Written in Flask
"""
from flask import Flask, request
from nlp.Stanley import Stanley as Director


app = Flask(__name__)


@app.route('/')
def index():
    print(request)
    print(request.method)
    print(request.args)
    print(request.cookies)
    return 'Hello, World!'


@app.route('/screenwrite/', methods=['GET', 'POST'])
def screenwrite():
    genres = ['western']
    characters = ['bob', 'bobby', 'bobra', 'bobert']
    source = '../nlp/markov_models'    
    director = Director(genres, characters, source)
    director.direct()
    pass


@app.route('/download/<path:filename>')
def download(filename):
    try:
        return send_from_directory(
            os.path.join(app.instance_path, ''),
            filename
        )
    except Exception as e:
        return e.message