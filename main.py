from data import *
from indicators import *
from plots import *
from analysis import *

print('-' * 67)
print('Welcome to Stock Analyzer!')
print('-' * 67)
print("This program provides a comprehensive analysis of a stock.")
print("You can explore the stock's volatility, volume, and moving averages,")
print("view visual graphs, and receive a summary recommendation at the end.")
print('-' * 67)
print('-' * 67)

ticker = str(input('Enter stock ticker: ').strip().replace(' ', '').upper())
while not is_valid_ticker(ticker):
    ticker = str(input('Enter the stock ticker: ').strip().replace(' ', '').upper())

valid_period = ['5d','1mo','3mo','6mo','1y']
period = str(input(f'{valid_period}\nEnter time period: ').strip().replace(' ', '').lower())
has_enough_data = period_covers_history(period, ticker)

while period not in valid_period or not has_enough_data:
    if period not in valid_period:
        print('Invalid time period. Please choose from the available options.')
    if not has_enough_data:
        print(f'{ticker} is relatively new. Please select a shorter time period.')

    period = str(input(f'{valid_period}\nEnter time period: ').strip().replace(' ', '').lower())
    has_enough_data = period_covers_history(period, ticker)


days_in_period = {'5d':5, '1mo':30, '3mo':90, '6mo':180, '1y':365}

current_price, open_prices, close_prices, volumes = get_history_data(ticker)

usd_change, percent_change = get_price_changes(current_price, close_prices, days_in_period[period])

volatility_flt, volatility_percent = get_volatility(close_prices, days_in_period[period])

fifty_MA, fifty_MAs_list = get_MAs(close_prices, days_in_period[period], 50)
two_hundred_MA, two_hundred_MAs_list = get_MAs(close_prices, days_in_period[period], 200)



#---------------------------------------------------------------------------------------
# variable.             type        description
# ticker                str         stock ticker
# period                str         user picked timeframe e.g. 1mo
# days_in_period        dict        key value pair of days in each period e.g. 1mo:30
# current_price         flt         current stock market value
# open_prices           df_col      historical open prices of stock
# close_prices          df_col      historical close prices of stock
# volumes               df_col      historical volumes of the stock
# usd_change            flt         price changes of the stock from period begin to now
# percent_change        pct         percentage changes of the stock prices from begin to now
# volatility_flt        flt         n-day volatility of the stock price
# volatility_flt        pct         n-day volatility of the stock price in percentage
# fifty_MA              flt         current 50-Day MA
# fifty_MAs_list        list        list of 50-day MAs of the last days in period
# two_hundred_MA        flt         current 200-Day MA
# two_hundred_MAs_list  list        list of 200-day MAs of the last days in period


