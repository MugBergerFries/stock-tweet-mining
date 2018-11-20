from pyspark.sql import SparkSession
# from pyspark.sql.functions import avg
# import json
from prediction import *
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil import parser


APP_NAME = "Social Media as an Economic Indicator"


def sentiment_scan(sentiments,s): # define this as a udf, than put it inside a withColumn statement
	acc = float(0) 
	for word in sentiments['word']:
		#print(acc)
		if(str(word).encode('utf-8') in s.encode('utf-8')):
			value = sentiments.loc[sentiments['word'] == word,'value']
			acc += float(value)
	return [acc]

def split_by_day(data,filter_days):
	# time = datetime.strptime(data['created_at'])
	# returns an array, where one side is sentiment for day1, next for day2, third for day3
	# sentiment calculated in this functi
	in_form = "%b %d %X %z %Y" # limit_unixtime = time.mktime(filter_days[0].timetuple())

	day1 = data.rdd.filter(lambda t: parser.parse(t['created_at']).strftime('%Y-%m-%d') == filter_days[0]) # datetime.strptime(data.created_at,in_form).strftime('%Y-%m-%d') == filter_days[0]) # Tue Dec 29 08:00:00 +0000 2015
	day2 = data.rdd.filter(lambda t: parser.parse(t['created_at']).strftime('%Y-%m-%d') == filter_days[1]) # may not work!!!!!
	day3 = data.rdd.filter(lambda t: parser.parse(t['created_at']).strftime('%Y-%m-%d') == filter_days[2])

	if(day1.isEmpty()):
		out1 = 0
	else:
		df1 = day1.map(lambda x: sentiment_scan(sentiments,x.text)).toDF().selectExpr("_1 as sentiments").toPandas()
		out1 = df1['sentiments'].mean()
	
	if(day2.isEmpty()):
		out2 = 0
	else:
		df2 = day2.map(lambda x: sentiment_scan(sentiments,x.text)).toDF().selectExpr("_1 as sentiments").toPandas()
		out2 = df2['sentiments'].mean()

	if(day3.isEmpty()):
		out3 = 0
	else:
		df3 = day3.map(lambda x: sentiment_scan(sentiments,x.text)).toDF().selectExpr("_1 as sentiments").toPandas()
		out3 = df3['sentiments'].mean()

	
	return [out1,out2,out3]


def assign_sentiment(sc,tweets,sentiments,days):
	tweets = tweets.filter(tweets.user['screen_name'].contains('tim_cook') | tweets.text.contains('apple') | tweets.text.contains('Apple') | tweets.text.contains('tim cook') | tweets.text.contains('Tim Cook'))
	execs = tweets.filter(tweets.user['screen_name'].contains('tim_cook'))
	generalPublic = tweets.filter(~tweets.user['screen_name'].contains('tim_cook'))
	training_data = []
	for i in range(len(days)-2):
		execSplit = split_by_day(execs,days[i:i+3])
		tweetSplit = split_by_day(generalPublic,days[i:i+3])
		# tweetSplit2 = split_by_day(generalPublic,days[i:im+3])
		training_data.append([execSplit + tweetSplit + tweetSplit])	
	# dfGeneral = tweets.rdd.map(lambda x: sentiment_scan(sentiments,x.text)).toDF().selectExpr("_1 as sentiments")
	return training_data
	

def get_stock_labels(stock_data):
	stocks = stock_data.selectExpr("_c0 as date","_c1 as close","_c2 as volume","_c3 as open","_c4 as high","_c5 as low")
	diff = stocks.withColumn('diff',stocks.close - stocks.open)
	return diff.filter(diff.date.rlike('2015/12/*'))

def bin_tweets(tweets):
	bins = np.array([0,0,0,0,0,0,0,0,0,0])
	count = -1
	for i in range(10):
		bin = tweets.filter(tweets.sentiments > count).filter(tweets.sentiments < count + 0.2)
		bins[i] = bin.count()
		count += 0.2
	return bins

#def 


if __name__ == '__main__':
#	conf = SparkConf().setAppName(APP_NAME)
#	conf = conf.setMaster("localhost") # set to cluster master nodes hostname or ip address
#	sc = SparkContext(conf=conf)
	
	spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
	sc = spark.sparkContext
	filename = "/opt/output.json"
	sentiments = "/opt/sentiments.csv"
	stocks = "/opt/stock.csv"
	days = ['2015-12-1','2015-12-2','2015-12-3','2015-12-4','2015-12-7','2015-12-8','2015-12-9','2015-12-10','2015-12-11','2015-12-14','2015-12-15',
	'2015-12-16','2015-12-17','2015-12-18','2015-12-21','2015-12-22','2015-12-23','2015-12-24','2015-12-28','2015-12-29','2015-12-30','2015-12-31']

	sentiment = pd.read_csv(sentiments) # spark.read.csv("file://" + sentiments)

	stock_data = spark.read.csv("file://" + stocks) # parse_stock_data(sc,stocks)
	tweet_data = spark.read.json("file://" + filename)
	train_tweets = assign_sentiment(sc,tweet_data,sentiment,days)

	labels = get_stock_labels(stock_data)
	#tweet_bins = bin_tweets(raw_data)

	# train_tweets = np.array([raw_data.toPandas().values.flatten()])
	raw_stocks = labels.toPandas()['diff'].values
	train_stocks = []
	for i in range(len(raw_stocks)):
		val = float(raw_stocks[i])
		if(val < 0.2 and val > -0.2):
			raw_stocks[i] = 0
		elif(val > 0):
			raw_stocks[i] = 1
		else:
			raw_stocks[i] = -1
	
	for i in range(len(raw_stocks)-2):
		train_stocks.append([raw_stocks[i],raw_stocks[i+1],raw_stocks[i+2]])

	p = predict()
	p.neural_net()
	for i in range(31): # loop through every day and update neural network based on new data
		# filter tweet data based on day here
		# filter stock data based on day here
		p.train_network(np.array(train_tweets),np.array(train_stocks)) # apply new filtered data for stocks and tweets here
	# run tests on data that has been set aside for testing here
