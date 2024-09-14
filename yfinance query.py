# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 10:14:28 2024

@author: joegr

list all available fields for an equity via yfinance.
This will help, with our security analysis.

"""
import yfinance as yf
import pandas as pd

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    try:
        return stock.info
    except:
        return 0
        
stock_info = get_stock_info('MSFT')

display(stock_info)
        
    

