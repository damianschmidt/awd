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
            latitude
            longitude
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
        'magnetic Varation': data['magneticVariation']
    }
    runways_count = data['runwayCount'] * 2

    if runways_count == 2:
        airport_info_dict['runway ident'] = data['runways'][0]['ident']
        airport_info_dict['runway lat'] = data['runways'][0]['ends'][0]['lat']
        airport_info_dict['runway lon'] = data['runways'][0]['ends'][0]['lon']
        airport_info_dict['runway surface'] = data['runways'][0]['surface']
    else:
        for i in range(0, runways_count):
            airport_info_dict[f'runway ident{i}'] = data['runways'][i]['ident']
            airport_info_dict[f'runway lat{i}'] = data['runways'][i]['ends'][0]['lat']
            airport_info_dict[f'runway lon{i}'] = data['runways'][i]['ends'][0]['lon']
            airport_info_dict[f'runway surface{i}'] = data['runways'][i]['surface']
            
    return airport_info_dict 


@FLIGHT.route('/<string:ICAO>', methods=['GET'])
def airport_info_api(ICAO):
    data = airport_info(ICAO)
    return jsonify(data), 200
