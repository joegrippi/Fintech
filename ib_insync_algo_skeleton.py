# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 11:21:01 2024

@author: joegr
"""

### Load libraries
from datetime import datetime
import requests as r
import pandas as pd
import numpy as np
import talib as ta
import matplotlib.pyplot as plt
import seaborn as sns
from ib_insync import *

### Connect and set ib functions
util.startLoop()
ib = IB()
ib.connect('127.0.0.1', 4001, clientId=17) # ibgateway

### Qualify Contract
etf='USO'
contract = Stock(symbol = etf, exchange = 'SMART', currency = 'USD')
ib.qualifyContracts(contract)

def get_latest_price(contract):
    bars =  ib.reqHistoricalData(contract, endDateTime='',durationStr='5 y',
                                barSizeSetting='1 day', whatToShow='MIDPOINT',
                                useRTH=True, formatDate=1)
    return bars[-1].close

while True:
    try:
        # Get the latest price
        price = get_latest_price(contract)
        print(f"Current price for {contract.symbol}: {price}")

        # Optional: Add your logic to handle the price update here 
        # (e.g., trading decision based on price)

        # Sleep for a short period to avoid excessive API calls
        time.sleep(1)

    except Exception as e:
        print(f"Error getting price: {e}") 
        # Handle potential errors 

# Disconnect from IB API 
ib.disconnect()