#############################################################################
# Import Flask and other dependencies
#############################################################################
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

##############################################################################
# Database Setup
##############################################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save reference to the table
measurement = Base.classes.measurement
Station = Base.classes.station

##############################################################################
# Flask Setup
##############################################################################

app = Flask(__name__)

##############################################################################
# Flask Routes
##############################################################################

# Define what to do when a user hits the index route
@app.route("/")
def home():
     return (
         f"Welcome to my 'Hawaii API!<br/>"
         f"Available Routes:<br/>"
         f"/api/v1.0/precipitation<br/>"
         f"/api/v1.0/stations<br/>"
         f"/api/v1.0/tobs<br/>"
         f"/api/v1.0/<start><br/>"
         f"/api/v1.0/<start>/<end>"
     )

# Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():

     # Create a session to link from Python to the DB
     session = Session(engine)

     """Return a list of all percipitation data from reporting stations"""

     results = session.query(measurement.date, measurement.prcp).all()

     # Create a dictionary from the row data and append to a list of all_percipitation
     all_percipitation = []
     for date, prcp in results:
         percipitation_dict = {}
         percipitation_dict["date"] = date
         percipitation_dict["prcp"] = prcp    
         all_percipitation.append(percipitation_dict)
         
     return jsonify(all_percipitation)

##################################################################################################
@app.route("/api/v1.0/stations")
def stations():
    # Create a session to link from Python to the DB
    session = Session(engine)
    
    """Return a list of stations"""
    
    stations = session.query(measurement.station, Station.name).distinct()
    
    # Create a dictionary from the station data and append to a list of all_stations
    all_stations = []
    for station in stations:
         station_dict = {}
         station_dict["station"] = station
         all_stations.append(station_dict)
    
    return jsonify(all_stations)

#################################################################################################### 
# Define what to do when a user hits the /temperature route
@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create a session to link from Python to the DB
    session = Session(engine)

    """Return a tempatures listed for most active data recording station USC00519281"""

    temp_active = session.query(measurement.station, measurement.date, measurement.tobs).\
    filter(measurement.date > '2016-08-23').\
    filter(measurement.date < '2017-08-23').\
    filter(measurement.station == "USC00519281").all()
        
    temp_list = []
    for tobs in temp_active:
         temperatures_dict = {}
         temperatures_dict["tobs"] = tobs
         temp_list.append(temperatures_dict)
    
    return jsonify(temp_list)

############################HOW TO DO ALIGATOR CLIPS##################################################

@app.route("/api/v1.0/<start>")
def temperature_s(start):

     """Return a  list of min_temp, avg_temp, & max_temp for a given start range"""
     
     # Create a session to link from Python to the DB
     session = Session(engine)
     
     # Set start and end dates for date range
     start_date = '2016-08-23'
     
     # Query from database full temp results for dates greater than or equal to start_date
     temp_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
     filter(measurement.date >= start_date).all()

     start_temp = []
     for tobs in temp_results:
         start_dict = {}
         start_dict["tobs"] = tobs
         start_temp.append(start_dict)

     return jsonify(start_temp)

#################################################################################################
@app.route("/api/v1.0/<start>/<end>")
def temperature(start, end):

     """Return a  list of min_temp, avg_temp, & max_temp for a given start-end range"""
    
     # Create a session to link from Python to the DB
     session = Session(engine)
    
     #Set start and end dates for date range
     start_date = '2016-08-23'
     end_date = '2017-08-23'

     # Query from database full temp results for dates greater than or equal to start_date
     start_end_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
     filter(measurement.date >= start_date).\
     filter(measurement.date <=end_date).all

     session.close()

     start_end_list = []
     for tobs in start_end_results:
         start_end_dict = {}
         start_end_dict["tobs"] = tobs
         start_end_list.append(start_end_dict)

     return jsonify(start_end_list)     

if __name__ == "__main__":
     app.run(debug=True)
