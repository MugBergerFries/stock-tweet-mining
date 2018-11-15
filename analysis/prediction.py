from pyspark import SparkConf, SparkContext
import json
import numpy as np
import tensorflow as tf

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
        pass 
        # batch learning, process a classifier per day. Classify only for data per day
        # inputs = tweets on particular day, outputs = predicted stock price on that day, or whether price will go up or down
