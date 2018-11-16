from pyspark.sql import SparkSession
import json
from prediction import *


APP_NAME = "sentiment calculations"

def create_json(s):
	# newItemm['statuses'][0]['text']
	newJson = json.loads(s)
	return newJson



def filter_json(tweet,filter_terms): # filter json to only id and text
	for x in filter_terms:
		if('text' in tweet):
			return (tweet['timestamp_ms'],tweet['created_at'],tweet['geo'],tweet['id'],tweet['text'])
		else:
			return (-1,'','','','')
	#return (tweet['id'],tweet['text'])

def deconstruct(j):
	return j['statuses']


def sentiment_scan(sentiments,s):
	words = s.split(' ') 




def assign_sentiment(sc,tweets,sentiments):
	#filter_terms = ['a']
	# first get a list of tuples of text/ids from data
	# Applying map in the correct way may do the above ^
	# apply sentiment scans to the new mapped objects
	# collect the objects by reducing to a single list
	# file_json = file.map(lambda x: create_json(x))
	# file_filtered = file_json(lambda )
	# deconstructed = file_json.map(lambda x: deconstruct(x))
	# file_sanitized = file_json.map(lambda x: filter_json(x,filter_terms))
	# file_map = file_sanitized.toDF()
	# file_map = file_sanitized.map(lambda s: sentiment_scan(sentiments,s)) # replace with better snetiment calculations here
	# file_reduce = file_map.reduce(lambda x,y: x + y)
	text = tweets.withColumn('text',tweets.lower)
	text.udf(lambda x: sentiment_scan(x,sentiments))
	

	return text # returns sentiments for tweets relating to a certain subject and they're sentiments

def get_stock_labels(stock_data):
	stocks = stock_data.selectExpr("_c0 as date","_c1 as close","_c2 as volume","_c3 as open","_c4 as high","_c5 as low")
	diff = stocks.withColumn('diff',stocks.close - stocks.open)
	return diff.filter(diff.date.rlike('2015/12/*'))


if __name__ == '__main__':
#	conf = SparkConf().setAppName(APP_NAME)
#	conf = conf.setMaster("localhost") # set to cluster master nodes hostname or ip address
#	sc = SparkContext(conf=conf)
	
	spark = SparkSession.builder.appName("APP_NAME").getOrCreate()
	sc = spark.sparkContext
	filename = "/opt/output.json"
	sentiments = "/opt/sentiments.csv"
	stocks = "/opt/stock.csv"

	sentiment = spark.read.csv("file://" + sentiments)

	stock_data = spark.read.csv("file://" + stocks) # parse_stock_data(sc,stocks)
	tweet_data = spark.read.json("file://" + filename)
	raw_data = assign_sentiment(sc,filename,sentiment)

	labels = get_stock_labels(stock_data)

	p = predict(raw_data,labels)
	



