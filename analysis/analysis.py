from pyspark.sql import SparkSession
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

#def test_func(t):
#	val = parser.parse(t['created_at'])
#	val1 = val.strftime('%Y-%m-%d')
#	return val1

def split_by_day(data,sentiments,filter_days):
	# time = datetime.strptime(data['created_at'])
	# returns an array, where one side is sentiment for day1, next for day2, third for day3
	# in_form = "%b %d %X %z %Y" # limit_unixtime = time.mktime(filter_days[0].timetuple())
	print("Filter days are: {}, {} and {}".format(filter_days[0],filter_days[1],filter_days[2]))
#	test = data.rdd.map(lambda t: test_func(t))
#	out = test.collect()
#	print("OUT IS: {}".format(out))
	day1 = data.rdd.filter(lambda t: parser.parse(t['created_at']).strftime('%Y-%m-%d') == filter_days[0]) # datetime.strptime(data.created_at,in_form).strftime('%Y-%m-%d') == filter_days[0]) # Tue Dec 29 08:00:00 +0000 2015
	day2 = data.rdd.filter(lambda t: parser.parse(t['created_at']).strftime('%Y-%m-%d') == filter_days[1]) 
	day3 = data.rdd.filter(lambda t: parser.parse(t['created_at']).strftime('%Y-%m-%d') == filter_days[2])

	if(day1.isEmpty()): # if the values are empty, there are no tweets for that day, neutralize
		out1 = 0
	else:
		df1 = day1.map(lambda x: sentiment_scan(sentiments,x.text)).toDF().selectExpr("_1 as sentiments").toPandas()
		out1 = df1['sentiments'].mean() # if there are tweets, get sentiment and get the average of all sentiment
	
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


def assign_sentiment(sc,tweets,sentiments,days): # getting data for apple and tim cook currently
	tweets = tweets.filter(tweets.user['screen_name'].contains('tim_cook') | tweets.text.contains('apple') | tweets.text.contains('Apple') | tweets.text.contains('tim cook') | tweets.text.contains('Tim Cook'))
	execs = tweets.filter(tweets.user['screen_name'].contains('tim_cook'))
	generalPublic = tweets.filter(~tweets.user['screen_name'].contains('tim_cook'))
	training_data = []
	for i in range(len(days)-5):
		print("Getting executive tweets")
		execSplit = split_by_day(execs,sentiments,days[i:i+3])
		print("Getting general tweets")
		tweetSplit = split_by_day(generalPublic,sentiments,days[i:i+3])
		# print(tweetSplit)
		# tweetSplit2 = split_by_day(generalPublic,days[i:im+3])
		# for i in range(len(tweetSplit)/2):
		# sample1 = np.random.choice(tweetSplit,size=len(tweetSplit),replace=False).tolist()
		# sample2 = np.random.choice(tweetSplit,size=len(tweetSplit),replace=False).tolist()
		training_data.append([execSplit + tweetSplit + tweetSplit])
	# dfGeneral = tweets.rdd.map(lambda x: sentiment_scan(sentiments,x.text)).toDF().selectExpr("_1 as sentiments")
	return training_data

def normalize_stocks(stocks): # normilizes stock differences into up, down or stright
	# print("STOCKS ARE {}".format(stocks))
	for i in range(len(stocks)):
		val = float(stocks[i])
		if(val < 0.2 and val > -0.2):
			stocks[i] = 0
		elif(val > 0):
			stocks[i] = 1
		else:
			stocks[i] = -1
	return stocks

def split_stocks(data,filter_days): # Orginize stock data into arrays able to be read by neural network
	#print(data.rdd.map(lambda t: t[0]).collect())

	data = data.rdd.filter(lambda t: t[0] != 'date') # kinda slow, but makes life way easier
	# print(data.map(lambda t: parse_date_stock(t)).collect())
	# print(filter_days)

	day1 = data.filter(lambda t: parser.parse(t['date']).strftime('%Y-%m-%d') == filter_days[0]) # datetime.strptime(data.created_at,in_form).strftime('%Y-%m-%d') == filter_days[0]) # Tue Dec 29 08:00:00 +0000 2015
	day2 = data.filter(lambda t: parser.parse(t['date']).strftime('%Y-%m-%d') == filter_days[1])
	day3 = data.filter(lambda t: parser.parse(t['date']).strftime('%Y-%m-%d') == filter_days[2])

	out1 = day1.toDF().toPandas()['diff'].values
	out2 = day2.toDF().toPandas()['diff'].values
	out3 = day3.toDF().toPandas()['diff'].values

	return normalize_stocks([out1,out2,out3])


