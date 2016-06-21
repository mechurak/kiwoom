__author__ = 'sangchae'
import pandas as pd
import pandas.io.data as web

# this class saves all information
# save or real-time processing?
<<<<<<< HEAD
# data structure from Pandas as followings:
# open/high/low/close/volume/adj close/ma...
=======
#
>>>>>>> origin/master
class Data:
    def __init__(self, start, end): # start : starting date, end : ending date or current date
        pass

<<<<<<< HEAD
    def Download_Latest_Data(self, name, start, end):
        DB = web.DataReader(name+str('.KS'), "yahoo", start, end)
        DB.to_csv(name+str('.csv'))

    def Read_Stored_Data(self, name):
=======
    # download latest data
    # it stores values of Date, Open, High, Low, Close, Volume, Adj Close, ma
    def Download_Latest_Data(self, name, start, end, ma): # ma should moving average
        DB = web.DataReader(name + str('.KS'), "yahoo", start, end)
        DB[ma] = pd.stats.moments.rolling_mean(DB['Adj Close'], int(ma[2:]) )

    def Read_Data(self):
>>>>>>> origin/master
        pass