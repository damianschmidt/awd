from learn import learn
from process import process
from simplify import simplify
from weather_api_mock import prepare_api
from run import run

# AIRPORT_STATION = {'SBAX': '83579', 'SBAT': '83214', 'SBAR': '83096', 'SBAU': '83623', 'SBHT': '82353',
#                    'SBBU': '83773', 'SBBE': '82191', 'SBPS': '83446', 'SBBR': '83373', 'SBBV': '82024',
#                    'SBCY': '83361', 'SBSP': '83781', 'SBCG': '83704', 'SBCR': '83552', 'SBCF': '83587',
#                    'SBKG': '82795', 'SBCT': '83842', 'SBFZ': '82397', 'SBGL': '83743', 'SBGR': '83075',
#                    'SBFI': '83881', 'SBJP': '82798', 'SBNT': '82598', 'SBBH': '83587', 'SBPA': '83967',
#                    'SBRF': '82900', 'SBRJ': '83743', 'SBSV': '83229', 'SBKP': '83851', 'SBVT': '83648',
#                    'SBCH': '83883'}

AIRPORT_STATION = {'SBAX': '83579'}


def prepare():
    input_wind_features = ['Month', 'WindDirection', 'Humidity12']
    output_wind_features = ['WindDirection']

    input_weather_features = ['Year', 'Month', 'Precipitation', 'MaxTemp', 'MinTemp', 'Insolation', 'AvgHumidity',
                              'AvgPressure', 'WindDirection', 'AvgWindSpeed', 'AvgCloudiness']
    output_weather_features = ['AvgWindSpeed', 'AvgCloudiness', 'AvgPressure', 'Precipitation', 'MinTemp']

    station_code_set = set(AIRPORT_STATION.values())
    simplify(station_code_set)
    process(station_code_set)
    prepare_api(station_code_set)

    for station_code in station_code_set:
        learn(station_code, input_wind_features, output_wind_features, classification=True)
        learn(station_code, input_weather_features, output_weather_features)


def predict(airport, date):
    input_wind_features = ['Month', 'WindDirection', 'Humidity12']
    output_wind_features = ['WindDirection']

    input_weather_features = ['Year', 'Month', 'Precipitation', 'MaxTemp', 'MinTemp', 'Insolation', 'AvgHumidity',
                              'AvgPressure', 'WindDirection', 'AvgWindSpeed', 'AvgCloudiness']
    output_weather_features = ['AvgWindSpeed', 'AvgCloudiness', 'AvgPressure', 'Precipitation', 'MinTemp']

    station_code = AIRPORT_STATION[airport]
    wind_direction = run(station_code, date, input_wind_features, output_wind_features, classification=True)
    weather_data = run(station_code, date, input_weather_features, output_weather_features)
    weather_data['WindDirection'] = wind_direction
    return weather_data

if __name__ == '__main__':
    data = predict('SBAX', '2021-01-30')
    print(data)
