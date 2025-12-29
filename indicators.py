import pandas as pd
import numpy as np

def get_price_changes(current_price, close_prices, days_in_period):
    #closing price at the beginning of the period
    start_price = close_prices.tail(days_in_period).iloc[0]

    usd_change = current_price - start_price
    percent_change = (usd_change/start_price) * 100

    return round(usd_change, 2), round(percent_change, 2)


def get_volatility(close_prices, days_in_period):
    v_flt = close_prices.tail(days_in_period).pct_change().std()
    v_pct = v_flt * 100
    return v_flt, round(v_pct, 2)

## Improved method (log returns) *ask chat why log volatility is better and how does is work?
# def improved_method(close_prices, days_in_period):
#     returns = np.log(close_prices / close_prices.shift(1))
#     v_flt = returns.tail(days_in_period).std()
#     v_pct = v_flt * 100
#     return v_flt, round(v_pct, 2)
