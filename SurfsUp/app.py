# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/")
def home():
    """List all available api routes"""
    return (
        f"All available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date one year from the last date in the data set.
    last_date = dt.date(2017, 8, 23)
    first_date = last_date - dt.timedelta(days=365)

    # Convert the query results from the precipitation analysis to a dictionary using date as the key and prcp as the value
    pcrp_query = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= first_date)
        .all()
    )

    # Close the session
    session.close()

    yearly_pcrp = []
    for date, pcrp in pcrp_query:
        pcrp_dict = {}
        pcrp_dict["date"] = date
        pcrp_dict["pcrp"] = pcrp
        yearly_pcrp.append(pcrp_dict)

    return jsonify(yearly_pcrp)


@app.route("/api/v1.0/stations")
def stations():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    # Create a list of all stations in the dataset and return them as a json list
    all_stations = [Measurement.station]
    station_list = session.query(*all_stations).group_by(Measurement.station).all()

    # Close the session
    session.close()

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def stations():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    # Find the most active station
    most_active_stations = session.query(
        Measurement.station, func.count(Measurement.station)
    ).group_by(Measurement.station)
    most_active_stations = most_active_stations.order_by(
        func.count(Measurement.station).desc()
    ).all()
    most_active_station = most_active_stations[0][0]

    # Calculate the date one year from the last date in the data set.
    last_date = dt.date(2017, 8, 23)
    first_date = last_date - dt.timedelta(days=365)

    # Query the dates and temperature observations of the most-active station for the previous year of data
    tobs_query = (
        session.query(
            Measurement.stations, Measurement.pcrp, Measurement.date, Measurement.tobs
        )
        .filter(Measurement.date >= first_date)
        .filter(Measurement.station == most_active_station)
        .all()
    )

    # Close the session
    session.close()

    # Return a JSON list of temperature observations for the previous year
