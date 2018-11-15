from pyspark import SparkConf, SparkContext
import json
import numpy as np
import tensorflow as tf

class predict:
    def __init__(self,tweet_data,stock_data):
        self.tweets = tweet_data
        self.stocks = stock_data



    def calculate_covariance(self):
        values = self.tweets.map(lambda x: x[1])
        tweet_mean = values.mean()
        stock_diff = self.stocks.map(lambda x: x['close'] - x['open'])
        stock_mean = stock_diff.mean()
        
        print("TWEET MEAN ISSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS {} AND STOCKS ARE {}".format(tweet_mean,stock_mean))
    
    def find_outliers(self):
        pass

    def neural_net(self):
        pass 
        # batch learning, process a classifier per day. Classify only for data per day
        # inputs = tweets on particular day, outputs = predicted stock price on that day, or whether price will go up or down
