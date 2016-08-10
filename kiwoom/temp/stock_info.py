__author__ = 'sangchae'
from bs4 import BeautifulSoup
from urllib.request import urlopen

#http://finance.naver.com/item/main.nhn?code= + code

res = urlopen('http://finance.naver.com/item/main.nhn?code=000660')
soup = BeautifulSoup(res, 'lxml')
soup.prettify()
print(soup)
#print(soup.strings)

