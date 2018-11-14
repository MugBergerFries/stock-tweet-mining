from pyspark import SparkConf, SparkContext
import json
from prediction import *


APP_NAME = "sentiment calculations"

def create_json(s):
	# newItemm['statuses'][0]['text']
	newJson = json.loads(s)
	return newJson



def filter_json(tweet,filter_terms): # filter json to only id and text
	for x in filter_terms:
		if(x in tweet and 'text' in tweet):
			return (tweet['timestamp_ms'],tweet['created_at'],tweet['geo'],tweet['id'],tweet['text'])
		else:
			return ('-1','','','','')
	#return (tweet['id'],tweet['text'])

def deconstruct(j):
	return j['statuses']


def sentiment_scan(sentiments,s):
	sSum = 0
	for i in sentiments:
		if(i[0] in s[1]): # fix this to count number of times i[0] appears
			sSum += float(i[1])
	return [i[0],sSum] # works!



def assign_sentiment(sc,filepath,sentiments):
	sentiment = sc.textFile("file://" + sentiments)
	mapped_sents = sentiment.map(lambda s: s.split(","))
	#processed_sents = mapped_sents.reduce(lambda x,y: x + y)
	sents = mapped_sents.collect()

	file = sc.textFile("file://" + filepath)
	filter_terms = ['apple','Apple','tim cook','Tim Cook','tim_cook','Tim_Cook']

	# first get a list of tuples of text/ids from data
	# Applying map in the correct way may do the above ^
	# apply sentiment scans to the new mapped objects
	# collect the objects by reducing to a single list
	file_json = file.map(lambda x: create_json(x))
	# file_filtered = file_json(lambda )
	# deconstructed = file_json.map(lambda x: deconstruct(x))
	file_sanitized = file_json.map(lambda x: filter_json(x,filter_terms))

	file_map = file_sanitized.map(lambda s: sentiment_scan(sents,s)) # replace with better snetiment calculations here
	# file_reduce = file_map.reduce(lambda x,y: x + y)
	return file_map # returns sentiments for tweets relating to a certain subject and they're sentiments


def parse_stock_data(sc,stock_path):
	stock_file = sc.file("file://" + stock_path)
	stock_parsed = stock_file.map(lambda x: x.split(","))
	return stock_parsed



if __name__ == '__main__':
	conf = SparkConf().setAppName(APP_NAME)
	conf = conf.setMaster("192.168.56.101") # set to cluster master nodes hostname or ip address
	sc = SparkContext(conf=conf)

	filename = "/opt/output.json"
	sentiments = "/opt/sentiments.csv"
	stocks = "/opt/stock.json"

	stock_data = parse_stock_data(sc,stocks)
	raw_data = assign_sentiment(sc,filename,sentiments)

	p = predict(data,stock_data)
	covariance = p.calculate_covariance()
	outliers = p.find_outliers()
	



