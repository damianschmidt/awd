import configparser

import pandas as pd


def prepare_api(station_code_set):
    pd.options.mode.chained_assignment = None
    config = configparser.ConfigParser()
    config.read('backend/weather/config.ini')
    processing_percentage = config.getint('APP', 'PROCESSING_PERCENTAGE')

    for station_code in station_code_set:
        df = pd.read_csv(f'backend/weather/data/processed/{station_code}_processed_{processing_percentage}.csv', sep=';', dtype=str)
        year = 2017
        while True:
            w_df = df[df.Year == str(year)]
            if len(w_df['Year']) < 100:
                year -= 1
            else:
                break

        w_df['Year'] = w_df['Year'].apply(lambda x: '2021')
        w_df['Date'] = w_df['Date'].apply(lambda x: '2021' + x[4:])
        w_df.to_csv(f'backend/weather/data/api/{station_code}_api.csv', sep=';', index=False)


def get_previous_days(station_code, date):
    config = configparser.ConfigParser()
    config.read('backend/weather/config.ini')
    history_period_size = config.getint('LEARNING', 'HISTORY_PERIOD_SIZE')

    w_df = pd.read_csv(f'backend/weather/data/api/{station_code}_api.csv', sep=';', dtype=str)
    idx = w_df.index.get_loc(w_df[w_df['Date'] == date].index[0])
    previous = idx - history_period_size if (idx - history_period_size) > 0 else 0
    return w_df.iloc[previous-2:idx]



if __name__ == '__main__':
    # get_previous_days('83579', '2021-01-25')
    prepare_api({'82024'})
