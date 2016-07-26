__author__ = 'sangchae'

''' It shows news or other information such as Oil price, Currency, and so on
'''

from bs4 import BeautifulSoup
from urllib.request import urlopen

class Information():
    def __init__(self):
        res = urlopen('http://www.infostock.co.kr')
        soup = BeautifulSoup(res, 'html.parser')

        soup.prettify()
        data = []
        for string in soup.strings:
            if(repr(string) != '\'\\n\'' and repr(string) != '\' \''):
                data.append(repr(string))

        #print(data)
        print("\t          가격\t          전일대비")
        for i in range(len(data)):
            if data[i] == '\'국제유가\'':
                print("국제유가:\t", "$",data[i+1][1:-2], "\t", data[i+2][1:-5])
            if data[i] == '\'Won/Dollar\'':
                print("환   율:\t", "W",data[i+1][1:-2], "\t", data[i+2][1:-5])