def get_stock_labels(stock_data):
	stocks = stock_data.selectExpr("_c0 as date","_c1 as close","_c2 as volume","_c3 as open","_c4 as high","_c5 as low")
	diff = stocks.withColumn('diff',stocks.close - stocks.open)
	return diff


def filter_stocks(stocks,days):
	#raw_stocks = labels.toPandas()['diff'].values # This is wrong, filter by the list given
	#print(raw_stocks)
	train_stocks = []
	for i in range(3,len(days)-2): # get all stock values that occur in the 3 days after tweet values
		stock_split = split_stocks(stocks,days)
		train_stocks.append(stock_split)
		#print(train_stocks)
	return train_stocks


if __name__ == '__main__':
#	conf = SparkConf().setAppName(APP_NAME)
#	conf = conf.setMaster("localhost") # set to cluster master nodes hostname or ip address
#	sc = SparkContext(conf=conf)
	
	spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
	sc = spark.sparkContext
	sc.setLogLevel("WARN") # less verbose

	filename = "/opt/output.json"
	sentiments = "/opt/sentiments.csv"
	stocks = "/opt/stock.csv"
	days2015 = ['2015-12-29','2015-12-02','2015-12-03','2015-12-04','2015-12-07','2015-12-08','2015-12-09','2015-12-10','2015-12-11','2015-12-14','2015-12-15',
	'2015-12-16','2015-12-17','2015-12-18','2015-12-21','2015-12-22','2015-12-23','2015-12-24','2015-12-28','2015-12-29','2015-12-30','2015-12-31']

	days2018 = ['2018-04-01']

	sentiment = pd.read_csv(sentiments) # spark.read.csv("file://" + sentiments)

	stock_data = spark.read.csv("file://" + stocks) # parse_stock_data(sc,stocks)
	tweet_data = spark.read.json("file://" + filename)
	train_tweets = assign_sentiment(sc,tweet_data,sentiment,days2015)

	labels = get_stock_labels(stock_data) # calculates the difference field for stock dataframe
	
	train_stocks = filter_stocks(labels,days2015) # filter stocks by date
	print("Training outputs (stock data) are {}".format(train_stocks))
	print("Training inputs (tweet data) are {}".format(train_tweets))

	with open("neural_network/training_stock_data.dat",'w') as f: # 
		for i in train_stocks:
			for j in i:
				f.write(str(j) + ",")
			f.write('\n')
	with open("neural_network/training_tweet_data.dat",'w') as f:
		for i in train_tweets:
			for j in i:
				f.write(str(j) + ",")
			f.write('\n')

	p = predict() # create prediction object
	p.neural_net() # build neural net
	#for i in range(31): # loop through every day and update neural network based on new data
		# filter tweet data based on day here
		# filter stock data based on day here
	p.train_network(np.array(train_tweets),np.array(train_stocks)) # train neural net on tweets and stock data
	# run tests on data that has been set aside for testing here


	#tweet_bins = bin_tweets(raw_data)

	# train_tweets = np.array([raw_data.toPandas().values.flatten()])
	#raw_stocks = labels.toPandas()['diff'].values # This is wrong, filter by the list given
	#train_stocks = []
	#for i in range(len(raw_stocks)):
	#	val = float(raw_stocks[i])
	#	if(val < 0.2 and val > -0.2):
	#		raw_stocks[i] = 0
	#	elif(val > 0):
	#		raw_stocks[i] = 1
	#	else:
	#		raw_stocks[i] = -1
	
	#for i in range(4,len(days2015)-2):
	#	train_stocks.append([raw_stocks[i],raw_stocks[i+1],raw_stocks[i+2]])
