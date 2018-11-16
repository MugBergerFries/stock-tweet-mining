import pandas as pd

names = ['SYY','FDX','PEP','MET','RTN','LMT','NOC','BA','JPM','COST','CVX','F','VZ','T','CVS','GM','TSLA','AMZN','WMT','XON','GOOG','AAPL','MSFT']

df = []

for i in names:
	df.append(pd.read_csv('StockData/HistoricalQuotes' + i + '.csv'))
#df = pd.read_csv('StockData/HistoricalQuotesMSFT.csv')



print(df)
