from flask import Flask, request, g
import sqlite3
import threading
import scraper
import os
import pandas as pd
import zipfile

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
TEMP_DIRECTORY = os.path.join(CURRENT_DIRECTORY, 'temp_dir')

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

#def update_station_data():
 #   for file in os.listdir(TEMP_DIRECTORY): 
  #      zf = zipfile.ZipFile(file)
   #     df = pd.read_csv(zf.open())


if __name__ == "__main__":
    t = threading.Thread(target=scraper.scraper)
    t.daemon = True
    t.start()

    app.run(debut=True)