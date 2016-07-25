__author__ = 'sangchae'
from bs4 import BeautifulSoup
from urllib.request import urlopen

res = urlopen('http://www.infostock.co.kr')#.read().decode('utf-8')
soup = BeautifulSoup(res, 'html.parser')

#print(soup.prettify())

oils = soup.find_all('td', class_='8point')

#for oil in oils:
#print(oil)