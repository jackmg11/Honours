## Machine learning code adapted from https://github.com/rohan-paul/MachineLearning-DeepLearning-Code-for-my-YouTube-Channel/blob/master/Finance_Stock_Crypto_Trading/Bitcoin_Price_Prediction_with_LSTM.ipynb




import warnings

from pip import main
#warnings.filterwarnings('ignore')
import os
import pandas as pd
import numpy as np
import math
import datetime as dt
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score, r2_score 
from sklearn.metrics import mean_poisson_deviance, mean_gamma_deviance, accuracy_score
from sklearn.preprocessing import MinMaxScaler

from itertools import product
import statsmodels.api as sm

import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import LSTM
from sklearn.metrics import mean_absolute_error
from itertools import cycle
import plotly.offline as py
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def LSTMFunc(coin):
    plt.style.use('seaborn-darkgrid')

    # btc_input_df = pd.read_csv(root_path, nrows=500)
    btc_input_df = pd.read_csv(f"ApiCryptoData{coin}.csv")
    btc_input_df.tail()

    btc_input_df.shape

    btc_input_df.describe()

    btc_input_df.info()

    btc_input_df_datetype = btc_input_df.astype({'RealTime': 'datetime64'})

    btc_input_df_datetype.info()

    #btc_input_df_datetype.set_index("RealTime").close.plot(figsize=(24,7), title="Bitcoin Weighted Price")





    btc_input_df_datetype['date'] = pd.to_datetime(btc_input_df_datetype['time'],unit='s').dt.date



    group = btc_input_df_datetype.groupby('date')

    btc_closing_price_groupby_date = group['close'].mean()



    print("Length of btc_closing_price_groupby_date :", len(btc_closing_price_groupby_date))

    prediction_days = 60

    # Set Train data to be uplo ( Total data length - prediction_days )
    df_train= btc_closing_price_groupby_date[:len(btc_closing_price_groupby_date)-prediction_days].values.reshape(-1,1)
    
    print(df_train)
    # Set Test data to be the last prediction_days (or 60 days in this case)
    df_test= btc_closing_price_groupby_date[len(btc_closing_price_groupby_date)-prediction_days:].values.reshape(-1,1)

    df_test.shape

    chosen_col = 'close'

    #fig, ax = plt.subplots(1, figsize=(13, 7))
    #ax.plot(df_train, label='Train', linewidth=2)
    #ax.plot(df_test, label='Test', linewidth=2)
    #ax.set_ylabel('Price USD', fontsize=14)
    #ax.set_title('', fontsize=16)
    #ax.legend(loc='best', fontsize=16)

    scaler_train = MinMaxScaler(feature_range=(0, 1))
    scaled_train = scaler_train.fit_transform(df_train)

    scaler_test = MinMaxScaler(feature_range=(0, 1))
    scaled_test = scaler_test.fit_transform(df_test)

    def dataset_generator_lstm(dataset, look_back=7):
        # A “lookback period” defines the window-size of how many
        # previous timesteps are used in order to predict
        # the subsequent timestep. 
        dataX, dataY = [], []
        
        for i in range(len(dataset) - look_back):
            window_size_x = dataset[i:(i + look_back), 0]
            dataX.append(window_size_x)
            dataY.append(dataset[i + look_back, 0]) # this is the label or actual y-value
        return np.array(dataX), np.array(dataY)

    trainX, trainY = dataset_generator_lstm(scaled_train)

    testX, testY = dataset_generator_lstm(scaled_test)

    print("trainX: ", trainX.shape)
    print("trainY: ", trainY.shape)
    print("testX: ", testX.shape)
    print("testY", testY.shape)

    print("trainX: ", trainX)
    # print("trainY: ", trainY)
    # print("testY: ", testX)
    # print("testY", testY)

    trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))

    testX = np.reshape(testX, (testX.shape[0], testX.shape[1], 1 ))

    print("Shape of trainX: ", trainX.shape)
    print("Shape of testX: ", testX.shape)

    print("trainX: ", trainX)
    print(" ********** ")
    print("testX: ", testX)

    # First checking the values for input_shape = (trainX.shape[1], trainX.shape[2])
    # Note - `input_shape` of LSTM Model - `input_shape` is supposed to be (timesteps, n_features).

    print("trainX.shape[1] - i.e. timesteps in input_shape = (timesteps, n_features) ", trainX.shape[1])
    print("trainX.shape[2] - i.e. n_features in input_shape = (timesteps, n_features) ", trainX.shape[2])

    regressor = Sequential()

    # Adding the first LSTM layer and some Dropout regularisation
    # You must set return_sequences=True when stacking LSTM layers so that the second LSTM layer
    # has a compatible n-dimensional sequence input.
    # This hyper parameter should be set to False (which is the default value) for the last layer
    # and true for the other previous layers.

    regressor.add(LSTM(units = 128, activation = 'relu',return_sequences=True, input_shape = (trainX.shape[1], trainX.shape[2])))
    regressor.add(Dropout(0.2))

    # Adding a second LSTM layer and some Dropout regularisation
    regressor.add(LSTM(units = 64, input_shape = (trainX.shape[1], trainX.shape[2])))
    # regressor.add(LSTM(units = 64, return_sequences = True, input_shape = (trainX.shape[1], trainX.shape[2])))
    regressor.add(Dropout(0.2))
    # Note - If I plan to add 3-rd or 4-th layers of LSTM then 
    # I must set return_sequences=True in the 2-nd layer above
    # so that the 3-rd LSTM layer has a compatible n-dimensional sequence input.


    # Adding a third LSTM layer and some Dropout regularisation
    # regressor.add(LSTM(units = 64, return_sequences = True, input_shape = (trainX.shape[1], trainX.shape[2])))
    # regressor.add(Dropout(0.2))


    # Adding a fourth LSTM layer and some Dropout regularisation
    # regressor.add(LSTM(units = 64, input_shape = (trainX.shape[1], trainX.shape[2])))
    # regressor.add(Dropout(0.2))


    # Adding the output layer
    regressor.add(Dense(units = 1))

    regressor.summary()

    from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

    # Compiling the LSTM
    regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

    checkpoint_path = 'my_best_model.hdf5'

    checkpoint = ModelCheckpoint(filepath=checkpoint_path, 
                                monitor='val_loss',
                                verbose=1, 
                                save_best_only=True,
                                mode='min')


    earlystopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    callbacks = [checkpoint, earlystopping]
    # callbacks = [checkpoint]


    history = regressor.fit(trainX, trainY, batch_size = 16, epochs = 100, verbose=1, shuffle=False, validation_data=(testX, testY), callbacks=callbacks)

    from tensorflow.keras.models import load_model

    model_from_saved_checkpoint = load_model(checkpoint_path)

    #plt.figure(figsize=(16,7))
    #plt.plot(history.history['loss'], label='train')

   # plt.plot(history.history['val_loss'], label='test')
    #plt.legend()
    #plt.show()

    # Transformation to original form and making the predictions

    # predicted_btc_price_test_data = regressor.predict(testX)
    predicted_btc_price_test_data = model_from_saved_checkpoint.predict(testX)

    predicted_btc_price_test_data = scaler_test.inverse_transform(predicted_btc_price_test_data.reshape(-1, 1))

    test_actual = scaler_test.inverse_transform(testY.reshape(-1, 1))





    #plt.figure(figsize=(16,7))

    #plt.plot(predicted_btc_price_test_data, 'r', marker='.', label='Predicted Test')

    #plt.plot(test_actual, marker='.', label='Actual Test')

    #plt.legend()
    #plt.show()

    predicted_btc_price_train_data = model_from_saved_checkpoint.predict(trainX)

    predicted_btc_price_train_data = scaler_train.inverse_transform(predicted_btc_price_train_data.reshape(-1, 1))

    train_actual = scaler_train.inverse_transform(trainY.reshape(-1, 1))

    #plt.figure(figsize=(16,7))

    #plt.plot(predicted_btc_price_train_data, 'r', marker='.', label='Predicted Train')

    #plt.plot(train_actual, marker='.', label='Actual Train')

    #plt.legend()
    #plt.show()

    rmse_lstm_test = math.sqrt(mean_squared_error(test_actual, predicted_btc_price_test_data))

    print('Test RMSE: %.3f' % rmse_lstm_test)

    

    rmse_lstm_train = math.sqrt(mean_squared_error(train_actual, predicted_btc_price_train_data))

    print('Train RMSE: %.3f' % rmse_lstm_train)

    #mape = mean_absolute_error((test_actual - predicted_btc_price_test_data / test_actual))*100
    #print(mape)
   

    testX
    testX.shape

    lookback_period = 7

   

    testX_last_7_days = testX[testX.shape[0] - lookback_period :  ]

    testX_last_7_days.shape



    testX_last_7_days

    predicted_7_days_forecast_price_test_x = []

    for i in range(7):  
        predicted_forecast_price_test_x = model_from_saved_checkpoint.predict(testX_last_7_days[i:i+1])
    
        predicted_forecast_price_test_x = scaler_test.inverse_transform(predicted_forecast_price_test_x.reshape(-1, 1))
    # print(predicted_forecast_price_test_x)
        predicted_7_days_forecast_price_test_x.append(predicted_forecast_price_test_x)
    
    print("Forecast for the next 7 Days Beyond the actual trading days ", np.array(predicted_7_days_forecast_price_test_x)) 
    

    predicted_7_days_forecast_price_test_x = np.array(predicted_7_days_forecast_price_test_x)

    predicted_7_days_forecast_price_test_x.shape

    predicted_btc_price_test_data.shape

    predicted_btc_price_test_data

    predicted_7_days_forecast_price_test_x

    predicted_7_days_forecast_price_test_x = predicted_7_days_forecast_price_test_x.flatten()

    predicted_7_days_forecast_price_test_x

    predicted_btc_price_test_data = predicted_btc_price_test_data.flatten()

    predicted_btc_price_test_data

    predicted_btc_test_concatenated = np.concatenate((predicted_btc_price_test_data, predicted_7_days_forecast_price_test_x))

    predicted_btc_test_concatenated

    predicted_btc_test_concatenated.shape

    plt.figure(figsize=(16,7))

    plt.plot(predicted_btc_test_concatenated, 'r', marker='.', label='Predicted Test')

    plt.plot(test_actual, marker='.', label='Actual Test')

    plt.legend()

    plt.show()

    predicted_btc_test_concatenated
    

    return predicted_7_days_forecast_price_test_x[-1]

    

    
if __name__=="__main__":
    
    LSTMFunc("BTC")