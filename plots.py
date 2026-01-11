import matplotlib.pyplot as plt
import pandas as pd
from output import shorten_number


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


def get_full_suffix(suffix):
    if suffix == "K":
        return "Thousand"
    elif suffix == "M":
        return "Million"
    elif suffix == "B":
        return "Billion"
    elif suffix == "T":
        return "Trillion"
    else:
        return "Quadrillion"


# Price + Moving Averages (line chart)
# Use: close_prices (series), fifty_MAs_list, two_hundred_MAs_list
# Optional extras: horizontal lines for period_high and period_low
def plot_price_MAs(closes, days, dates, fifty_MAs, twoH_MAs):
    closes = closes.tail(days)
    plt.figure(figsize=(12, 6))
    plt.title("Close Price with 50/200-Day MA")
    plt.xlabel("Date (YYYY-MM-DD)")
    plt.ylabel("Close Price (USD)")
    indices, x_ticks = get_x_ticks(days, dates)
    plt.xticks(indices, x_ticks)
    plt.plot(dates, closes, label="Close Prices")
    plt.plot(dates, fifty_MAs, label="50-Day MA")
    plt.plot(dates, twoH_MAs, label="200-Day MA")
    plt.legend(loc="best")


def get_abbrv_sf(list):
    abbrv_list = []  # abbreviated volumes
    for item in list:
        abbrv_list.append(shorten_number(item))  # add abbrv form of volume e.g. 5.34M

    suffix = abbrv_list[-1][-1]
    full_sf = get_full_suffix(suffix)

    no_sf_abbrv = []
    for abbrv in abbrv_list:
        if abbrv[-1] in ["K", "M", "B", "T", "Q"]:
            no_sf_abbrv.append(float(abbrv[: len(abbrv) - 1]))
        else:
            no_sf_abbrv.append(float(abbrv))
    return no_sf_abbrv, full_sf


# Volume bars + Avg volume line (best volume chart)
# Use: volumes (series), avg_volume (single number)
# Plot volume as bars.
# Plot a flat line at avg_volume across the whole period.
def plot_volumes(volumes, days, curr_vol, avg_vol, dates):
    volumes = list(volumes.tail(days))
    peak_vol = max(volumes)
    stats_text = f"{'Avg Volume':<12}: {shorten_number(avg_vol):>5}\n{'Peak Volume':<12}: {shorten_number(peak_vol):>5}\n{'Current':<12}: {shorten_number(curr_vol):>5}"
    avg_vol = float(shorten_number(avg_vol)[:-1])
    volumes, full_sf = get_abbrv_sf(volumes)

    plt.figure(figsize=(12, 6))
    plt.title("Volume")
    plt.xlabel("Date (YYYY-MM-DD)")
    plt.ylabel(f"Volume in {full_sf}")
    plt.text(
        0.99,
        0.98,
        stats_text,
        transform=plt.gca().transAxes,
        fontsize=9,
        fontfamily="monospace",
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.7),
    )
    indices, x_ticks = get_x_ticks(days, dates)
    plt.xticks(indices, x_ticks)
    plt.bar(dates, volumes)
    plt.axhline(y=avg_vol, linestyle="--", linewidth=1)


# OBV line (good confirmation chart)
# Use: OBVs_list
# It’s useful when users want “is volume supporting the move?”
def plot_OBVs(OBVs, days, dates):
    OBVs, full_sf = get_abbrv_sf(OBVs)

    plt.figure(figsize=(12, 6))
    plt.title("On-Balance Volume")
    plt.xlabel("Date (YYYY-MM-DD)")
    plt.ylabel(f"OBV in {full_sf}")
    indices, x_ticks = get_x_ticks(days, dates)
    plt.xticks(indices, x_ticks)
    plt.plot(dates, OBVs)


# Expert recommendations as horizontal bar chart
def plot_analyst_recommendations(pct):
    labels = ["Sell", "Hold", "Buy"]
    values = [pct[2], pct[1], pct[0]]

    plt.figure(figsize=(12, 6))
    plt.title("Analyst Recommendations")

    plt.barh(labels, values)
    # plt.xlim(0, 100)
    plt.xlabel("Percent")

    for i, v in enumerate(values):  # label percent number next to the bar
        plt.text(v + 1, i, f"{v:.0f}%")

    # plt.tight_layout()
