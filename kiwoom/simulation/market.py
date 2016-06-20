__author__ = 'sangchae'

class Market:
    def __init__(self, test):
        print("Select Market: 1.KOSPI 2.NASDAQ. 3.Hongkong 4.China")
        sel = input()

        if test == 1:
            print(sel)

        # read kospi information
        if sel == '1':
            f = open("YAHOO_KOSPI.txt")
        elif sel == '2':
            pass
        elif sel == '3':
            pass
        elif sel == '4':
            pass

        lists = f.readlines()

