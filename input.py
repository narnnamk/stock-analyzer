import yfinance as yf
import pandas as pd


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


def input_ticker():
    print("-" * 100)
    ticker = str(input("Enter the stock ticker: ").strip().replace(" ", "").upper())
    ticker_check = is_valid_ticker(ticker)

    while ticker_check != "valid":
        if ticker_check == "invalid_type":
            print(f"Invalid entry. {ticker} is not a stock/equity ticker.")
        elif ticker_check == "not_enough_data":
            print(
                f"{ticker} does not have enough historical data to perform trend analysis.\n"
                "Specifically, the 200-day moving average, a significant indicator, cannot be calculated."
            )

        print("-" * 100)
        ticker = str(input("Enter the stock ticker: ").strip().replace(" ", "").upper())
        ticker_check = is_valid_ticker(ticker)

    return ticker


def is_valid_period(period, ticker):
    valid_period = ["1mo", "3mo", "6mo", "1y"]
    if period in valid_period:
        if period_covers_history(period, ticker):
            return "valid"
        else:
            return "not_enough_data"
    else:
        return "invalid"


def input_period(ticker):
    valid_period = ["1mo", "3mo", "6mo", "1y"]
    print("-" * 100)
    period = str(
        input(f"{valid_period}\nEnter time period for {ticker}: ")
        .strip()
        .replace(" ", "")
        .lower()
    )
    period_check = is_valid_period(period, ticker)

    while period_check != "valid":
        if period_check == "not_enough_data":
            print(f"{ticker} is relatively new. Please select a shorter time period.")
        else:
            print("Invalid time period. Please choose from the available options.")

        print("-" * 100)
        period = str(
            input(f"{valid_period}\nEnter time period for {ticker}: ")
            .strip()
            .replace(" ", "")
            .lower()
        )
        period_check = is_valid_period(period, ticker)

    return period
