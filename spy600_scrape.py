# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 14:40:34 2024

@author: joegr
"""

''' This file scrapes wikipedia for the SPX 600
https://en.wikipedia.org/wiki/List_of_S%26P_600_companies'''
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
url='https://en.wikipedia.org/wiki/List_of_S%26P_600_companies'
sp600=r.get(url,headers=headers)
# display(sp600)

# lets make some soup
soup = BeautifulSoup(sp600.content, 'html.parser')
tables = soup.find_all('table', attrs={'class': 'wikitable'})
sp600cl = tables[0]
sp600changes = tables[1]

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
sp600_ticker_list=parse_table(sp600cl)
sp600_ticker_list.drop([0],inplace=True)
sp600_ticker_list=sp600_ticker_list[['Symbol\n']]
sp600_ticker_list=sp600_ticker_list.replace(r'\n','', regex=True)
sp600_ticker_list=sp600_ticker_list.rename(columns={'Symbol\n': 'ticker'})
sp600_ticker_list=sp600_ticker_list.reset_index(drop=True)

# display(sp600_ticker_list)

### save to an excel file
sp600_ticker_list.to_csv('data/spx600.csv')
