import matplotlib.pyplot as plt
import pandas as pd
from output import shorten_number

plt.rcParams["font.family"] = "Courier"


def get_x_ticks(days, dates):
    if days == 21:
        step = 5
        x_ticks = dates[::step]
    elif days == 63:
        step = 13
        x_ticks = [d[2:] for d in dates[::step]]
    elif days == 126:
        step = 21
        x_ticks = [d[:7] for d in dates[::step]]
    else:
        step = 42
        x_ticks = [d[:7] for d in dates[::step]]

    indices = list(range(0, days, step))
    if indices[-1] != days - 1:
        indices += [days - 1]
        if days == 21:
            x_ticks += [dates[-1]]
        elif days == 63:
            x_ticks += [dates[-1][2:]]
        else:
            x_ticks += [dates[-1][:7]]

    return indices, x_ticks


def get_date_form(days):
    if days == 21:
        return "YYYY-MM-DD"
    elif days == 63:
        return "YY-MM-DD"
    else:
        return "YYYY-MM"


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


def plot_price_MAs(ax, closes, days, dates, fifty_MAs, twoH_MAs):
    closes = closes.tail(days)
    ax.set_title("Close Price with 50/200-Day MA")
    date_form = get_date_form(days)
    ax.set_xlabel(f"Date ({date_form})")
    ax.set_ylabel("Close Price (USD)")
    indices, x_ticks = get_x_ticks(days, dates)
    ax.set_xticks(indices, x_ticks)
    ax.plot(dates, closes, label="Close Prices", color="#555555")
    ax.plot(dates, fifty_MAs, label="50-Day MA", color="#feab3e")
    ax.plot(dates, twoH_MAs, label="200-Day MA", color="#538be4")
    ax.legend(loc="upper left", prop={"family": "monospace", "size": 9})
    ax.set_xlim(0, days - 1)
    ax.grid(True, alpha=0.7, linestyle=":", linewidth=0.5)
    ax.set_axisbelow(True)


def get_abbrv_sf(list):
    abbrv_list = []
    for item in list:
        abbrv_list.append(shorten_number(item))

    suffix = abbrv_list[-1][-1]
    full_sf = get_full_suffix(suffix)

    no_sf_abbrv = []
    for abbrv in abbrv_list:
        if abbrv[-1] in ["K", "M", "B", "T", "Q"]:
            no_sf_abbrv.append(float(abbrv[: len(abbrv) - 1]))
        else:
            no_sf_abbrv.append(float(abbrv))
    return no_sf_abbrv, full_sf


def plot_volumes(ax, volumes, days, curr_vol, avg_vol, dates, colors):
    volumes = list(volumes.tail(days))
    peak_vol = max(volumes)
    stats_text = f"{'Avg Volume':<12}: {shorten_number(avg_vol):>5}\n{'Peak Volume':<12}: {shorten_number(peak_vol):>5}\n{'Current':<12}: {shorten_number(curr_vol):>5}"
    avg_vol = float(shorten_number(avg_vol)[:-1])
    volumes, full_sf = get_abbrv_sf(volumes)

    ax.set_title("Volume")
    date_form = get_date_form(days)
    ax.set_xlabel(f"Date ({date_form})")
    ax.set_ylabel(f"Volume ({full_sf})")
    ax.text(
        0.02,
        0.96,
        stats_text,
        transform=ax.transAxes,
        fontsize=9,
        fontfamily="courier",
        verticalalignment="top",
        horizontalalignment="left",
        bbox=dict(
            boxstyle="round", facecolor="white", alpha=0.9, edgecolor="lightgrey"
        ),
    )
    indices, x_ticks = get_x_ticks(days, dates)
    ax.set_xticks(indices, x_ticks)
    edge_c = ["grey" if days == 21 or days == 63 else "none"]
    line_w = [0.7 if days == 21 else 0.3 if days == 63 else None]
    ax.bar(dates, volumes, color=colors, edgecolor=edge_c, linewidth=line_w)
    ax.axhline(y=avg_vol, linestyle="--", linewidth=1, alpha=1, color="#555555")
    ax.set_xlim(0, days - 1)
    ax.grid(True, alpha=0.7, linestyle=":", linewidth=0.5)
    ax.set_axisbelow(True)


def plot_OBVs(ax, OBVs, days, dates):
    OBVs, full_sf = get_abbrv_sf(OBVs)

    ax.set_title("On-Balance Volume")
    date_form = get_date_form(days)
    ax.set_xlabel(f"Date ({date_form})")
    ax.set_ylabel(f"OBV ({full_sf})")
    indices, x_ticks = get_x_ticks(days, dates)
    ax.set_xticks(indices, x_ticks)
    ax.plot(dates, OBVs, color="#BB72DA")
    ax.set_xlim(0, days - 1)
    ax.grid(True, alpha=0.7, linestyle=":", linewidth=0.5)
    ax.set_axisbelow(True)


def plot_analyst_recommendations(ax, pct):
    labels = ["Sell", "Hold", "Buy"]
    values = [pct[2], pct[1], pct[0]]
    colors = ["#E48A8AFF", "#FDEEBF", "#BDDDBF"]

    ax.set_title("Analyst Recommendations")
    ax.barh(labels, values, color=colors, edgecolor="black", linewidth=1)
    plt.xlim(0, 100)
    ax.set_xlabel("Percent")
    ax.set_xlim(0, 100)
    ax.grid(True, alpha=0.7, linestyle=":", linewidth=0.5)
    ax.set_axisbelow(True)

    for i, v in enumerate(values):
        ax.text((v - 9 if v >= 10 else v + 3), i - 0.05, f"{v}%", size=9)


def plot_all_charts(
    ticker,
    closes,
    days,
    dates,
    fifty_MAs,
    twoH_MAs,
    volumes,
    curr_vol,
    avg_vol,
    vol_colors,
    OBVs,
    pct,
):
    fig, axs = plt.subplots(2, 2, figsize=(12, 7))

    plot_price_MAs(axs[0, 0], closes, days, dates, fifty_MAs, twoH_MAs)
    plot_volumes(axs[0, 1], volumes, days, curr_vol, avg_vol, dates, vol_colors)
    plot_analyst_recommendations(axs[1, 0], pct)
    plot_OBVs(axs[1, 1], OBVs, days, dates)

    plt.tight_layout()
    plt.savefig(f"{ticker}_charts.png", dpi=300, bbox_inches="tight")
