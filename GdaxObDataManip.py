#### TODO
# more sofisticated data science
# find correlations between orderbook data features and price changes

import json
import numpy as np
import pandas as pd
from pprint import pprint
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression

# ONLY USES GDAX OB DATA AS OF NOW

################## MUTABLE PARAMETERS ###################
# in minutes
S1 = 15
S2 = 30
S3 = 45
# Data collection frequency in seconds
collectionFreq = 10
# Time in future to predict in tens of seconds
futureSecsDivTen = 6
###########################################################

####################### Pulling from Kraken ##############
KrakenDataList = []
numKrakenLines = 0
with open('../Jims_Project/KrakenOrderBook.json') as f:
	for line in f:
		KrakenDataList.append(json.loads(line))
		numKrakenLines +=1

###########################################################


# Pull JSON into list
ObDataList = []
numLines = 0;
with open('../Jims_Project/GdaxOrderBook.json') as f:
	for line in f:
		ObDataList.append(json.loads(line))
		numLines += 1	

# gdax Array inits
gdaxTime = np.zeros(numLines)
marketPrice = np.zeros(numLines)
firstLevelAsk = np.zeros(numLines)
firstLevelBid = np.zeros(numLines)
tenLevelAskMean = np.zeros(numLines)
tenLevelBidMean = np.zeros(numLines)
fiftyLevelAskMean = np.zeros(numLines)
fiftyLevelBidMean = np.zeros(numLines)
time = np.zeros(numLines)
priceChange = np.zeros(numLines)
r50= np.zeros(numLines)
r10 = np.zeros(numLines)
avgTenArray = np.zeros(10)
avgFiftyArray = np.zeros(50)


dex =0
for line in ObDataList:
	# get time array from Gdax stamps (kraken should have identical stamps)
	gdaxTime[dex]=line['time']
	# Determine market price, place into dataframe
	marketPrice[dex] = (float(line['bids'][0][0])+float(line['asks'][0][0]))/2
	# First level ask volume
	firstLevelAsk[dex] = float(line['asks'][0][1])
	# First level bid volume
	firstLevelBid[dex] = float(line['bids'][0][1])
	# Mean volume of first 10 asks
	for x in range(0,10):
		avgTenArray[x] = float(line['asks'][x][1])
	tenLevelAskMean[dex] = np.average(avgTenArray)
	# Mean volume of first 10 bids
	for x in range(0,10):
		avgTenArray[x] = float(line['bids'][x][1])
	tenLevelBidMean[dex] = np.average(avgTenArray)
	# Mean volume of top 50 asks
	for x in range(0,50):
		avgFiftyArray[x] = float(line['asks'][x][1])
	fiftyLevelAskMean[dex] = np.average(avgFiftyArray)
	# Mean volume of top 50 bids
	for x in range(0,50):
		avgFiftyArray[x] = float(line['bids'][x][1])
	fiftyLevelBidMean[dex] = np.average(avgFiftyArray)
	# Price change from last sample
	priceChange[dex] = marketPrice[dex] - marketPrice[dex-1]
	# time
	time[dex] = int(line['time'])
	dex+=1

# problems
#		what if kraken data length isnt same as gdax?
#		
#
#	
	

timeFrame = pd.DataFrame()
timeFrame['CurrentPrice'] = marketPrice
timeFrame['FuturePrice'] = timeFrame['CurrentPrice'].shift(-6)
timeFrame['PriceChange'] = priceChange

# Average price change over last 45 minutes (2700000ms) (S3)
rangeBegin = int(np.ceil((S3*60)/collectionFreq)+1)
rangeEnd = timeFrame.index[-1]+1
S3Average = np.zeros(rangeEnd - rangeBegin)

dex=0
for x in range(rangeBegin, rangeEnd):
	avgStartDex = x - rangeBegin
	sliced = priceChange[avgStartDex:x]
	S3Average[dex] = np.average(sliced)
	dex+=1

timeFrame = timeFrame.iloc[rangeBegin:rangeEnd].reset_index(drop=True)
timeFrame['S3Average'] = S3Average

pprint("S3Average size: " + str(S3Average.size))
pprint("timeFrame size: " + str(timeFrame.size))
timeFrame.dropna(inplace=True)
timeFrame.drop(timeFrame.index[0], inplace=True)
pprint(timeFrame)

# Average price change over50last 30 minutes (1800000ms)

# Average price change over50last 15 minutes (900000ms)



# r50 value (Vbid-Vask)/(Vbid+Vask)
r50= np.divide(np.subtract(fiftyLevelBidMean,fiftyLevelAskMean),np.add(fiftyLevelBidMean,fiftyLevelAskMean))

# r10 value (Vbid-Vask)/(Vbid+Vask)
r10= np.divide(np.subtract(tenLevelBidMean,tenLevelAskMean),np.add(tenLevelBidMean,tenLevelAskMean))

dataFrame  = pd.DataFrame()
dataFrame['r50'] = r50
dataFrame['r10'] = r10
dataFrame['MarketPrice'] = marketPrice
dataFrame['FuturePrice'] = dataFrame['MarketPrice'].shift(-futureSecsDivTen)
dataFrame.dropna(inplace=True)



# X = np.array(dataFrame.drop(['FuturePrice'],1))
# X = preprocessing.scale(X)
# Y = np.array(dataFrame['FuturePrice'])

# X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X,Y,test_size=0.2)

# clf = LinearRegression()
# clf.fit(X_train, Y_train)
# accuracy = clf.score(X_test, Y_test)

# print(accuracy)







