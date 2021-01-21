import configparser
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras.engine.saving import load_model
from keras.utils import np_utils
from sklearn.preprocessing import RobustScaler

from weather_api_mock import get_previous_days


def run(station, date, input_features, output_features, classification=False):
    # Loading configuration
    config = configparser.ConfigParser()
    config.read('config.ini')
    processing_percentage = config.getint('APP', 'PROCESSING_PERCENTAGE')
    future_period_predict = config.getint('LEARNING', 'FUTURE_PERIOD_PREDICT')
    history_period_size = config.getint('LEARNING', 'HISTORY_PERIOD_SIZE')

    # Prepare sequences and predictions
    records = get_previous_days(station, date)
    model = load_model(f'models/{station}_wind_direction.h5') if classification else load_model(f'models/{station}_weather.h5')
    
    # Scale
    pd.options.mode.chained_assignment = None  # disable false warning for copying

    x_transformer = RobustScaler()
    x_transformer = x_transformer.fit(records[input_features].to_numpy())
    x_scaled = x_transformer.transform(records[input_features].to_numpy())


    if classification:
        y_scaled = np_utils.to_categorical(records[output_features].to_numpy())
        y_labels = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'V']
    else:
        y_transformer = RobustScaler()
        y_transformer = y_transformer.fit(records[output_features].to_numpy())
        y_scaled = y_transformer.transform(records[output_features].to_numpy())

    # Prepare sequences
    sequential_data = []
    for i in range(len(x_scaled) - history_period_size - future_period_predict):
        sequential_data.append([
            x_scaled[i:(i + history_period_size)],
            y_scaled[i + history_period_size + future_period_predict - 1]
        ])
    x, y = [], []
    for seq, target in sequential_data:
        x.append(seq)
        y.append(target)

    # Predict
    x_pred = np.array(x)
    y_pred = np.array(y)

    if classification:
        y_inverse = y_pred.argmax(axis=1)
        predicted = model.predict(x_pred)
        predicted_inverse = np.argmax(predicted, axis=1)
        print(y_labels[y_inverse[0]], y_labels[predicted_inverse[0]])
        return y_labels[predicted_inverse[0]]
    else:
        y_inverse = y_transformer.inverse_transform(y_pred)
        predicted = model.predict(x_pred)
        predicted_inverse = y_transformer.inverse_transform(predicted)
        print(output_features)
        print(predicted_inverse[0])
        return {output_features[i]: predicted_inverse[0][i] for i in range(len(output_features))}


if __name__ == '__main__':
    pass
