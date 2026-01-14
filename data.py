# import yfinance as yf
# import pandas as pd


def get_history_data(stock, history):
    return (
        round(stock.info["regularMarketPrice"], 2),
        history["Open"],
        history["High"],
        history["Low"],
        history["Close"],
        history["Volume"],
    )


def get_dates_in_period(history, days):
    dates_times = history.index
    dates_times_str = []
    dates = []
    for dt in dates_times:
        dates_times_str.append(str(dt))
        dates.append(dates_times_str[-1].split(" ")[0])

    dates_in_period = []
    for i in range(-1, -days - 1, -1):
        dates_in_period.append(dates[i])

    dates_in_period.reverse()
    return dates_in_period


def get_recommendations(stock):
    recommendations = stock.recommendations.iloc[0, :].to_dict()
    del recommendations["period"]
    return recommendations


def get_market_cap(stock):
    market_cap = stock.fast_info["marketCap"]
    return market_cap


def get_company_name(stock):
    return stock.info["displayName"]
