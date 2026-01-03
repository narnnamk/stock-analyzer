from data import *


def input_ticker():
    print("-" * 67)
    ticker = str(input("Enter the stock ticker: ").strip().replace(" ", "").upper())

    loop_ticker_input = True
    while loop_ticker_input:
        while not is_valid_ticker(ticker):
            print("-" * 67)
            ticker = str(
                input("Enter the stock ticker: ").strip().replace(" ", "").upper()
            )
        has_enough_data = period_covers_history("1mo", ticker)
        while not has_enough_data:
            print(
                f"{ticker} does not have enough historical data to perform trend analysis.\n"
                "Specifically, the 200-day moving average, a significant indicator, cannot be calculated."
            )
            print("-" * 67)
            ticker = str(
                input("Enter the stock ticker: ").strip().replace(" ", "").upper()
            )
            has_enough_data = period_covers_history("1mo", ticker)
        loop_ticker_input = False
    print("-" * 67)

    return ticker


def input_period(ticker):
    valid_period = ["1mo", "3mo", "6mo", "1y"]

    print("-" * 67)
    period = str(
        input(f"{valid_period}\nEnter time period for {ticker}: ")
        .strip()
        .replace(" ", "")
        .lower()
    )
    loop_period_input = True

    while loop_period_input:
        while period not in valid_period:
            print("Invalid time period. Please choose from the available options.")
            print("-" * 67)
            period = str(
                input(f"{valid_period}\nEnter time period for {ticker}: ")
                .strip()
                .replace(" ", "")
                .lower()
            )
        has_enough_data = period_covers_history(period, ticker)
        while not has_enough_data:
            print(f"{ticker} is relatively new. Please select a shorter time period.")
            print("-" * 67)
            period = str(
                input(f"{valid_period}\nEnter time period for {ticker}: ")
                .strip()
                .replace(" ", "")
                .lower()
            )
            has_enough_data = period_covers_history(period, ticker)
        loop_period_input = False
    print("-" * 67)
    return period
