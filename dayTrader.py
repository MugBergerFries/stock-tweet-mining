import csv


dayTraderMoney = 10000.00
investorStock = 10000.00 / 217.91
boughtIn = False
totalStocks = 0.0
lineCount = 0
daysValue = 0.0

resultsFile = open('results.csv', 'w')
resultsFile.write('data, long term, day trading\n')

with open('modTSLA.csv') as csvFile:
    reader = csv.reader(csvFile, delimiter=',')
    for row in reader:
        lineCount += 1
        if (int(row[3]) == 1 and boughtIn == False):
            print("Buying in")
            daysValue = dayTraderMoney
            totalStocks = dayTraderMoney / float(row[1])
            dayTraderMoney = 0
            boughtIn = True
            resultsFile.write(row[0] + ',' + str(investorStock * float(row[2])) + ', ' + str(daysValue) + '\n')
        elif (int(row[3]) == 0 and boughtIn == True):
            print("Getting out")
            dayTraderMoney = totalStocks * float(row[1])
            totalStocks = 0
            boughtIn = False
            resultsFile.write(row[0] + ',' + str(investorStock * float(row[2])) + ', ' + str(dayTraderMoney) + '\n')
        finalStockPrice = float(row[2])

if (boughtIn == True):
    dayTraderMoney = finalStockPrice * totalStocks

print("Day trader money = " + str(dayTraderMoney))

resultsFile.close()