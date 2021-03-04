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
         f"/api/v1.0/tobs"
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
    # Set start and end dates for date range
    start_date = '2016-08-23'
    end_date = '2017-08-23'
    
    """Return a  list of min_temp, avg_temp, & max_temp for a given start or start-end range"""

    ##Query from database full temp results over a range of dates
    temp_results = session.query(measurement.date, measurement.tobs).all()
     
    temp_details = [measurement.date,measurement.tobs]

    temp_range = session.query(*temp_details).\
                    filter(measurement.date >= '2016-08-23').\
                    filter(measurement.date <= '2017-08-23').all()
        
    ##Find the min, max, avg temperature in that date range
    temp_range_min = session.query(temp_range.tobs, func.min(temp_range.tobs)).first()

    temp_range_max = session.query(temp_range.tobs, func.max(temp_range.tobs)).first()

    temp_range_avg = session.query(temp_range.tobs, func.avg(temp_range.tobs)).first()

    return jsonify(temp_range_min)
    return jsonify(temp_range_max)
    return jsonify(temp_range_avg)

@app.route("/api/v1.0/<start>/<end>")
def temperature(start, end):
    start_date = '2016-08-23'
    end_date = '2017-08-23'
    
    def calc_temps(start_date, end_date):
        
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        
        trip_temps = calc_temps(start_date, end_date)
        
        return jsonify(trip_temps)
        
        session.close()

if __name__ == "__main__":
     app.run(debug=True)
