import requests
import bs4
import pandas as pd
import numpy as np

def __init__():
    df=[]
    url=[]

def GetDf(url):
    r = requests.get(url)
    html = r.text

    soup = bs4.BeautifulSoup(html, 'html.parser')
    allRows = soup.find('tbody').find_all('tr')

    results = [[data.text.split('?')[0].replace('\n','').replace('\t','') for data in td.find_all('td')]\
               for td in allRows]

    rowspan = [] #row

    for tr_no, tr in enumerate(allRows): #enumerate returns index, data 
        tmp = []
        for td_no, data in enumerate(tr.find_all('td')):
            if data.has_attr("rowspan"):
                rowspan.append((tr_no, td_no, int(data["rowspan"]), data.get_text().split('?')[0].replace('\n','').replace('\t','')))

    if rowspan:
        for i in rowspan:
            for j in range(1, i[2]):
                results[i[0]+j].insert(i[1],i[3])

    headers=[]

    for i in range(1,11):
        if i==6:
            continue
        if i==9:
            headers.append(soup.find('thead').find('th',{'class':'th_result'+str(i)+'_on'}).text)
        else:
            headers.append(soup.find('thead').find('th',{'class':'th_result'+str(i)}).text)    
    
    df = pd.DataFrame(data=results)
    
    df.columns = headers
    
    df['설정액'] = df['설정액'].str.replace(',','').astype(float)
    df['1개월 증감액'] = df['1개월 증감액'].str.replace(',','').astype(float)
    df = df.replace('N/A',np.nan)
    df.dropna(inplace=True)
    
    df = df.apply(pd.to_numeric, args =('ignore',))
    
    df.reset_index(inplace=True, drop=True)
    return df