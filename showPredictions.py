import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

# the evaluated prediction data
e_data = [0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
1, 1, 1, 0, 0,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
1, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
1, 1, 0, 1, 0,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
1, 0, 0, 0, 1,
0, 1, 0, 0, 1,
1, 1, 0, 1, 0,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
1, 1, 0, 0, 0,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
1, 0, 0, 1, 0,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1,
0, 1, 0, 0, 1]

dfStocks = pd.read_csv('StockData/HistoricalQuotesTSLA.csv')

stockdates = []
stockclose = []
stockdates = dfStocks['date'].tolist()
stockclose = dfStocks['close'].tolist()
stockopen = dfStocks['open'].tolist()

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

# holidays to skip
skip_dates = ['2017/02/21','2017/01/17','2017/01/03','2016/12/27','2016/11/25','2016/09/06','2016/07/05'] #all +1 day
#President's day 2/20/2017, MLK 1/16/2017, New years 1/2/2017, christimas 12/26/2016, thanksgiving 11/24/2016, labor day 9/5/2016, 4th of july 7/4/2016

# get all the stock data in this date range
def getDatabyDateRange(dates,start_date,end_date):
    data = []
    locs = []
    skip_locs = []
    go = False
    i=0
    j=0
    for d in dates:
        if d == start_date:
            go = True
        if go:
            data.append(d)
            locs.append(i)
            if(d in skip_dates):
                skip_locs.append(j+1)
            j+=1
        if d == end_date:
            go = False
        i+=1
    return data, locs, skip_locs

# get the data
start_date = '2017/03/31'
end_date = '2016/06/06'
data, locs, skip_locs = getDatabyDateRange(stockdates,start_date,end_date)

#update the evaluated data to delete holidays
for e in range(0,len(e_data)):
    if(e in skip_locs):
        del e_data[e]

# get the stock data for this range
pred_stocks = []
for l in locs:
    pred_stocks.append(stockclose[l])

# get the actual data for each day, whether it went up or down   
actual_data = []
for l in locs:
    if(stockclose[l]>stockopen[l]):
        actual_data.append(1)
    else:
        actual_data.append(0)

print(actual_data)
print(e_data)

same = 0
notsame = 0
pred_len = len(pred_stocks)
for i in range(0,pred_len):
    if(actual_data[i]==e_data[i]):
        same+=1
    else:
        notsame+=1
print(same)
print(notsame)

rightdates = []
wrongdates = []
rightpoints = []
wrongpoints = []
for i in range(0,pred_len):
    if(actual_data[i]==e_data[i]):
        rightdates.append(data[i])
        rightpoints.append(pred_stocks[i])
    else:
        wrongdates.append(data[i])
        wrongpoints.append(pred_stocks[i])

# show the data
#f, pl1 = plt.subplots(figsize = (50,28))
#f.suptitle("Predictions",fontsize=50),linewidth=7.0,label="Tesla Stock Price at Close"
fig = plt.figure(1, figsize=(50, 28))
ax1 = fig.add_subplot(111)
ax1.plot(data,pred_stocks,color="blue")
ax1.scatter(rightdates,rightpoints,color="green",linewidths=10)
ax1.scatter(wrongdates,wrongpoints,color="red",linewidths=10)
#plt.legend(loc=0,fontsize=40)
plt.show()
