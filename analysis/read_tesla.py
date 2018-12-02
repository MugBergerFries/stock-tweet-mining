from prediction import *
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil import parser
from datetime import datetime, timedelta



def normalize_stocks(val): # normilizes stock differences into up, down or stright
	# print("STOCKS ARE {}".format(stocks))
	#for i in range(len(stocks)):
	#	val = float(stocks[i])
    stocks = 0
    if(val > 0):
        stocks = 1
    else:
        stocks = 0
    return stocks

# get the date for elon musk tweets, go back 3 days, and see what his tweets are back than
# go forward 3 days and see what stock trend is.
# for testing try predicting stock trend based on last 3 days of elon musk tweets

def sum_for_day(tweets):
    newTweets = {}
    for i in range(len(tweets)):
        date = parser.parse(tweets['date'][i]).strftime('%Y-%m-%d')
        if(date not in newTweets.keys()):
            newTweets[date] = tweets['sentiment'][i]
        else:
            newTweets[date] += tweets['sentiment'][i]
    # print(newTweets
    s = pd.Series(newTweets, name='value')
    s.index.name = 'date'
    return s.reset_index()
    # return pd.DataFrame(newTweets.items(), columns=['date', 'value'])

def week_lookback(current,tweets):
    output = []
    for i in range(7):
        newDate = (parser.parse(current) - timedelta(days=i)).strftime('%Y-%m-%d')
        filtered = tweets.loc[tweets['date'] == newDate]['value']
        if(not filtered.empty):
            output.insert(0,filtered.tolist()[0])
        else:
            output.insert(0,0)
    return output

def stock_lookforward(current,stocks):
    output = []
    current = parser.parse(current)
    start = 0
    for i in range(len(stocks)):
        if(parser.parse(stocks['date'][i]) == current):
            start = i
            break
    for i in range(start,start+5):
        prediction = normalize_stocks(stocks['close'][i] - stocks['open'][i])
        output.append(prediction)
    return output

dfTweets = pd.read_csv('./sentimentsNewerHalf.csv')
dfStocks = pd.read_csv('./StockData/HistoricalQuotesTSLA.csv')
dfTest = pd.read_csv('./sentimentsOlderHalf.csv')

dfTweets = sum_for_day(dfTweets)
dfTest = sum_for_day(dfTest)
training_tweets = []
training_stocks = []
test_tweets = []
test_stocks = []
for i in range(43):
    test_tweets.append(week_lookback(dfTweets['date'][13+i*7],dfTweets))
    test_stocks.append(stock_lookforward(dfTweets['date'][13+i*7],dfStocks))


for i in range(43):
    training_tweets.append(week_lookback(dfTest['date'][8+i*7],dfTest))
    training_stocks.append(stock_lookforward(dfTest['date'][8+i*7],dfStocks))

p = predict()
p.neural_net()
p.train_second(np.array(training_tweets),np.array(training_stocks),np.array(test_tweets),np.array(test_stocks))

#print(np.array(training_stocks))
#print(training_tweets)
#print(dfTweets)
#print(dfStocks)
