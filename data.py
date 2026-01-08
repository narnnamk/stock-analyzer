# import yfinance as yf
# import pandas as pd


def get_history_data(stock):
    stock_history = stock.history(period="max")
    return (
        round(stock.info["regularMarketPrice"], 2),
        stock_history["Open"],
        stock_history["High"],
        stock_history["Low"],
        stock_history["Close"],
        stock_history["Volume"],
    )


def get_recommendations(stock):
    recommendations = stock.recommendations.iloc[0, :].to_dict()
    del recommendations["period"]
    return recommendations


def get_market_cap(stock):
    market_cap = stock.fast_info["marketCap"]
    return market_cap
