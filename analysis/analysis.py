from pyspark.sql import SparkSession
import json
from prediction import *
import pandas as pd
import numpy as np


APP_NAME = "Social Media as an Economic Indicator"


def sentiment_scan(sentiments,s): # define this as a udf, than put it inside a withColumn statement
	acc = float(0) 
	for word in sentiments['word']:
		#print(acc)
		if(str(word).encode('utf-8') in s.encode('utf-8')):
			value = sentiments.loc[sentiments['word'] == word,'value']
			acc += float(value)
	return [acc]


def assign_sentiment(sc,tweets,sentiments):
	tweets = tweets.filter(tweets.text.contains('apple') | tweets.text.contains('Apple') | tweets.text.contains('tim cook') | tweets.text.contains('Tim Cook'))
	dfSent = tweets.rdd.map(lambda x: sentiment_scan(sentiments,x.text)).toDF().selectExpr("_1 as sentiments")
	return tweets.join(dfSent)
	

def get_stock_labels(stock_data):
	stocks = stock_data.selectExpr("_c0 as date","_c1 as close","_c2 as volume","_c3 as open","_c4 as high","_c5 as low")
	diff = stocks.withColumn('diff',stocks.close - stocks.open)
	return diff.filter(diff.date.rlike('2015/12/*'))

def bin_tweets(tweets):
	bins = [0,0,0,0,0,0,0,0,0,0]
	count = -1
	for i in range(10):
		bin = tweets.filter(tweets.sentiments > count).filter(tweets.sentiments < count + 0.2)
		bins[i] = bin.count()
		count += 0.2
	return bins


if __name__ == '__main__':
#	conf = SparkConf().setAppName(APP_NAME)
#	conf = conf.setMaster("localhost") # set to cluster master nodes hostname or ip address
#	sc = SparkContext(conf=conf)
	
	spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
	sc = spark.sparkContext
	filename = "/opt/output.json"
	sentiments = "/opt/sentiments.csv"
	stocks = "/opt/stock.csv"

	sentiment = pd.read_csv(sentiments) # spark.read.csv("file://" + sentiments)

	stock_data = spark.read.csv("file://" + stocks) # parse_stock_data(sc,stocks)
	tweet_data = spark.read.json("file://" + filename)
	raw_data = assign_sentiment(sc,tweet_data,sentiment)

	labels = get_stock_labels(stock_data)
	tweet_bins = bin_tweets(raw_data)

	p = predict()
	p.neural_net()
	for i in range(31): # loop through every day and update neural network based on new data
		# filter tweet data based on day here
		# filter stock data based on day here
		p.train_network(tweet_bins,labels) # apply new filtered data for stocks and tweets here
	# run tests on data that has been set aside for testing here

	

	
	
	



