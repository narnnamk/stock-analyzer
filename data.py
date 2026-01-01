import yfinance as yf
import pandas as pd


def is_valid_ticker(ticker):
    stock = yf.Ticker(ticker)
    stock_history = stock.history(period="1d")

    if stock_history.empty:
        return False
    return True


def period_covers_history(period, ticker):
    # Days_needed:
    # Count only trading days
    # Added 200 days buffer to allow 200-days MA calculation
    days_needed = {"1y": 452, "6mo": 326, "3mo": 263, "1mo": 221}
    stock = yf.Ticker(ticker)
    stock_history = stock.history(period="max")

    if stock_history.shape[0] < days_needed["1mo"]:
        return False

    if stock_history.shape[0] < days_needed[period]:
        return False
    return True


def get_history_data(ticker):
    stock = yf.Ticker(ticker)
    stock_history = stock.history(period="max")
    return (
        round(stock.info["regularMarketPrice"], 2),
        stock_history["Open"],
        stock_history["High"],
        stock_history["Low"],
        stock_history["Close"],
        stock_history["Volume"],
    )


def get_recommendations(ticker):
    stock = yf.Ticker(ticker)
    recommendations = stock.recommendations.iloc[0, :].to_dict()
    del recommendations["period"]
    return recommendations
