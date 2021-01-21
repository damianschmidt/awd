import configparser

import pandas as pd


def prepare_api(station_code_set):
    config = configparser.ConfigParser()
    config.read('config.ini')
    processing_percentage = config.getint('APP', 'PROCESSING_PERCENTAGE')

    for station_code in station_code_set:
        w_df = pd.read_csv(f'data/processed/{station_code}_processed_{processing_percentage}.csv', sep=';', dtype=str)
        w_df = w_df[w_df.Year == '2017']
        w_df['Year'] = w_df['Year'].apply(lambda x: '2021')
        w_df['Date'] = w_df['Date'].apply(lambda x: '2021' + x[4:])
        w_df.to_csv(f'data/api/{station_code}_api.csv', sep=';', index=False)


def get_previous_days(station_code, date):
    config = configparser.ConfigParser()
    config.read('config.ini')
    history_period_size = config.getint('LEARNING', 'HISTORY_PERIOD_SIZE')

    w_df = pd.read_csv(f'data/api/{station_code}_api.csv', sep=';', dtype=str)
    idx = w_df.index.get_loc(w_df[w_df['Date'] == date].index[0])
    previous = idx - history_period_size if (idx - history_period_size) > 0 else 0
    return w_df.iloc[previous-2:idx]



if __name__ == '__main__':
    get_previous_days('83579', '2021-01-25')
