# app.py
"""
Server side logic for D.A.V.E, the screenplay generating bot
Written in Flask
"""
import os
from flask import Flask, request, send_from_directory
from DAVE.nlp.Stanley import Stanley as Director

app = Flask(__name__, 
    static_folder='client/public/',
    template_folder='client/static/'
)

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


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != '' and os.path.exists(app.static_folder + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True, debug=True)