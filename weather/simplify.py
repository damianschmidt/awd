import pandas as pd


def simplify(station_code_set):
    df = pd.read_csv('data/src/conventional_weather_stations_inmet_brazil_1961_2019.csv', sep=';', dtype=str, usecols=[
        'Estacao', 'Data', 'Hora', 'Precipitacao', 'TempBulboSeco', 'TempBulboUmido', 'TempMaxima', 'TempMinima',
        'UmidadeRelativa', 'PressaoAtmEstacao', 'PressaoAtmMar', 'DirecaoVento', 'VelocidadeVento', 'Insolacao',
        'Nebulosidade', 'Evaporacao Piche', 'Temp Comp Media', 'Umidade Relativa Media', 'Velocidade do Vento Media'
    ])
    df.rename(columns={'Estacao': 'Code', 'Data': 'Date', 'Hora': 'Hour',
                       'Precipitacao': 'Precipitation', 'TempBulboSeco': 'DryBulbTemp',
                       'TempBulboUmido': 'WetBulbTemp', 'TempMaxima': 'MaxTemp',
                       'TempMinima': 'MinTemp', 'UmidadeRelativa': 'Humidity',
                       'PressaoAtmEstacao': 'PressureStation', 'PressaoAtmMar': 'PressureSea',
                       'DirecaoVento': 'WindDirection', 'VelocidadeVento': 'WindSpeed',
                       'Insolacao': 'Insolation', 'Nebulosidade': 'Cloudiness',
                       'Evaporacao Piche': 'Evaporation', 'Temp Comp Media': 'AvgCompTemp',
                       'Umidade Relativa Media': 'AvgRelHumidity',
                       'Velocidade do Vento Media': 'AvgWindSpeed'}, inplace=True)

    # Connect the date
    df['Date'] = df['Date'] + ' ' + df['Hour'].apply(lambda x: x[0:2] + ':' + x[2:4] + ':00')
    df.drop('Hour', 1, inplace=True)

    # Save selected data
    for station_code in station_code_set:
        print(f'Simplify: {station_code}')
        df[df['Code'] == station_code].to_csv(f'data/simplified/{station_code}_simplified.csv', sep=';', index=False)


if __name__ == '__main__':
    code_set = {'82331'}
    simplify(code_set)
