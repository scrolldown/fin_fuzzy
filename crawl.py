#-*- coding: utf-8 -*-
import sys
import urllib2
import bs4
import pandas as pd

url = 'http://info.finance.naver.com/fund/fundTypeEarningRate.nhn'
request = urllib2.Request(url)
request.add_header('Accept-Encoding','utf-8')
html = urllib2.urlopen(request)

soup = bs4.BeautifulSoup(html, 'html.parser')

title=soup.find_all('td',{'class':'type'})
amount=soup.find_all('td',{'class':'set'})

for row in title:
    print [row1 for row1 in row.find('a')]
"""
for data in zip(title, amount):
    for row1 in data[0].find('a'):
        str(row1).s
        print row1
    
    print data[1].text
"""


"""
euc_bytes=r'K200\xc3\x80\xc3\x8e\xc2\xb5\xc2\xa6\xc2\xbd\xc2\xba'
utf_bytes = unicode(euc_bytes,'cp949').encode('utf-8')
print euc_bytes.decode('string-escape')
print utf_bytes
"""
