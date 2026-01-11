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


# Volume bars + Avg volume line (best volume chart)
# Use: volumes (series), avg_volume (single number)
# Plot volume as bars.
# Plot a flat line at avg_volume across the whole period.
def plot_volumes(volumes, days, curr_vol, avg_vol, dates):
    volumes = list(volumes.tail(days))
    peak_vol = max(volumes)
    stats_text = f"{'Avg Volume':<12}: {shorten_number(avg_vol):>5}\n{'Peak Volume':<12}: {shorten_number(peak_vol):>5}\n{'Current':<12}: {shorten_number(curr_vol):>5}"
    avg_vol = float(shorten_number(avg_vol)[:-1])

    abbrv_volumes = []  # abbreviated volumes
    for volume in volumes:
        abbrv_volumes.append(
            shorten_number(volume)
        )  # add abbrv form of volume e.g. 5.34M

    suffix = abbrv_volumes[0][-1]
    full_sf = get_full_suffix(suffix)

    no_sf_abbrv_volumes = []
    for abbrv in abbrv_volumes:
        if abbrv[-1] in ["K", "M", "B", "T", "Q"]:
            no_sf_abbrv_volumes.append(float(abbrv[: len(abbrv) - 1]))
        else:
            no_sf_abbrv_volumes.append(float(abbrv))

    volumes = no_sf_abbrv_volumes

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
    abbrv_OBVs = []
    for obv in OBVs:
        abbrv_OBVs.append(shorten_number(obv))

    suffix = abbrv_OBVs[0][-1]
    full_sf = get_full_suffix(suffix)

    no_sf_abbrv_OBVs = []
    for abbrv in abbrv_OBVs:
        if abbrv[-1] in ["K", "M", "B", "T", "Q"]:
            no_sf_abbrv_OBVs.append(float(abbrv[: len(abbrv) - 1]))
        else:
            no_sf_abbrv_OBVs.append(float(abbrv))

    OBVs = no_sf_abbrv_OBVs

    plt.figure(figsize=(12, 6))
    plt.title("On-Balance Volume")
    plt.xlabel("Date (YYYY-MM-DD)")
    plt.ylabel(f"OBV in {full_sf}")
    indices, x_ticks = get_x_ticks(days, dates)
    plt.xticks(indices, x_ticks)
    plt.plot(dates, OBVs)


# Expert recommendations as horizontal bar chart
