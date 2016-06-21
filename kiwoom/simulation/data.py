__author__ = 'sangchae'
import pandas as pd
import pandas.io.data as web

# this class saves all information
# save or real-time processing?
# data structure from Pandas as followings:
# open/high/low/close/volume/adj close/ma...
#
class Data:
    def __init__(self, start, end): # start : starting date, end : ending date or current date
        pass

    def Download_Latest_Data(self, name, start, end):
        DB = web.DataReader(name+str('.KS'), "yahoo", start, end)
        DB.to_csv(name+str('.csv'))

    def Read_Stored_Data(self, name):
        pass