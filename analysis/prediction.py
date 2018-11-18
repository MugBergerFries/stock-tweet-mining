import tensorflow as tf
from tensorflow import keras
import numpy as np


class predict:
    def __init__(self):
        self.model = keras.Sequential([
            keras.layers.Dense(9,activation='relu'),
            keras.layers.Dense(27,activation='relu'),
            keras.layers.Dense(72,activation='relu'),
            keras.layers.Dense(27,activation='relu'),
            keras.layers.Dense(9,activation='relu'),
            keras.layers.Dense(1)
        ])


    def calculate_covariance(self):
        #self.tweets.stat.cov('')
        
        #print("TWEET MEAN ISSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS {} AND STOCKS ARE {}".format(tweet_mean,stock_mean))
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

        optimizer = tf.train.RMSPropOptimizer(0.001)

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
        train_tweets = np.array([train_tweets.toPandas().values.flatten()])
        train_stocks = train_stock.toPandas()['diff'].values
        for i in range(len(train_stocks)):
            val = float(train_stocks[i])
            if(val < 0.5 and val > -0.5):
                val = 0
            elif(val > 0):
                val = 1
            else:
                val = -1
            train_stocks[i] = val

        self.model.fit(train_tweets,train_stocks,epochs=500)
