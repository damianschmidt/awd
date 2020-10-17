import pandas as pd

from utils import step


def process_data():
    progress = 0
    number_of_steps = 7
    datafile = 'top_one'

    progress = step(progress, number_of_steps)
    print('Get data...')
    data = pd.read_csv(f'data/{datafile}.csv', sep=';', dtype=str)

    progress = step(progress, number_of_steps)
    add_extra_date_fields(data)
    
    progress = step(progress, number_of_steps)
    add_location_info(data)

    progress = step(progress, number_of_steps)
    merge_fields_from_multiple_columns(data)

    progress = step(progress, number_of_steps)
    remove_conflicts(data)

    progress = step(progress, number_of_steps)
    sort_data(data)

    progress = step(progress, number_of_steps)
    print('Save data...')
    data.to_csv(f'data/{datafile}_processed.csv', index=False)

    step(progress, number_of_steps)


def resolve_location(code, data):
    _, latitude, longitude, altitude = data[data['Code'] == code].iloc[0]
    return pd.Series([latitude, longitude, altitude])


def add_extra_date_fields(data):
    print('Add extra date fields...')
    data['Date'] = pd.to_datetime(data['Date'], infer_datetime_format=True)
    data['Year'] = data['Date'].apply(lambda x: x.year)
    data['Month'] = data['Date'].apply(lambda x: x.month)
    data['Day'] = data['Date'].apply(lambda x: x.day)
    data['Hour'] = data['Date'].apply(lambda x: x.hour)


def add_location_info(data):
    print('Add location info...')
    working_data = pd.read_csv('data/weather_stations_codes.csv', sep=';', dtype=str,
                    usecols=['Código', 'Latitude', 'Longitude', 'Altitude'])
    working_data.rename(columns={'Código': 'Code'}, inplace=True)
    data[['Latitude', 'Longitude', 'Altitude']] = data['Code'].apply(lambda x: resolve_location(x, working_data))


def merge_fields_from_multiple_columns(data):
    print('Merge fields from multiple columns...')
    data['Humidity0'], data['Humidity12'], data['Humidity18'] = [0, 0, 0]
    data['Pressure0'], data['Pressure12'], data['Pressure18'] = [0.0, 0.0, 0.0]
    data['WindDirection0'], data['WindDirection12'], data['WindDirection18'] = [0, 0, 0]
    data['WindSpeed0'], data['WindSpeed12'], data['WindSpeed18'] = [0.0, 0.0, 0.0]
    data['Cloudiness0'], data['Cloudiness12'], data['Cloudiness18'] = [0.0, 0.0, 0.0]

    for index, morning in data[:-3].iterrows():
        if morning['Hour'] != 0:
            continue

        midday = data.iloc[index + 1]
        evening = data.iloc[index + 2]

        data.at[index, 'Precipitation'] = morning['Precipitation'] \
            if pd.notnull(morning['Precipitation']) else midday['Precipitation'] \
            if pd.notnull(midday['Precipitation']) else evening['Precipitation'] \
            if pd.notnull(evening['Precipitation']) else -1
        data.at[index, 'MinTemp'] = midday['MinTemp'] if pd.notnull(midday['MinTemp']) else -1
        data.at[index, 'MaxTemp'] = morning['MaxTemp'] if pd.notnull(morning['MaxTemp']) else -1
        data.at[index, 'Humidity0'], data.at[index, 'Humidity12'], data.at[index, 'Humidity18'] = \
            [morning['Humidity'] if pd.notnull(morning['Humidity']) else -1,
            midday['Humidity'] if pd.notnull(midday['Humidity']) else -1,
            evening['Humidity'] if pd.notnull(evening['Humidity']) else -1]
        data.at[index, 'Pressure0'], data.at[index, 'Pressure12'], data.at[index, 'Pressure18'] = \
            [morning['PressureStation'] if pd.notnull(morning['PressureStation']) else -1,
            midday['PressureStation'] if pd.notnull(midday['PressureStation']) else -1,
            evening['PressureStation'] if pd.notnull(evening['PressureStation']) else -1]
        data.at[index, 'WindDirection0'], data.at[index, 'WindDirection12'], data.at[index, 'WindDirection18'] = \
            [morning['WindDirection'] if pd.notnull(morning['WindDirection']) else -1,
            midday['WindDirection'] if pd.notnull(midday['WindDirection']) else -1,
            evening['WindDirection'] if pd.notnull(evening['WindDirection']) else -1]
        data.at[index, 'WindSpeed0'], data.at[index, 'WindSpeed12'], data.at[index, 'WindSpeed18'] = \
            [morning['WindSpeed'] if pd.notnull(morning['WindSpeed']) else -1,
            midday['WindSpeed'] if pd.notnull(midday['WindSpeed']) else -1,
            evening['WindSpeed'] if pd.notnull(evening['WindSpeed']) else -1]
        data.at[index, 'Cloudiness0'], data.at[index, 'Cloudiness12'], data.at[index, 'Cloudiness18'] = \
            [morning['Cloudiness'] if pd.notnull(morning['Cloudiness']) else -1,
            midday['Cloudiness'] if pd.notnull(midday['Cloudiness']) else -1,
            evening['Cloudiness'] if pd.notnull(evening['Cloudiness']) else -1]

    data.drop(['DryBulbTemp', 'WetBulbTemp', 'Evaporation', 'AvgCompTemp', 'AvgRelHumidity', 'AvgWindSpeed', 'Humidity',
            'PressureStation', 'PressureSea', 'WindDirection', 'WindSpeed', 'Cloudiness'], 1, inplace=True)

    avg_process_columns = ['Humidity0', 'Humidity12', 'Humidity18',
                        'Pressure0', 'Pressure12', 'Pressure18',
                        'Cloudiness0', 'Cloudiness12', 'Cloudiness18']

    data[avg_process_columns] = data[avg_process_columns].apply(pd.to_numeric, axis=1)

    data['AvgHumidity'] = data[['Humidity0', 'Humidity12', 'Humidity18']].apply(lambda x: (x[0] + x[1] + x[2]) / 3, axis=1)
    data['AvgPressure'] = data[['Pressure0', 'Pressure12', 'Pressure18']].apply(lambda x: (x[0] + x[1] + x[2]) / 3, axis=1)
    data['AvgCloudiness'] = data[['Cloudiness0', 'Cloudiness12', 'Cloudiness18']].apply(lambda x: (x[0] + x[1] + x[2]) / 3,

                                                                                        axis=1)
def remove_conflicts(data):
    print('Remove confilcts...')
    data = data[(data['Hour'] == 0) & (data['Precipitation'] != -1) & (data['MinTemp'] != -1) & (data['MaxTemp'] != -1)]
    data.drop('Hour', 1, inplace=True)
    data = data[(data['Humidity0'] != -1) & (data['Humidity12'] != -1) & (data['Humidity18'] != -1)]
    data = data[(data['Pressure0'] != -1) & (data['Pressure12'] != -1) & (data['Pressure18'] != -1)]
    data = data[(data['WindDirection0'] != -1) & (data['WindDirection12'] != -1) & (data['WindDirection18'] != -1)]
    data = data[(data['WindSpeed0'] != -1) & (data['WindSpeed12'] != -1) & (data['WindSpeed18'] != -1)]
    data = data[(data['Cloudiness0'] != -1) & (data['Cloudiness12'] != -1) & (data['Cloudiness18'] != -1)]


def sort_data(data):
    print('Sort data...')
    data.sort_values(by=['Date'], ascending=True, inplace=True)
    data.reset_index(drop=True, inplace=True)


if __name__ == '__main__':
    process_data()
