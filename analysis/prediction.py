from pyspark import SparkConf, SparkContext
import json
import numpy as np
import pandas as pd

class predict:
    def __init__(self,tweet_data,stock_data):
        self.tweets = tweet_data
        self.stocks = stock_data

    def covariance_eq(dataPt):
        pass

    def calculate_covariance(self):
        values = self.tweets.map(lambda x: x[1])
        tweet_mean = values.mean()
        print("TWEET MEAN ISSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS " +str(tweet_mean))
    
    def find_outliers(self):
        pass

    def neural_net(self):
        pass
