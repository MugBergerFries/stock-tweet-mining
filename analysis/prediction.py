import tensorflow as tf
from tensorflow import keras


class predict:
    def __init__(self,tweet_data,stock_data):
        self.tweets = tweet_data
        self.stocks = stock_data


    def calculate_covariance(self):
        #self.tweets.stat.cov('')
        
        #print("TWEET MEAN ISSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS {} AND STOCKS ARE {}".format(tweet_mean,stock_mean))
        pass
    
    def find_outliers(self):
        pass

    def neural_net(self):
        # format data to match training data

        model = keras.Sequential([
            keras.layers.Dense(30,activation='relu'),
            keras.layers.Dense(20,activation='relu'),
            keras.layers.Dense(10,activation='relu'),
            keras.layers.Dense(1)
        ])

        optimizer = tf.train.RMSPropOptimizer(0.001)

        model.compile(optimizer=optimizer,
              loss='mse', # classify for 0 or 1
              metrics=['mae'])  # get accuracy

        model.fit(self.tweets.toPandas().values,self.stocks.toPandas()['diff'].values[0:6],epochs=1000)

        # model.fit(x: samples, y: labels) # labels are the stock differences (up or down) and the samples is the tweet data
        
        # Create training data -> inputs = bins of tweet sentiments (maybe also timestamps)
        #                       -> outputs = up or down, go through current stock data, get ups and downs
        
        # input data as vector, use binning
        # pass 
        # per unit time inputs?
        # batch learning, process a classifier per day. Classify only for data per day
        # inputs = tweets on particular day, outputs = predicted stock price on that day, or whether price will go up or down
