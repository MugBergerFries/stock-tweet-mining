import requests
import datetime

now = datetime.datetime.now()
r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=TSLA&apikey=N911MSQOY5DXTE2T&outputsize=full&interval=1min")
with open("TSLA_intraday" + now.isoformat()[0:10],"w+") as f:
	f.write(r.text)



