from data import *
from indicators import *
from plots import *
from analysis import *


print("-" * 67)
print("Welcome to Stock Analyzer!")
print("-" * 67)
print("This program provides a comprehensive analysis of a stock.")
print("You can explore the stock's volatility, volume, and moving averages,")
print("view visual graphs, and receive a summary recommendation at the end.")
print(
    "Note: 1mo = 21 trading days, 3mo = 63 trading days, 6mo = 126 trading days, and 1y = 252 trading days."
)
print("-" * 67)
print("-" * 67)

ticker = str(input("Enter the stock ticker: ").strip().replace(" ", "").upper())
loop_ticker_input = True


while loop_ticker_input:
    while not is_valid_ticker(ticker):
        print("-" * 67)
        ticker = str(input("Enter the stock ticker: ").strip().replace(" ", "").upper())
    has_enough_data = period_covers_history("1mo", ticker)
    while not has_enough_data:
        print(
            f"{ticker} does not have enough historical data to perform trend analysis.\n"
            "Specifically, the 200-day moving average, a significant indicator, cannot be calculated."
        )
        print("-" * 67)
        ticker = str(input("Enter the stock ticker: ").strip().replace(" ", "").upper())
        has_enough_data = period_covers_history("1mo", ticker)
    loop_ticker_input = False


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

stock = yf.Ticker(ticker)

days_in_period = {"1mo": 21, "3mo": 63, "6mo": 126, "1y": 252}

current_price, open_prices, high_prices, low_prices, close_prices, volumes = (
    get_history_data(stock)
)

usd_change, percent_change = get_price_changes(
    current_price, close_prices, days_in_period[period]
)

volatility = get_volatility(close_prices, days_in_period[period])

fifty_MA, fifty_MAs_list = get_MAs(close_prices, days_in_period[period], 50)
two_hundred_MA, two_hundred_MAs_list = get_MAs(
    close_prices, days_in_period[period], 200
)

current_OBV, OBVs_list = get_OBVs(close_prices, volumes, days_in_period[period])

period_high, period_low = get_period_high_lows(
    high_prices, low_prices, days_in_period[period]
)
high_52wk, low_52wk = get_period_high_lows(
    high_prices, low_prices, days_in_period["1y"]
)

expert_comments = get_recommendations(stock)

trend = analyze_trend(current_price, fifty_MA, two_hundred_MA)
trend_message = get_trend_message(trend, ticker)

momentum = analyze_momentum(percent_change, current_price, high_52wk, low_52wk, period)
momentum_message = get_momentum_message(momentum, ticker)

market_cap = get_market_cap(stock)
company_size = get_company_size(market_cap)


print(company_size)
print("yay")


# ---------------------------------------------------------------------------------------
# variable.             type        description
# stock                 df          contains all yf library data about a stock given the ticker
# ticker                str         stock ticker
# period                str         user picked timeframe e.g. 1mo
# days_in_period        dict        key value pair of days in each period e.g. 1mo:30
# current_price         flt         current stock market value
# open_prices           df_col      historical open prices of stock
# close_prices          df_col      historical close prices of stock
# volumes               df_col      historical volumes of the stock
# usd_change            flt         price changes of the stock from period begin to now
# percent_change        pct         percentage changes of the stock prices from begin to now
# volatility            pct         n-day volatility of the stock price in percentage
# fifty_MA              flt         current 50-Day MA
# fifty_MAs_list        list        list of 50-day MAs of the days in period
# two_hundred_MA        flt         current 200-Day MA
# two_hundred_MAs_list  list        list of 200-day MAs of the days in period
# current_OBV           int         current on balance volume
# OBVs_list             list        list of on balance volume of the days in period
# period_high           flt         highest stock price from the period
# period_low            flt         lowest stock price from the period
# expert_comments       dict        dictionary containing expert/financial firms recommendations with keys: strongBuy, buy, hold, sell, strongSell
# trend                 dict key    dictionary key to access trend message with the get_trend_message() function
# trend_message         str         return a trend analysis and some trend interpretation
# momentum              dict key    dictionary key to access momentum message with the get_momentum_message() function
# momentum_message      str         return a momentum analysis and some momentum interpretation
# market_cap            int         stock's market cap in usd
# company_size          str         company size in according to market cap
