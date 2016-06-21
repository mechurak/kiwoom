__author__ = 'sangchae'
import pandas as pd
import pandas.io.data as web

# this class saves all information
# save or real-time processing?
#
class Data:
    def __init__(self, start, end): # start : starting date, end : ending date or current date
        pass

    # download latest data
    # it stores values of Date, Open, High, Low, Close, Volume, Adj Close, ma
    def Download_Latest_Data(self, name, start, end, ma): # ma should moving average
        DB = web.DataReader(name + str('.KS'), "yahoo", start, end)
        DB[ma] = pd.stats.moments.rolling_mean(DB['Adj Close'], int(ma[2:]) )

    def Read_Data(self):
        pass