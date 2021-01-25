import configparser
import random

import numpy as np
import pandas as pd
from keras import Sequential
from keras.callbacks import TensorBoard, ModelCheckpoint
from keras.layers import Dense, Dropout, LSTM, Bidirectional
from keras.optimizers import Adam
from keras.utils import np_utils
from sklearn.preprocessing import RobustScaler


def prepare(processing, input_features, output_features, classification):
    config = configparser.ConfigParser()
    config.read('backend/weather/config.ini')
    future_period_predict = config.getint('LEARNING', 'FUTURE_PERIOD_PREDICT')
    history_period_size = config.getint('LEARNING', 'HISTORY_PERIOD_SIZE')

    # Scale
    pd.options.mode.chained_assignment = None  # disable false warning for copying

    x_transformer = RobustScaler()
    x_transformer = x_transformer.fit(processing[input_features].to_numpy())
    x_scaled = x_transformer.transform(processing[input_features].to_numpy())

    if classification:
        y_scaled = np_utils.to_categorical(processing[output_features].to_numpy())
    else:
        y_transformer = RobustScaler()
        y_transformer = y_transformer.fit(processing[output_features].to_numpy())
        y_scaled = y_transformer.transform(processing[output_features].to_numpy())

    # Shuffle
    sequential_data = []

    for i in range(len(x_scaled) - history_period_size - future_period_predict):
        sequential_data.append([
            x_scaled[i:(i + history_period_size)],
            y_scaled[i + history_period_size + future_period_predict - 1]
        ])

    random.shuffle(sequential_data)

    # Split
    x, y = [], []

    for seq, target in sequential_data:
        x.append(seq)
        y.append(target)

    return np.array(x), np.array(y)


def learn(station_code, input_features, output_features, classification=False):
    # Loading configuration
    config = configparser.ConfigParser()
    config.read('backend/weather/config.ini')
    processing_percentage = config.getint('APP', 'PROCESSING_PERCENTAGE')

    # Settings
    batch_size = 32
    epochs = 30
    rnn_layers = [1]
    rnn_node_sizes = [256]
    dense_layers = [1]
    dense_node_sizes = [128]

    # Prepare sequences and predictions
    records = pd.read_csv(f'data/processed/{station_code}_processed_{processing_percentage}.csv', sep=';', dtype=str)
    records.dropna(inplace=True)  # remove nulls just in case
    divider_index = int(len(records) * 0.8)
    training_records = records[:divider_index]
    validation_records = records[divider_index:]
    train_x, train_y = prepare(training_records, input_features, output_features, classification)
    validation_x, validation_y = prepare(validation_records, input_features, output_features, classification)

    # Modeling
    for dense_layer in dense_layers:
        for dense_node_index, dense_node_size in enumerate(dense_node_sizes):
            for rnn_layer in rnn_layers:
                for rnn_node_size in rnn_node_sizes:
                    if dense_node_index > 0 and dense_layer == 0:
                        continue

                    # name = f'{rnn_layer}-{rnn_node_size}-rnn-{dense_layer}-{dense_node_size}-dense'
                    # name = f'{name}-{processing_percentage}-proc-{future_period_predict}-fut-{history_period_size}-his'
                    # name = f'{name}-{batch_size}-batch-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")}'
                    classification_name = "wind_direction" if classification else "weather"
                    name = f'{station_code}_{classification_name}'

                    print(f'Current computation: {name}')

                    model = Sequential()

                    model.add(Bidirectional(LSTM(
                        rnn_node_size,
                        input_shape=(train_x.shape[1:]),
                        return_sequences=rnn_layer > 1)
                    ))
                    model.add(Dropout(0.2))

                    for layer in range(1, rnn_layer):
                        model.add(Bidirectional(LSTM(rnn_node_size, return_sequences=layer < rnn_layer - 1)))
                        model.add(Dropout(0.2))

                    for _ in range(dense_layer):
                        model.add(Dense(dense_node_size))
                        model.add(Dropout(0.2))

                    if classification:
                        model.add(Dense(train_y.shape[1], activation='softmax'))

                        model.compile(
                            loss='categorical_crossentropy',
                            optimizer=Adam(lr=0.001, decay=1e-6),
                            metrics=['accuracy']
                        )
                    else:
                        model.add(Dense(train_y.shape[1]))
                        model.compile(
                            loss='mean_squared_error',
                            optimizer=Adam(lr=0.001, decay=1e-6),
                            metrics=['accuracy']
                        )

                    checkpoint = ModelCheckpoint(
                        f'backend/weather/models/{name}.h5',
                        monitor='val_loss',
                        save_best_only=True,
                        mode='min'
                    )
                    log_dir = f'logs/{name}'
                    tensorboard = TensorBoard(log_dir=log_dir)

                    model.fit(
                        train_x, train_y,
                        batch_size=batch_size,
                        epochs=epochs,
                        validation_data=(validation_x, validation_y),
                        callbacks=[checkpoint, tensorboard]
                    )


if __name__ == '__main__':
    input_wind_features = ['Month', 'WindDirection', 'Humidity12']
    output_wind_features = ['WindDirection']
    learn('82331', input_wind_features, output_wind_features, classification=True)
