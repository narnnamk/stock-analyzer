# import pandas as pd
import numpy as np
import math


def get_price_changes(current, closes, days):
    # closing price at the beginning of the period
    start = closes.tail(days).iloc[0]

    usd_change = current - start
    percent_change = (usd_change / start) * 100

    return round(usd_change, 2), round(percent_change, 2)


def get_volatility(closes, days):
    prices = closes.tail(days)
    log_returns = np.log(prices / prices.shift(1))
    volatility = log_returns.std() * np.sqrt(252) * 100
    return round(volatility, 2)


def get_MAs(closes, days, window):
    moving_averages = (
        closes.rolling(window=window).mean().dropna().round(2).tail(days).to_list()
    )
    return moving_averages[-1], moving_averages


def get_OBVs(closes, volumes, days):
    prices = closes.tail(days)
    volumes = volumes.tail(days)

    OBVs = [0]
    colors = ["#E48A8AFF", "#FDEEBF", "#BDDDBF"]
    volume_colors = [colors[1]]

    for i in range(1, days):
        if prices.iloc[i] > prices.iloc[i - 1]:
            OBVs.append(OBVs[-1] + volumes.iloc[i])
            volume_colors.append(colors[2])
        elif prices.iloc[i] < prices.iloc[i - 1]:
            OBVs.append(OBVs[-1] - volumes.iloc[i])
            volume_colors.append(colors[0])
        else:
            OBVs.append(OBVs[-1])
            volume_colors.append(colors[1])

    return OBVs[-1], OBVs, volume_colors


def get_period_high_lows(highs, lows, days):
    highs = highs.tail(days)
    lows = lows.tail(days)
    return round(highs.max(), 2), round(lows.min(), 2)


def get_company_size(market_cap):
    if market_cap >= 200_000_000_000:
        return "mega_cap"
    elif market_cap >= 10_000_000_000:
        return "large_cap"
    elif market_cap >= 2_000_000_000:
        return "mid_cap"
    elif market_cap >= 250_000_000:
        return "small_cap"
    else:
        return "micro_cap"


def get_avg_volume(volumes, days):
    volumes = volumes.tail(days)
    return round(volumes.mean())


def get_recommendations_pct(recommendations):
    counts = [
        recommendations["strongBuy"] + recommendations["buy"],
        recommendations["hold"],
        recommendations["strongSell"] + recommendations["sell"],
    ]
    total = sum(counts)

    if total == 0:
        return [0, 0, 0]

    list_pct = [
        (counts[0] / total) * 100,
        (counts[1] / total) * 100,
        (counts[2] / total) * 100,
    ]

    floors = [math.floor(p) for p in list_pct]
    decimals = [list_pct[i] - floors[i] for i in range(3)]

    missing_pct = 100 - sum(floors)

    while missing_pct > 0:
        largest_i = decimals.index(max(decimals))
        floors[largest_i] += 1
        decimals[largest_i] = 0
        missing_pct -= 1

    return floors
