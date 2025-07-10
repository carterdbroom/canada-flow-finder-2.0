from flask import Flask, request, g
import sqlite3
import threading
import scraper
import os
import pandas as pd
import zipfile
from flask_sqlalchemy import SQLAlchemy
import datetime

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
TEMP_DIRECTORY = os.path.join(CURRENT_DIRECTORY, 'temp_dir')

app = Flask(__name__)
# Add the database to our app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.db'

# Initializing the database
db = SQLAlchemy(app)

# Database schemas
# This table will hold all of the latest station data that is found in the csv files 
class StationData(db.Model):
    station_id = db.Column(db.String(7), primary_key=True)
    station_name = db.Column(db.String(200), unique=True, nullable=False)
    province = db.Column(db.String(2), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    discharge_value = db.Column(db.Float)

# This table will hold the IDs of the stations that they have chosen as favourites
class Favourite(db.Model):
    station_id = db.Column(db.String(7), primary_key=True)

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