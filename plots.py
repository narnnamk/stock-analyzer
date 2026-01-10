import matplotlib.pyplot as plt
import pandas as pd


def get_x_ticks(days, dates):
    if days == 21:  # 1mo
        step = 5
    elif days == 63:  # 3mo
        step = 13
    elif days == 126:  # 6mo
        step = 21
    else:  # 1y
        step = 42

    indices = list(range(0, days, step))
    x_ticks = dates[::step]
    if indices[-1] != days - 1:
        indices += [days - 1]
        x_ticks += [dates[-1]]

    return indices, x_ticks


# Price + Moving Averages (line chart)
# Use: close_prices (series), fifty_MAs_list, two_hundred_MAs_list
# Optional extras: horizontal lines for period_high and period_low


def plot_price_MAs(closes, days, dates, fifty_MAs, twoH_MAs):
    closes = closes.tail(days)
    indices, x_ticks = get_x_ticks(days, dates)
    plt.figure(figsize=(12, 6))
    plt.title("Close Price with 50/200-Day MA")
    plt.xlabel("Date (YYYY-MM-DD)")
    plt.ylabel("Close Price (USD)")
    plt.xticks(indices, x_ticks)
    plt.plot(dates, closes, label="Close Prices")
    plt.plot(dates, fifty_MAs, label="50-Day MA")
    plt.plot(dates, twoH_MAs, label="200-Day MA")
    plt.legend(loc="best")


# Volume bars + Avg volume line (best volume chart)
# Use: volumes (series), avg_volume (single number)
# Plot volume as bars.
# Plot a flat line at avg_volume across the whole period.

# OBV line (good confirmation chart)
# Use: OBVs_list
# It’s useful when users want “is volume supporting the move?”

# Expert recommendations as horizontal bar chart
