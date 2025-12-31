import pandas as pd
import numpy as np


def get_price_changes(current, closes, days):
    # closing price at the beginning of the period
    start = closes.tail(days).iloc[0]

    usd_change = current - start
    percent_change = (usd_change / start) * 100

    return round(usd_change, 2), round(percent_change, 2)


def get_volatility(closes, days):
    prices = closes.tail(days)
    log_returns = np.log(prices / prices.shift(1))
    v_flt = log_returns.std()
    v_pct = v_flt * 100
    return v_flt, round(v_pct, 2)


def get_MAs(closes, days, window):
    moving_averages = (
        closes.rolling(window=window).mean().dropna().round(2).tail(days).to_list()
    )
    return moving_averages[-1], moving_averages


def get_OBVs(closes, volumes, days):
    prices = closes.tail(days)
    volumes = volumes.tail(days)

    OBVs = [0]

    for i in range(1, days):
        if prices.iloc[i] > prices.iloc[i - 1]:
            OBVs.append(OBVs[-1] + volumes.iloc[i])
        elif prices.iloc[i] < prices.iloc[i - 1]:
            OBVs.append(OBVs[-1] - volumes.iloc[i])
        else:
            OBVs.append(OBVs[-1])

    return OBVs[-1], OBVs


def get_period_high_lows(highs, lows, days):
    highs = highs.tail(days)
    lows = lows.tail(days)
    return round(highs.max(), 2), round(lows.min(), 2)
