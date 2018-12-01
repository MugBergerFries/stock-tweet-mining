import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

dfStocks = pd.read_csv('StockData/HistoricalQuotesTSLA.csv')
dfTweets2012 = pd.read_csv('StockData/ColumnTweets2012.csv')
dfTweets2013 = pd.read_csv('StockData/ColumnTweets2013.csv')
dfTweets2014 = pd.read_csv('StockData/ColumnTweets2014.csv')
dfTweets2015 = pd.read_csv('StockData/ColumnTweets2015.csv')
dfTweets2016 = pd.read_csv('StockData/ColumnTweets2016.csv')
dfTweets2017 = pd.read_csv('StockData/ColumnTweets2017.csv')
tweetDfs = {}
tweetDfs['2012'] = dfTweets2012
tweetDfs['2013'] = dfTweets2013
tweetDfs['2014'] = dfTweets2014
tweetDfs['2015'] = dfTweets2015
tweetDfs['2016'] = dfTweets2016
tweetDfs['2017'] = dfTweets2017

stockdates = []
stockclose = []
stockdates = dfStocks['date'].tolist()
stockclose = dfStocks['close'].tolist()

stockweeks = []
i = 0
for item in stockdates:
    try:
        dateOfStock = item.split('/')
        week = datetime.date(int(dateOfStock[0]), int(dateOfStock[1]), int(dateOfStock[2])).isocalendar()[1]
        stockweeks.append(week)
    except:
        stockweeks.append(-1)
    i+=1
    
dfStocks['week'] = stockweeks
StockWeekList = dfStocks['week'].tolist()
weeks = list(range(1,54))

def getDatabyYear(values,dates,year,weeks):
    i = 0
    data = [[] for _ in range(53)]
    for item in values:
        if dates[i][0:4]==year:
            data[weeks[i]-1].append(item)
        i+=1
    averages = []
    for l in data:
        averages.append(np.mean(l))
    return averages

def plot_data(year):
    muskcounts = []
    df = tweetDfs[year]
    muskcounts = df[year].tolist()
    
    stocklist = []
    stocklist = getDatabyYear(stockclose,stockdates,year,StockWeekList)
    stocklistlen = list(range(1,len(stocklist)+1))
    
    f, pl1 = plt.subplots(figsize = (50,28))
    f.suptitle("Elon Musk Tweet Counts vs. Tesla Stock Prices "+year,fontsize=50)
    pl2 = pl1.twinx()
    pl1.bar(weeks,muskcounts,label="Elon Musk Tweets")
    pl1.axis(xmin=1)
    
    pl2.plot(stocklistlen,stocklist,color="orange",linewidth=7.0,label="Tesla Stock Price at Close")
    
    pl2.grid(b=False)
    
    pl1.set_xlabel('Week',fontsize=40)
    pl1.set_ylabel('Tweet Count',fontsize=40)
    
    pl2.set_ylabel('Stock Price',fontsize=40)
    
    pl1.tick_params(axis='both', which='major', labelsize=40)
    pl2.tick_params(axis='both', which='major', labelsize=40)
    
    plt.legend(loc=0,fontsize=40)
    
    plt.savefig('Graphs/TweetVsStock'+year+'.png')
    plt.show()

plot_data('2012')
plot_data('2013')
plot_data('2014')
plot_data('2015')
plot_data('2016')
plot_data('2017')