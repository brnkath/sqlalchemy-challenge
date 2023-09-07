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
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
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
def tobs():
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
        session.query(Measurement.stations, Measurement.date, Measurement.tobs)
        .filter(Measurement.date >= first_date)
        .filter(Measurement.station == most_active_station)
        .all()
    )

    # Close the session
    session.close()

    # Convert the tobs query to a dictionary
    query_list = []
    for station, date, tobs in tobs_query:
        query_dict = {}
        query_dict["station"] = station
        query_dict["date"] = date
        query_dict["tobs"] = tobs

        query_list.append(query_dict)

    # Return a JSON list of temperature observations for the previous year
    return jsonify(query_list)


@app.route("/api/v1.0/<start>")
def start(start):
    # Create a session (link) from Python to the DB
    session = Session(engine)

    # Calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
    start_query = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .all()
    )

    # Close the session
    session.close()

    # Convert list of tuples into normal list
    start_results = list(np.ravel(start_query))

    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date
    return jsonify(start_results)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create a session (link) from Python to the DB
    session = Session(engine)

    # Calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date and less than or equal to the end date
    start_end_query = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .filter(Measurement.date <= end)
        .all()
    )

    # Close the session
    session.close()

    # Convert list of tuples into normal list
    start_end_results = list(np.ravel(start_end_query))

    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start and end date
    return jsonify(start_end_results)


if __name__ == "__main__":
    app.run(debug=True)
