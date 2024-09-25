# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 19:37:52 2024

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
def get_sector(ticker):
    stock = yf.Ticker(ticker)
    try:
        return stock.info['sector']
    except:
        return 0
def get_price(ticker):
    stock = yf.Ticker(ticker)
    try:
        return stock.info['currentPrice']
    except:
        return 0
def avg_volume(ticker):
    stock = yf.Ticker(ticker)
    try:
        return stock.info['averageVolume']
    except:
        return 0

def screen_stocks(tickers, start_date, end_date):
    results = []
    for ticker in tickers:
        try:
            data = fetch_stock_data(ticker, start_date, end_date)
            sector = get_sector(ticker)
            price = get_price(ticker)
            average_volume = avg_volume(ticker)
            volatility = calculate_volatility(data)
            div_yield = get_dividend_yield(ticker)
            results.append({
                'Ticker': ticker,
                'Sector': sector,
                'Price': price,
                'Avg Volume': average_volume,
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

# run analysis sort by calculated score

results = screen_stocks(tickers, start_date, end_date)
results = results.sort_values('Score', ascending=False)

'Reset index and remove unwanted sectors and securities with out a Dividend.'
results = results.drop(results[results['Dividend Yield'] < .001].index)
results = results.drop(results[results['Sector'] == 'Real Estate'].index)
results = results.reset_index(drop=True)
results.to_csv('data/sp_500_results.csv', index=False)

print(results)


