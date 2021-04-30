import numpy as np
import re
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql import exists  
from flask import Flask, jsonify

# Database Setup

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station
# Create our session (link) from Python to the DB
inspector = inspect(engine)

# Flask Setup

app = Flask(__name__)

# Flask Routes
# Home Page
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return ("---Home page----<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"dates in the form YYYY-MM-DD"
    )

# Precipitation JSON
@app.route("/api/v1.0/precipitation") 
def precipitation():
    # Link Session
    session = Session(engine)

    # Query Measurement
    results = (session.query(Measurement.date, Measurement.tobs)
                      .order_by(Measurement.date))
    
    # Create a dictionary
    precipitation_date_tobs = []
    for each_row in results:
        dt_dict = {}
        dt_dict["date"] = each_row.date
        dt_dict["tobs"] = each_row.tobs
        precipitation_date_tobs.append(dt_dict)

    return jsonify(precipitation_date_tobs)

# Stations JSON
@app.route("/api/v1.0/stations") 
def stations():
    # Link Session
    session = Session(engine)

    # Query Stations
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    station_details = list(np.ravel(results))

    return jsonify(station_details)

# Observed Temperatures JSON
@app.route("/api/v1.0/tobs") 
def stations():
    # Link Session
    session = Session(engine)

    station_activity=(session.query(Measurement.station,func.count(Measurement.station))
                         .group_by(Measurement.station)
                         .order_by(func.count(Measurement.station).desc())
                         .all())
    most_active_station = station_activity[0][0]
    tobs=[Measurement.station, 
             func.min(Measurement.tobs), 
             func.max(Measurement.tobs), 
             func.avg(Measurement.tobs)]
    station_query=(session.query(*tobs)
                       .filter(Measurement.station==most_active_station)
                       .all())
#_station_query

query_temps=pd.DataFrame(station_query, columns=['station', 'min_temp', 
                                                          'max_temp', 'avg_temp'])
query_temps.set_index('station', inplace=True)
query_temps
