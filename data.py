import yfinance as yf
import pandas as pd


def is_valid_ticker(ticker):
    stock = yf.Ticker(ticker)
    stock_history = stock.history(period="1d")

    if not stock_history.empty:
        if stock.fast_info["quoteType"] == "EQUITY":
            if period_covers_history("1mo", ticker):
                return "valid"
            else:
                return "not_enough_data"
        else:
            return "invalid_type"
    return "empty_data"


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
