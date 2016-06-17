__author__ = 'sangchae'

class Market:
    def __init__(self, test):
        print("Select Market: 1.Korea 2.U.S.A. 3.Hongkong 4.China")
        sel = input()

        if test == 1:
            print(sel)

        # read kospi information
        if sel == '1':
            f = open("YAHOO_KOSPI.txt")
            lists = f.readlines()
            print(lists)
