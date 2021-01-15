import requests
import json
from flask import Blueprint, jsonify

FLIGHT = Blueprint('airport_info', __name__)


def airport_info(ICAO):
    """
    get info about airport
    input airport ICAO
    output:
        airport name
        airport latitude
        airport longitude 
        airport elevation
        airport magnetic variation
        airport runways
            identifier
            length
            width
            surface
    """
    url = f'https://api.flightplandatabase.com/nav/airport/{ICAO}'
    r = requests.get(url=url)
    data = r.json()
    airport_info_dict = {
        'name': data['name'],
        'latitude': data['lat'],
        'longitude': data['lon'],
        'elevation': data['elevation'],
        'magnetic Varation': data['magneticVariation'],
        'runway ident': [],
        'runway length': [],
        'runway width': [],
        'runway surface': []
    }
    runways_count = data['runwayCount'] * 2

    for i in range(0, runways_count):
        if runways_count == 2:
            i = 0
        airport_info_dict['runway ident'].append(data['runways'][i]['ident'])
        airport_info_dict['runway length'].append(data['runways'][i]['length'])
        airport_info_dict['runway width'].append(data['runways'][i]['width'])
        airport_info_dict['runway surface'].append(data['runways'][i]['surface'])
    return airport_info_dict


@FLIGHT.route('/<string:ICAO>', methods=['GET'])
def airport_info_api(ICAO):
    data = airport_info(ICAO)
    return jsonify(data), 200
