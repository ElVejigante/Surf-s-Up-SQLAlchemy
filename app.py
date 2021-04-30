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

# Flask Setup

app = Flask(__name__)

# Flask Routes

@app.route("/")

