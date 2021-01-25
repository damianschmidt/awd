import json
import pandas as pd

from flask import Blueprint, jsonify
import datetime as dt
from ..weather.predict import predict

WEATHER = Blueprint('weather_info', __name__)


@WEATHER.route('/<string:ICAO>/<string:datetime>', methods=['GET'])
def index(ICAO, datetime):
    date_time_obj = dt.datetime.strptime(datetime, '%Y-%m-%d')
    weather_dict = {'AvgWindSpeed': 2.1854916, 'AvgCloudiness': 3.1873982,
                    'AvgPressure': 1012.7367, 'Precipitation': 2.561558,
                    'MinTemp': 24.013891, 'WindDirection': 'E'}
    tmp = predict(ICAO, datetime)
    tmp2=pd.Series(tmp).to_json(orient='values')
    return jsonify(tmp2), 200
