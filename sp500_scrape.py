# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 19:33:39 2024

@author: joegr

This file scrapes wikipedia for the SPX 500
https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
"""
# import libraries
import pandas as pd # excel for python
import requests as r # ability to bring in data
import os # brings in os functions
import regex
from bs4 import BeautifulSoup # ability to parse a web page for the data that we need
import yfinance as yf #used to request a securities feature data

#get data from page
headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 \
           (KHTML, like Gecko) \
           Chrome/47.0.2526.106 Safari537.36'}
url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
sp500=r.get(url,headers=headers)
# display(sp500)

# lets make some soup
soup = BeautifulSoup(sp500.content, 'html.parser')
tables = soup.find_all('table', attrs={'class': 'wikitable'})
sp500cl = tables[0]
sp500changes = tables[1]

def parse_table(html_table) -> pd.DataFrame:
    columns =[]
    rows = []
    for column in html_table.find_all('th'): # 'th' table headers
        columns.append(column.text)
    for row in html_table.find_all('tr'): # 'tr' table rows
        row_to_add =[]
        for cell in row.find_all('td'): # 'td' table data
            row_to_add.append(cell.text)
        rows.append(row_to_add)
    df = pd.DataFrame(rows,columns=columns)
    return df

# clean data, this will be turned into a function at a later time.
sp500=parse_table(sp500cl)
sp500.drop([0],inplace=True)
sp500=sp500[['Symbol\n']]
sp500=sp500.replace(r'\n','', regex=True)
sp500=sp500.rename(columns={'Symbol\n': 'ticker'})
sp500=sp500.reset_index(drop=True)

### save to an excel file
sp500.to_csv('data/spx500.csv')


