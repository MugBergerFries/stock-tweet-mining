from pyspark import SparkConf, SparkContext
import json
import numpy as np
import tensorflow as tf
from tensorflow import keras


class predict:
    def __init__(self,tweet_data,stock_data):
        self.tweets = tweet_data
        self.stocks = stock_data


    def calculate_covariance(self):
        #self.tweets.stat.cov('')
        
        #print("TWEET MEAN ISSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS {} AND STOCKS ARE {}".format(tweet_mean,stock_mean))
        pass
    
    def find_outliers(self):
        pass

    def neural_net(self):
        model = keras.Sequential([
            keras.layers.Dense(30,activation='relu'),
            keras.layers.Dense(20,activation='relu'),
            keras.layers.Dense(10,activation='relu'),
            keras.layers.Dense(1)
        ])

        model.compile(optimizer=tf.train.AdamOptimizer(0.01),
              loss='mse',       # mean squared error
              metrics=['mae'])  # mean absolute error
        
        # input data as vector, use binning
        # pass 
        # per unit time inputs?
        # batch learning, process a classifier per day. Classify only for data per day
        # inputs = tweets on particular day, outputs = predicted stock price on that day, or whether price will go up or down
