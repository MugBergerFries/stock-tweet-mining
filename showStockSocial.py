import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

def getDatabyYear(values,dates,year,weeks):
    i = 0
    data = [[] for _ in range(52)]
    for item in values:
        if dates[i][0:4]==year:
            data[weeks[i]-1].append(item)
        i+=1
    averages = []
    for l in data:
        averages.append(np.mean(l))
    return averages

dfStocks = pd.read_csv('StockData/HistoricalQuotesTSLA.csv')
dfTweets = pd.read_csv('ColumnTweets.csv')

stockdates = []
stockclose = []
muskcounts12 = []
stockdates = dfStocks['date'].tolist()
stockclose = dfStocks['close'].tolist()
muskcounts12 = dfTweets['2012'].tolist()

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

stocklist12 = []
stocklist12 = getDatabyYear(stockclose,stockdates,'2012',StockWeekList)
stocklist12len = list(range(1,len(stocklist12)+1))

weeks = list(range(1,54))

f, (pl1, pl2) = plt.subplots(1, 2, figsize = (25,7))
pl1.bar(weeks,muskcounts12)
pl1.axis(xmin=1)
pl1.set_xlabel('Week')
pl1.set_ylabel('Tweet Count')
f.subplots_adjust(wspace=0.2)
pl2.plot(stocklist12len,stocklist12)
pl2.set_xlabel('Week')
pl2.set_ylabel('Stock Price')
plt.show()