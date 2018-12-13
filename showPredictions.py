import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

# the evaluated prediction data
e_data = [0, 1, 0, 0, 1,0, 1, 0, 0, 1,1, 1, 1, 0, 0,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,1, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,1, 1, 0, 1, 0,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,1, 0, 0, 0, 1,0, 1, 0, 0, 1,1, 1, 0, 1, 0,0, 1, 0, 0, 1,0, 1, 0, 0, 1,1, 1, 0, 0, 0,0, 1, 0, 0, 1,0, 1, 0, 0, 1,1, 0, 0, 1, 0,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1,0, 1, 0, 0, 1]

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


# get all the stock data in this date range
def getDatabyDateRange(dates,start_date,end_date):
    data = []
    locs = []
    go = False
    i=0
    month_locs = []
    for d in dates:
        if d == start_date:
            go = True
        if go:
            data.append(d)
            locs.append(i)
            if d[5:]=='04/03':
                month_locs.append(i)
            if d[5:]=='03/01':
                month_locs.append(i)
            if d[5:]=='02/01':
                month_locs.append(i)
            if d[5:]=='01/03':
                month_locs.append(i)
            if d[5:]=='12/01':
                month_locs.append(i)
            if d[5:]=='11/01':
                month_locs.append(i)
            if d[5:]=='10/03':
                month_locs.append(i)
            if d[5:]=='09/01':
                month_locs.append(i)
            if d[5:]=='08/01':
                month_locs.append(i)
            if d[5:]=='07/01':
                month_locs.append(i)
            if d[5:]=='06/01':
                month_locs.append(i)
        if d == end_date:
            go = False
        i+=1
    return data, locs, month_locs

# get the data
start_date = '2017/04/03'
end_date = '2016/05/26'
data, locs, month_locs = getDatabyDateRange(stockdates,start_date,end_date)

month_names = ["April '17","March '17","February '17","January '17","December '16","November '16","October '16","September '16","August '16","July '16","June '16"]
months = []
q=0
for l in locs:
    if l in month_locs:
        months.insert(0,month_names[q])
        q+=1
    else:
        months.insert(0,"")

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

same = 0
notsame = 0
pred_len = len(pred_stocks)
for i in range(0,pred_len):
    if(actual_data[i]==e_data[i]):
        same+=1
    else:
        notsame+=1
percent_correct = 100/pred_len*same
print(percent_correct,'% correct')

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
fig = plt.figure(1, figsize=(50, 28))
ax1 = fig.add_subplot(111)
ax1.plot(data,pred_stocks,color="blue",label="Stock Price at Close")
ax1.scatter(rightdates,rightpoints,color="green",linewidths=10,label="Correct Prediction")
ax1.scatter(wrongdates,wrongpoints,color="red",linewidths=10,label="Incorrect Prediction")
ax1.set_title("Predictions of Stock Prices from Tweet Sentiments - "+"{:.2f}".format(percent_correct)+"% correct",fontsize=50)
ax1.tick_params(axis = 'both', which = 'major', labelsize = 24)
ax1.tick_params(axis = 'both', which = 'minor', labelsize = 16)
ax1.set_ylabel("Stock Price ($)",fontsize=50)
ax1.set_xlabel("Date",fontsize=50)
ax1.legend(loc=0,fontsize=40)
ax1.set_xticklabels(months)
plt.savefig('Graphs/PredictionResults.png')
plt.show()
