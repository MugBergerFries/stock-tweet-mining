import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

dfStocks = pd.read_csv('StockData/HistoricalQuotesTSLA.csv')
dfSentiments2012 = pd.read_csv('StockData/weeklySentiment12.csv')
dfSentiments2013 = pd.read_csv('StockData/weeklySentiment13.csv')
dfSentiments2014 = pd.read_csv('StockData/weeklySentiment14.csv')
dfSentiments2015 = pd.read_csv('StockData/weeklySentiment15.csv')
dfSentiments2016 = pd.read_csv('StockData/weeklySentiment16.csv')
dfSentiments2017 = pd.read_csv('StockData/weeklySentiment17.csv')
sentimentDfs = {}
sentimentDfs['2012'] = dfSentiments2012
sentimentDfs['2013'] = dfSentiments2013
sentimentDfs['2014'] = dfSentiments2014
sentimentDfs['2015'] = dfSentiments2015
sentimentDfs['2016'] = dfSentiments2016
sentimentDfs['2017'] = dfSentiments2017

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
    musksentiments = []
    df = sentimentDfs[year]
    musksentiments = df[year].tolist()
    
    stocklist = []
    stocklist = getDatabyYear(stockclose,stockdates,year,StockWeekList)
    stocklistlen = list(range(1,len(stocklist)+1))
    
    f, pl1 = plt.subplots(figsize = (50,28))
    f.suptitle("Elon Musk Tweet Sentiments vs. Tesla Stock Prices "+year,fontsize=50)
    pl2 = pl1.twinx()
    pl1.bar(weeks,musksentiments,label="Elon Musk Tweets")
    pl1.axis(xmin=1)
    
    pl2.plot(stocklistlen,stocklist,color="orange",linewidth=7.0,label="Tesla Stock Price at Close")
    
    pl2.grid(b=False)
    
    pl1.set_xlabel('Week',fontsize=40)
    pl1.set_ylabel('Sentiment',fontsize=40)
    
    pl2.set_ylabel('Stock Price',fontsize=40)
    
    pl1.tick_params(axis='both', which='major', labelsize=40)
    pl2.tick_params(axis='both', which='major', labelsize=40)
    
    plt.legend(loc=0,fontsize=40)
    
    plt.savefig('Graphs/SentimentVsStock'+year+'.png')
    plt.show()

plot_data('2012')
plot_data('2013')
plot_data('2014')
plot_data('2015')
plot_data('2016')
plot_data('2017')