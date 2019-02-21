# DAVE.py
"""
Server side logic for D.A.V.E, the screenplay generating bot
Written in Flask
"""
from flask import Flask, request
# url_for, redirect


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
    pass