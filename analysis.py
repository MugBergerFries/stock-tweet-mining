from pyspark import SparkConf, SparkContext
import json


APP_NAME = "sentiment calculations"

def create_json(s):
	# newItemm['statuses'][0]['text']
	newJson = json.loads(s)
	return newJson

def filter_json(tweet): # filter json to only id and text
	if('text' in tweet):
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
	mapped_sents = sentiment.map(lambda s: s.split(",").encode("ascii"))
	#processed_sents = mapped_sents.reduce(lambda x,y: x + y)
	sents = mapped_sents.collect()

	file = sc.textFile("file://" + filepath)

	# first get a list of tuples of text/ids from data
	# Applying map in the correct way may do the above ^
	# apply sentiment scans to the new mapped objects
	# collect the objects by reducing to a single list
	file_json = file.map(lambda x: create_json(x))
	# file_filtered = file_json(lambda )
	# deconstructed = file_json.map(lambda x: deconstruct(x))
	file_sanitized = file_json.map(lambda x: filter_json(x))

	file_map = file_sanitized.map(lambda s: sentiment_scan(sents,s))
	# file_reduce = file_map.reduce(lambda x,y: x + y)
	return file_map.collect()


if __name__ == '__main__':
	conf = SparkConf().setAppName(APP_NAME)
	conf = conf.setMaster("192.168.56.101") # set to cluster master nodes hostname or ip address
	sc = SparkContext(conf=conf)

	filename = "/opt/output.json"
	sentiments = "/opt/sentiments.csv"

	assign_sentiment(sc,filename,sentiments)