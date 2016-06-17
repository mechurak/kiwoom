__author__ = 'sangchae'


import pandas as pd
import pandas.io.data as web
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import date2num
import bollingerband, envelope, golden, menu, market

test = 1

if __name__ == "__main__":
    # below contents will belong to another file, menu.py
    me = menu.Menu()

    # selelct what you want to do
    sel_menu = me.menu_decide(test)

    # select what you want to see the result of the simulation
    mar = market.Market(test)





    # select starting date and ending date
