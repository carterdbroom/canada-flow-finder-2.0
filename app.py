from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p> Hello, World!</p>"

# /
# /search
# /favourites

@app.route('/favourites', methods = ['POST'])
def add_favourite():
    return

