import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import model_from_json
import numpy as np


class predict:
    def __init__(self): # min, 25%, 50%, 75%, and max for sentiments on morn, noon, evening, general, and morn, noon, evening for exec
        self.model = keras.Sequential([
            keras.layers.Dense(9,activation='relu'), 
            keras.layers.Dense(5,activation='relu'),
            keras.layers.Dense(3) #,activation='relu'),
            # keras.layers.Dense(3)
        ])


    def calculate_covariance(self):
        #self.tweets.stat.cov('')
        pass
    
    def find_outliers(self):
        pass

    def neural_net(self):
        # format data to match training data

        '''
        self.model = keras.Sequential([
            keras.layers.Dense(9,activation='relu'),
            keras.layers.Dense(27,activation='relu'),
            keras.layers.Dense(72,activation='relu'),
            keras.layers.Dense(27,activation='relu'),
            keras.layers.Dense(9,activation='relu'),
            keras.layers.Dense(1)
        ])
        '''

        optimizer = tf.train.RMSPropOptimizer(0.01)

        self.model.compile(optimizer=optimizer,
              loss='mse', # classify for 0 or 1
              metrics=['mae'])  # get accuracy

        

        # model.fit(x: samples, y: labels) # labels are the stock differences (up or down) and the samples is the tweet data
        
        # Create training data -> inputs = bins of tweet sentiments (maybe also timestamps)
        #                       -> outputs = up or down, go through current stock data, get ups and downs
        
        # input data as vector, use binning
        # pass 
        # per unit time inputs?
        # batch learning, process a classifier per day. Classify only for data per day
        # inputs = tweets on particular day, outputs = predicted stock price on that day, or whether price will go up or down

    def train_network(self,train_tweets,train_stock):
        # tweets = np.array(train_tweets)
        # create array based on first 3 days, split the data into 1d array for every 3 days. Can also overlap days
        self.model.fit(train_tweets,train_stock,epochs=1000)

        # Save the model to model.json and model.h5
        model_json = self.model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.model.save_weights("model.h5")
        print("Saved model to disk")

    def load_network(self): # loads a network from saved files
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        # load weights into new model
        self.model.load_weights("model.h5")
        print("Loaded model from disk")
