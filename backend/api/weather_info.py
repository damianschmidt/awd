from flask import Blueprint, jsonify
import datetime as dt

WEATHER = Blueprint('weather_info', __name__)


@WEATHER.route('/<string:ICAO>/<string:datetime>', methods=['GET'])
def index(ICAO, datetime):
    date_time_obj = dt.datetime.strptime(datetime, '%Y-%m-%d')
    weather_dict = {'AvgWindSpeed': 2.1854916, 'AvgCloudiness': 3.1873982,
                    'AvgPressure': 1012.7367, 'Precipitation': 2.561558,
                    'MinTemp': 24.013891, 'WindDirection': 'E'}
    return jsonify(weather_dict), 200
