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
station = Base.classes.station

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
     
     session.close()

     # Create a dictionary from the row data and append to a list of all_percipitation
     all_percipitation = []
     for date, prcp in results:
         percipitation_dict = {}
         percipitation_dict["date"] = date
         percipitation_dict["prcp"] = prcp    
         all_percipitation.append(percipitation_dict)
         
     return jsonify(all_percipitation)

    #######################2nd Option##########################################################

    ##PROBLEM - CANNOT GET BOTH STATION AND NAME TO RETURN.  CODE DOES NOT LIKE STATION

@app.route("/api/v1.0/stations")
def stations():
    # Create a session to link from Python to the DB
    session = Session(engine)
    
    """Return a list of stations"""
    
    stations = session.query(measurement.station).distinct()
    
    session.close()

    # Create a dictionary from the station data and append to a list of all_stations
    all_stations = []
    for station in stations:
         station_dict = {}
         station_dict["station"] = station
         all_stations.append(station_dict)
    
    return jsonify(all_stations)

    #################OPTION 1 NOT WORKING################################################################
  
    #result2 = session.query(station.station, station.name).all()
    #result2 = session.query(station, station.station, station.name).all()
    
    # session.close()
    
    # # Create a dictionary from the station data and append to a list of all_stations
    # all_stations = []
    # for station, name in result2:
    #     station_dict = {}
    #     station_dict["station"] = station
    #     station_dict["name"] = name
    #     all_stations.append(station_dict)
    
    # return jsonify(all_stations)

#########################Option 3 Not Working###########################################################

# Define what to do when a user hits the /stations route

# SELECT
# measurement.station,
# station.name,
# FROM measurement
# INNER JOIN station ON
# measurement.station = station.station;

# @app.route("/api/v1.0/stations")
# def stations():
#     # Create a session to link from Python to the DB
#     session = Session(engine)
    
#     """Return a list of stations"""
   
#     stations = session.query(measurement.station, measurement.name).distinct()
#     session.close()

#     # Create a dictionary from the station data and append to a list of all_stations
#      all_stations = []
#     for station in stations:
#          station_dict = {}
#          station_dict["station"] = station
#          station_dict["name"] = name
#          all_stations.append(station_dict)
    
#     return jsonify(all_stations)

################################################################################################################ 
    
# Define what to do when a user hits the /temperature route
@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create a session to link from Python to the DB
    session = Session(engine)

    precipitation = [measurement.id,
    measurement.station,
    measurement.date,
    measurement.prcp,
    measurement.tobs]
                
    waihee = session.query(*precipitation).\
    filter(measurement.date > '2016-08-23').\
    filter(measurement.date < '2017-08-23').\
    filter(measurement.station == "USC00519281").all()

    session.close()

    # Create a dictionary from the annual temp data and append to temp list
    temp_list = []
    for temp in waihee:
        temperatures_dict = {}
        temperatures_dict["date"] = date
        temperatures_dict["tobs"] = tobs
        temp_list.append(temperatures_dict)
    
    return jsonify(temp_list)

############################HOW TO DO ALIGATOR CLIPS##############################

#api/v1.0/<start> and /api/v1.0/<start>/<end>

#Return a JSON list of the minimum temperature, the average temperature,and  the max temperature 
# for a given start or start-end range.

#When given the start only, calculate TMIN, TAVG, and TMAX, for all dates greater than and equal 
# to the start date.

#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the 
# start and end date inclusive.

  # Create a session to link from Python to the DB
     session = Session(engine)

     """Return a  list of the minimum temperature, the average temperature,.\
        and the max temperature for a given start or start-end range"""

    ##Query from database full temp results over a range of dates
    temp_results = session.query(measurement.date, measurement.tobs).all()
     
    temp_details = [measurement.date,
                    measurement.tobs]

    temp_range = session.query(*temp_details).\
                    filter(measurement.date >= '2016-08-23').\
                    filter(measurement.date <= '2017-08-23').all()
    session.close()
    
    ##Find the min, max, avg temperature in that date range
    temp_range_min = session.query(temp_range.tobs, func.min(temp_range.tobs)).first()

    temp_range_max = session.query(temp_range.tobs, func.max(temp_range.tobs)).first()

    temp_range_avg = session.query(temp_range.tobs, func.avg(temp_range.tobs)).first()

    return jsonify(temp_range_min)
    return jsonify(temp_range_max)
    return jsonify(temp_range_avg)

if __name__ == "__main__":
     app.run(debug=True)
