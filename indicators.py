import pandas as pd
import numpy as np

def get_price_changes(current_price, close_prices, days):
    #closing price at the beginning of the period
    start_price = close_prices.tail(days).iloc[0]

    usd_change = current_price - start_price
    percent_change = (usd_change/start_price) * 100

    return round(usd_change, 2), round(percent_change, 2)


def get_volatility(close_prices, days):
    prices = close_prices.tail(days)
    log_returns = np.log(prices / prices.shift(1))
    v_flt = log_returns.std()
    v_pct = v_flt * 100
    return v_flt, round(v_pct, 2)


# def get_moving_averages(close_prices, days, window):
#     moving_averages = []
    
#     for i in range(days):
#         if i == 0:
#             moving_avg = close_prices.iloc[-window:].mean()
#         else:
#             moving_avg = close_prices.iloc[-(i+window):-i].mean()
#         moving_averages.append(round(moving_avg,2))
    
#     moving_averages.reverse()

#     return moving_averages[0], moving_averages


def get_MAs(close_prices, days, window):
    moving_averages = (
        close_prices
        .rolling(window=window)
        .mean()
        .dropna()
        .round(2)
        .tail(days)
        .to_list()
        )
    return moving_averages[-1], moving_averages


def get_OBV():
