# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 14:40:01 2024

@author: joegr

This model will scan an index, in this case $SPX600, and look for
low volitility stocks with a high yield. The theory being if we pinpoint good
low volitility stocks, we can invest into high dividends. At the end, we sort
our findings in a score order.

"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def fetch_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date)
    return hist

def calculate_volatility(data):
    returns = data['Close'].pct_change()
    volatility = returns.std() * np.sqrt(252)  # Annualized volatility
    return volatility

def get_dividend_yield(ticker):
    stock = yf.Ticker(ticker)
    try:
        return stock.info['dividendYield']
    except:
        return 0

def screen_stocks(tickers, start_date, end_date):
    results = []
    for ticker in tickers:
        try:
            data = fetch_stock_data(ticker, start_date, end_date)
            volatility = calculate_volatility(data)
            div_yield = get_dividend_yield(ticker)
            results.append({
                'Ticker': ticker,
                'Volatility': volatility,
                'Dividend Yield': div_yield,
                'Score': div_yield / volatility if volatility > 0 else 0
            })
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
    
    return pd.DataFrame(results)

# Intake SPX600
'You will have to run the spy600_scrape.py file for symbol list'
symbols = pd.read_csv('data/spx600.csv', sep=",")
symbols = symbols.drop(symbols.columns[0], axis=1)
tickers = symbols['ticker'].tolist()
# set time constraints
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
# run analysis 
results = screen_stocks(tickers, start_date, end_date)
results_sorted = results.sort_values('Score', ascending=False)
results_sorted.to_excel('data/results.xlsx')

