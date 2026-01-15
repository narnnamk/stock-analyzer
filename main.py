from data import *
from indicators import *
from plots import *
from analysis import *
from output import *
from input import *
import os

print_welcome_message()

ticker = input_ticker()

period = input_period(ticker)

stock = yf.Ticker(ticker)

history = stock.history(period="max")

company_name = get_company_name(stock)

days_in_period = {"1mo": 21, "3mo": 63, "6mo": 126, "1y": 252}
days = days_in_period[period]

dates_in_period = get_dates_in_period(history, days)

current_price, open_prices, high_prices, low_prices, close_prices, volumes = (
    get_history_data(stock, history)
)

usd_change, percent_change = get_price_changes(current_price, close_prices, days)

volatility = get_volatility(close_prices, days)

fifty_MA, fifty_MAs_list = get_MAs(close_prices, days, 50)
two_hundred_MA, two_hundred_MAs_list = get_MAs(close_prices, days, 200)

current_volume = volumes.iloc[-1]
avg_volume = get_avg_volume(volumes, days)
current_OBV, OBVs_list, volume_colors = get_OBVs(close_prices, volumes, days)

period_high, period_low = get_period_high_lows(high_prices, low_prices, days)
high_52wk, low_52wk = get_period_high_lows(
    high_prices, low_prices, days_in_period["1y"]
)

recommendations = get_recommendations(stock)
recommendations_pct = get_recommendations_pct(recommendations)

trend = analyze_trend(current_price, fifty_MA, two_hundred_MA)

momentum = analyze_momentum(percent_change, current_price, high_52wk, low_52wk, period)

market_cap = get_market_cap(stock)
company_size = get_company_size(market_cap)

volatility_level = analyze_volatility(volatility, company_size)

volume_confirmation = get_volume_confirmation(OBVs_list, close_prices, days)

recent_cross = find_recent_cross(fifty_MAs_list, two_hundred_MAs_list)
next_cross = predict_next_cross(fifty_MAs_list, two_hundred_MAs_list, volatility_level)

signal_score = get_signal_score(
    trend, momentum, volume_confirmation, recent_cross, next_cross
)
outlook = interpret_signal_score(signal_score)
confidence_level = get_confidence(trend, momentum, volume_confirmation, recent_cross)


plot_all_charts(
    ticker,
    close_prices,
    days,
    dates_in_period,
    fifty_MAs_list,
    two_hundred_MAs_list,
    volumes,
    current_volume,
    avg_volume,
    volume_colors,
    OBVs_list,
    recommendations_pct,
)

report = get_report(
    ticker,
    company_name,
    period,
    usd_change,
    percent_change,
    current_price,
    period_high,
    period_low,
    volatility,
    volatility_level,
    current_volume,
    avg_volume,
    market_cap,
    fifty_MA,
    two_hundred_MA,
    recent_cross,
    next_cross,
    trend,
    momentum,
    volume_confirmation,
    signal_score,
    outlook,
    confidence_level,
)

# delete charts png
os.remove(f"/Users/narnnamk/stock-analyzer/{ticker}_charts.png")

# ---------------------------------------------------------------------------------------
# variable.                 type        description
# stock                     df          contains all yf library data about a stock given the ticker
# ticker                    str         stock ticker
# history                   df          history dataframe of the stock
# company_name              str         company name
# period                    str         user picked timeframe e.g. 1mo
# days_in_period            dict        key value pair of days in each period e.g. 1mo:30
# dates_in_period           list        list of all trading dates in the period
# current_price             flt         current stock market value
# open_prices               df_col      historical open prices of stock
# close_prices              df_col      historical close prices of stock
# volumes                   df_col      historical volumes of the stock
# usd_change                flt         price changes of the stock from period begin to now
# percent_change            pct         percentage changes of the stock prices from begin to now
# volatility                pct         n-day volatility of the stock price in percentage
# fifty_MA                  flt         current 50-Day MA
# fifty_MAs_list            list        list of 50-day MAs of the days in period
# two_hundred_MA            flt         current 200-Day MA
# two_hundred_MAs_list      list        list of 200-day MAs of the days in period
# current_volume            int         latest volume
# avg_volume                int         average volume over the period
# current_OBV               int         current on balance volume
# OBVs_list                 list        list of on balance volume of the days in period
# volume_colors             list        list of colors according to closing price compared to previous days.
# period_high               flt         highest stock price from the period
# period_low                flt         lowest stock price from the period
# recommendations           dict        dictionary containing expert/financial firms recommendations with keys: strongBuy, buy, hold, sell, strongSell
# recommendations_pct       list        return buy, hold, sell in percent according to recommendations
# trend                     dict key    dictionary key to access trend message with the get_trend_message() function
# momentum                  dict key    dictionary key to access momentum message with the get_momentum_message() function
# market_cap                int         stock's market cap in usd
# company_size              dict key    company size in according to market cap
# volatility_description    dict key    annualized volatility according to company size
# volume_confirmation       str         confirm trend using OBV
# recent_cross              str         the most recent cross
# next_cross                str         prediction of the next cross
# signal_score              int         return signal score out of 100
# outlook                   str         return outlook direction according to signal score
# confidence_level          str         return confidence level on signal scores
# report                    pdf         report of stock analysis with text and charts
