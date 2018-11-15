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
			return (tweet['timestamp_ms'].encode("ascii"),tweet['created_at'],tweet['geo'],tweet['id'],tweet['text'])
		else:
			return (-1,'','','','')
	#return (tweet['id'],tweet['text'])

def deconstruct(j):
	return j['statuses']


def sentiment_scan(sentiments,s):
	sSum = 0
	for i in sentiments.select['_c0']:
            #print(i)
            #print(s)
		if(i[0] in s[4]): # fix this to count number of times i[0] appears
			sSum += float(sentiments['_c1'])
	return [s,sSum] # works!



def assign_sentiment(sc,tweets,sentiments):
	filter_terms = ['a']
	# first get a list of tuples of text/ids from data
	# Applying map in the correct way may do the above ^
	# apply sentiment scans to the new mapped objects
	# collect the objects by reducing to a single list
	# file_json = file.map(lambda x: create_json(x))
	# file_filtered = file_json(lambda )
	# deconstructed = file_json.map(lambda x: deconstruct(x))
	# file_sanitized = file_json.map(lambda x: filter_json(x,filter_terms))
	# file_map = file_sanitized.toDF()
	#file_map = file_sanitized.map(lambda s: sentiment_scan(sentiments,s)) # replace with better snetiment calculations here
	# file_reduce = file_map.reduce(lambda x,y: x + y)
	text = tweets.select('text')
	text.udf(lambda x: sentiment_scan(x,sentiments))
	

	return file_map # returns sentiments for tweets relating to a certain subject and they're sentiments


def parse_stock_data(sc,stock_path):
	stock_file = sc.textFile("file://" + stock_path)
	stock_parsed = stock_file.map(lambda x: x.split(","))
	return stock_parsed



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

	p = predict(raw_data,stock_data)
	covariance = p.calculate_covariance()
	outliers = p.find_outliers()
	



