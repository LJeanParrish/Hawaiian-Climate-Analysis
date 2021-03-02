# Import Flask and other dependencies
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station= Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#Percipitation Dictionary
percipitation_recordings = [







]

#################################################
# Flask Routes
#################################################

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
        f"Welcome to my 'Hawaii API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

# 4. Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    return "Welcome to my Precipitation page!"

# 5. Define what to do when a user hits the /stations route
@app.route("/api/v1.0/stations")
def stations():
     return "Welcome to my Stations page!"

# 6. Define what to do when a user hits the /temperature route
@app.route("/api/v1.0/tobs")
def tobs():
     return "Welcome to my Temperature page!"


if __name__ == "__main__":
    app.run(debug=True)# 3. Define what to do when a user hits the index route
