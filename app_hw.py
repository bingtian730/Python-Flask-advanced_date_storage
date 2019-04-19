import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, make_response
from gevent.pywsgi import WSGIServer
from json import dumps

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base=automap_base()
Base.prepare(engine, reflect=True)



Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
end_date=session.query(func.max(Measurement.date))
#end_date='2017-08-23'

app = Flask(__name__)

@app.route("/")
def welcome():
    return('Welcome to Bing page')

@app.route("/api/precipitation")
def precipitation():
    prcp_dict={}
    key_list=session.query(Measurement.date)
    value_list=session.query(Measurement.prcp)
    key_list=[x[0] for x in key_list]
    value_list=[x[0] for x in value_list]
    prcp_dict= dict((key, value) for (key, value) in zip(key_list, value_list))
    return jsonify(prcp_dict)

@app.route("/api/stations")
def station():
    result = engine.execute("SELECT DISTINCT name from Station" ).fetchall()
    return jsonify({'result': [dict(row) for row in result]})

@app.route("/api/temperature")
def temperature():
    temp=session.query(Measurement.tobs).filter(Measurement.date>'2016-08-22').all()
    result=[str(x[0]) for x in temp]
    return jsonify({'result':result})


@app.route("/api/<start>",defaults={"end": end_date})
@app.route("/api/<start>/<end>")
def calc_temps(start, end):
    result=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >=start).filter(Measurement.date <=end).all()
    return jsonify({'result':result})


if  __name__ == '__main__':
    app.run(host='localhost',debug=True)
    