from os import path

import matplotlib.pyplot as plt
import pandas as pd
from weather.utils import step

DATASET_URL = 'https://www.kaggle.com/saraivaufc/conventional-weather-stations-brazil/download'
DATASET_NAME = 'conventional_weather_stations_inmet_brazil_1961_2019.csv'


def simplify_data():
    progress = 0
    number_of_steps = 5

    progress = step(progress, number_of_steps)
    data = get_data()

    progress = step(progress, number_of_steps)
    format_date(data)

    progress = step(progress, number_of_steps)
    top_five_stations = data['Code'].value_counts().head(5)

    progress = step(progress, number_of_steps)
    save_simplified_data(data, top_five_stations)

    progress = step(progress, number_of_steps)
    plot_stations_with_most_record(top_five_stations)

    step(progress, number_of_steps)


def get_data():
    print('Get data...')
    print('Check if CSV file exists...')

    if not path.isfile('./data/' + DATASET_NAME):
        print('\nDataset does not exists!\nPlease download and unzip dataset to /weather/data/ directory.\n'
              f'URL: {DATASET_URL}')
        exit(1)

    data = pd.read_csv('data/' + DATASET_NAME, sep=';', dtype=str, usecols=[
        'Estacao', 'Data', 'Hora', 'Precipitacao', 'TempBulboSeco', 'TempBulboUmido', 'TempMaxima', 'TempMinima',
        'UmidadeRelativa',
        'PressaoAtmEstacao', 'PressaoAtmMar', 'DirecaoVento', 'VelocidadeVento', 'Insolacao', 'Nebulosidade',
        'Evaporacao Piche',
        'Temp Comp Media', 'Umidade Relativa Media', 'Velocidade do Vento Media'
    ])

    data.rename(columns={
        'Estacao': 'Code',
        'Data': 'Date',
        'Hora': 'Hour',
        'Precipitacao': 'Precipitation',
        'TempBulboSeco': 'DryBulbTemp',
        'TempBulboUmido': 'WetBulbTemp',
        'TempMaxima': 'MaxTemp',
        'TempMinima': 'MinTemp',
        'UmidadeRelativa': 'Humidity',
        'PressaoAtmEstacao': 'PressureStation',
        'PressaoAtmMar': 'PressureSea',
        'DirecaoVento': 'WindDirection',
        'VelocidadeVento': 'WindSpeed',
        'Insolacao': 'Insolation',
        'Nebulosidade': 'Cloudiness',
        'Evaporacao Piche': 'Evaporation',
        'Temp Comp Media': 'AvgCompTemp',
        'Umidade Relativa Media': 'AvgRelHumidity',
        'Velocidade do Vento Media': 'AvgWindSpeed',
    }, inplace=True)

    return data


def format_date(data):
    print('Change date format...')
    data['Date'] = data['Date'] + ' ' + data['Hour'].apply(lambda x: x[0:2] + ':' + x[2:4] + ':00')
    data.drop('Hour', 1, inplace=True)


def save_simplified_data(data, top_five_station):
    print('Save all data...')
    data.to_csv('data/simplified.csv', sep=';', index=False)
    print('Save top one data...')
    data[data['Code'] == top_five_station.index[0]].to_csv('data/top_one.csv', sep=';',
                                                              index=False)


def plot_stations_with_most_record(data):
    print('Plot chart...')
    plt.style.use('fivethirtyeight')
    _, axis = plt.subplots(figsize=(12, 9))
    data.plot.bar(color='green')
    axis.set_xticklabels(axis.get_xticklabels(), rotation=25)
    plt.title('The most active/precious stations')
    plt.show()


if __name__ == "__main__":
    simplify_data()
