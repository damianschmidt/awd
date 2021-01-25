import pandas as pd
from flask import Blueprint, jsonify

from ..weather.predict import predict

WEATHER = Blueprint('weather_info', __name__)


@WEATHER.route('/<string:ICAO>/<string:datetime>', methods=['GET'])
def index(ICAO, datetime):
    tmp = predict(ICAO, datetime)
    tmp2 = pd.Series(tmp).to_json(orient='values')
    return jsonify(tmp2), 200
