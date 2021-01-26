import configparser

import pandas as pd
import numpy as np

PROGRESS = 0


def process(station_code_set):
    def step():
        global PROGRESS
        PROGRESS += 1
        print(f'Progress: {PROGRESS}')

    def resolve_location(code):
        _, latitude, longitude, altitude = s_df[s_df['Code'] == code].iloc[0]
        return pd.Series([latitude, longitude, altitude])

    def resolve_wind(wind):
        try:
            return int(float(wind))
        except:
            return wind

    def find_wind_direction(wind0, wind12, wind18, winds_code):
        if wind0 != winds_code['V']:
            return wind0
        elif wind12 != winds_code['V']:
            return wind12
        elif wind18 != winds_code['V']:
            return wind18
        return -1

    # Loading configuration
    config = configparser.ConfigParser()
    config.read('backend/weather/config.ini')
    processing_percentage = config.getint('APP', 'PROCESSING_PERCENTAGE')

    for station_code in station_code_set:
        print(f'Process: {station_code}')
        # Selecting data
        step()  # 1
        w_df = pd.read_csv(
            f'data/simplified/{station_code}_simplified.csv', sep=';', dtype=str)

        # Add extra date fields for later
        step()  # 2
        w_df['Date'] = pd.to_datetime(w_df['Date'], infer_datetime_format=True)
        w_df['Year'] = w_df['Date'].apply(lambda x: x.year)
        w_df['Month'] = w_df['Date'].apply(lambda x: x.month)
        w_df['Day'] = w_df['Date'].apply(lambda x: x.day)
        w_df['Hour'] = w_df['Date'].apply(lambda x: x.hour)

        # Resolve location
        step()  # 3
        s_df = pd.read_csv('data/src/weather_stations_codes.csv', sep=';', dtype=str,
                           usecols=['Código', 'Latitude', 'Longitude', 'Altitude'])
        s_df.rename(columns={'Código': 'Code'}, inplace=True)
        w_df[['Latitude', 'Longitude', 'Altitude']
             ] = w_df['Code'].apply(resolve_location)

        # Merge fields from multiple columns
        step()  # 4
        w_df['WindDirection'] = w_df['WindDirection'].apply(resolve_wind)
        w_df['Humidity0'], w_df['Humidity12'], w_df['Humidity18'] = [0, 0, 0]
        w_df['Pressure0'], w_df['Pressure12'], w_df['Pressure18'] = [0.0, 0.0, 0.0]
        w_df['WindDirection0'], w_df['WindDirection12'], w_df['WindDirection18'] = [
            0, 0, 0]
        w_df['WindSpeed0'], w_df['WindSpeed12'], w_df['WindSpeed18'] = [
            0.0, 0.0, 0.0]
        w_df['Cloudiness0'], w_df['Cloudiness12'], w_df['Cloudiness18'] = [
            0.0, 0.0, 0.0]
        for index, morning in w_df[:-3].iterrows():
            if morning['Hour'] != 0:
                continue

            midday = w_df.iloc[index + 1]
            evening = w_df.iloc[index + 2]

            w_df.at[index, 'Precipitation'] = morning['Precipitation'] \
                if pd.notnull(morning['Precipitation']) else midday['Precipitation'] \
                if pd.notnull(midday['Precipitation']) else evening['Precipitation'] \
                if pd.notnull(evening['Precipitation']) else -1
            w_df.at[index, 'MinTemp'] = midday['MinTemp'] if pd.notnull(
                midday['MinTemp']) else -1
            w_df.at[index, 'MaxTemp'] = morning['MaxTemp'] if pd.notnull(
                morning['MaxTemp']) else -1
            w_df.at[index, 'Humidity0'], w_df.at[index, 'Humidity12'], w_df.at[index, 'Humidity18'] = \
                [morning['Humidity'] if pd.notnull(morning['Humidity']) else -1,
                 midday['Humidity'] if pd.notnull(midday['Humidity']) else -1,
                 evening['Humidity'] if pd.notnull(evening['Humidity']) else -1]
            w_df.at[index, 'Pressure0'], w_df.at[index, 'Pressure12'], w_df.at[index, 'Pressure18'] = \
                [morning['PressureStation'] if pd.notnull(morning['PressureStation']) else -1,
                 midday['PressureStation'] if pd.notnull(
                     midday['PressureStation']) else -1,
                 evening['PressureStation'] if pd.notnull(evening['PressureStation']) else -1]
            w_df.at[index, 'WindDirection0'], w_df.at[index, 'WindDirection12'], w_df.at[index, 'WindDirection18'] = \
                [morning['WindDirection'] if pd.notnull(morning['WindDirection']) else -1,
                 midday['WindDirection'] if pd.notnull(
                     midday['WindDirection']) else -1,
                 evening['WindDirection'] if pd.notnull(evening['WindDirection']) else -1]
            w_df.at[index, 'WindSpeed0'], w_df.at[index, 'WindSpeed12'], w_df.at[index, 'WindSpeed18'] = \
                [morning['WindSpeed'] if pd.notnull(morning['WindSpeed']) else -1,
                 midday['WindSpeed'] if pd.notnull(
                     midday['WindSpeed']) else -1,
                 evening['WindSpeed'] if pd.notnull(evening['WindSpeed']) else -1]
            w_df.at[index, 'Cloudiness0'], w_df.at[index, 'Cloudiness12'], w_df.at[index, 'Cloudiness18'] = \
                [morning['Cloudiness'] if pd.notnull(morning['Cloudiness']) else -1,
                 midday['Cloudiness'] if pd.notnull(
                     midday['Cloudiness']) else -1,
                 evening['Cloudiness'] if pd.notnull(evening['Cloudiness']) else -1]
        w_df.drop(
            ['DryBulbTemp', 'WetBulbTemp', 'Evaporation', 'AvgCompTemp', 'AvgRelHumidity', 'AvgWindSpeed', 'Humidity',
             'PressureStation', 'PressureSea', 'WindDirection', 'WindSpeed', 'Cloudiness'], 1, inplace=True)
        avg_process_columns = ['Humidity0', 'Humidity12', 'Humidity18',
                               'Pressure0', 'Pressure12', 'Pressure18',
                               'Cloudiness0', 'Cloudiness12', 'Cloudiness18']
        w_df[avg_process_columns] = w_df[avg_process_columns].apply(
            pd.to_numeric, axis=1)
        w_df['AvgHumidity'] = w_df[['Humidity0', 'Humidity12', 'Humidity18']].apply(lambda x: (x[0] + x[1] + x[2]) / 3,
                                                                                    axis=1)
        w_df['AvgPressure'] = w_df[['Pressure0', 'Pressure12', 'Pressure18']].apply(lambda x: (x[0] + x[1] + x[2]) / 3,
                                                                                    axis=1)
        w_df['AvgCloudiness'] = w_df[['Cloudiness0', 'Cloudiness12', 'Cloudiness18']].apply(
            lambda x: (x[0] + x[1] + x[2]) / 3,
            axis=1)
        w_df['AvgWindSpeed'] = w_df[['WindSpeed0', 'WindSpeed12', 'WindSpeed18']].apply(
            lambda x: (x[0] + x[1] + x[2]) / 3,
            axis=1)
        # Remove conflicts
        step()  # 5
        w_df = w_df[
            (w_df['Hour'] == 0) & (w_df['Precipitation'] != -1) & (w_df['MinTemp'] != -1) & (w_df['MaxTemp'] != -1)]
        w_df.drop('Hour', 1, inplace=True)
        w_df = w_df[(w_df['Humidity0'] != -1) &
                    (w_df['Humidity12'] != -1) & (w_df['Humidity18'] != -1)]
        w_df = w_df[(w_df['Pressure0'] != -1) &
                    (w_df['Pressure12'] != -1) & (w_df['Pressure18'] != -1)]
        w_df = w_df[(w_df['WindDirection0'] != -1) &
                    (w_df['WindDirection12'] != -1) & (w_df['WindDirection18'] != -1)]
        w_df = w_df[(w_df['WindSpeed0'] != -1) &
                    (w_df['WindSpeed12'] != -1) & (w_df['WindSpeed18'] != -1)]
        w_df = w_df[(w_df['Cloudiness0'] != -1) &
                    (w_df['Cloudiness12'] != -1) & (w_df['Cloudiness18'] != -1)]

        # Simplify wind codes
        winds = pd.read_csv(
            'data/src/wind_directions_codes.csv', sep=';', dtype=str)
        winds_dict = {
            'NNE': 0, 'NE': 1, 'ENE': 2, 'E': 2, 'ESE': 2, 'SE': 3, 'SSE': 4, 'S': 4, 'SSW': 4, 'SW': 5, 'WSW': 6,
            'W': 6, 'WNW': 6, 'NW': 7, 'NNW': 0, 'N': 0, 'V': 8
        }

        w_df['WindDirection0'] = w_df.WindDirection0.apply(
            lambda x: winds_dict[winds.loc[winds.Id == str(x), 'Símbolo'].values[0]])
        w_df['WindDirection12'] = w_df.WindDirection12.apply(
            lambda x: winds_dict[winds.loc[winds.Id == str(x), 'Símbolo'].values[0]])
        w_df['WindDirection18'] = w_df.WindDirection18.apply(
            lambda x: winds_dict[winds.loc[winds.Id == str(x), 'Símbolo'].values[0]])

        w_df['WindDirection'] = w_df[['WindDirection0', 'WindDirection12', 'WindDirection18']].apply(
            lambda x: find_wind_direction(x[0], x[1], x[2], winds_dict), axis=1)
        w_df = w_df[(w_df['WindDirection'] != -1)]

        # Sort the data
        step()  # 6
        w_df.sort_values(by=['Date'], ascending=True, inplace=True)
        w_df.reset_index(drop=True, inplace=True)

        # Save data
        step()  # 7
        processing_size = int(len(w_df) * (0.01 * processing_percentage))
        w_df[-processing_size:].to_csv(f'data/processed/{station_code}_processed_{processing_percentage}.csv', sep=';',
                                       index=False)


if __name__ == '__main__':
    code_set = {'82331'}
    process(code_set)