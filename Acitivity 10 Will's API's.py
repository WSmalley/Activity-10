
from flask import Flask, jsonify
import datetime as dt
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:////Users/willsmalley/Desktop/hawaii.sqlite")

Base = automap_base()
Base.prepare(autoload_with=engine)
# reflect the tables
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return(
        f"Welcome to Will's Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date (replace start_date with a date in 'YYYY-MM-DD' format)<br/>"
        f"/api/v1.0/start_date/end_date (replace start_date and end_date with dates in 'YYYY-MM-DD' format)"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = (dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)).strftime("%Y-%m-%d")

    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    station_list = [station[0] for station in stations]

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    most_active_station = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count().desc()).first()[0]
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = (dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)).strftime("%Y-%m-%d")

    temperature_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station, Measurement.date >= one_year_ago).all()

    return jsonify(temperature_data)

@app.route("/api/v1.0/<start>")
def temperature_stats_start(start):
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    return jsonify({"TMIN": temperature_stats[0][0], "TAVG": temperature_stats[0][1], "TMAX": temperature_stats[0][2]})

@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_start_end(start, end):
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()

    return jsonify({"TMIN": temperature_stats[0][0], "TAVG": temperature_stats[0][1], "TMAX": temperature_stats[0][2]})

if __name__ == "__main__":
    app.run(debug=True)










