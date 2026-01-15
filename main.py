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

get_report(
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

os.remove(f"/Users/narnnamk/stock-analyzer/{ticker}_charts.png")
print(
    f"{ticker} stock analysis report was generated and saved as '{ticker}_Report.pdf' in this directory."
)
print("=" * 100)

# ---------------------------------------------------------------------------------------
# variable                 type                 description
# stock                    yf.Ticker            yfinance Ticker object for the symbol (used to fetch data)
# ticker                   str                  stock ticker symbol (e.g., "TSLA")
# history                  pd.DataFrame         historical OHLCV dataframe for the selected period
# company_name             str                  company name

# period                   str                  selected timeframe: "1mo", "3mo", "6mo", "1y"
# days_in_period           dict[str, int]       map of period -> trading days used in your logic (1mo:21, 3mo:63, 6mo:126, 1y:252)
# dates_in_period          list[str]            trading dates in the period as "YYYY-MM-DD" (aligned to your plotted data)

# current_price            float                latest close price used in the summary
# open_prices              pd.Series            historical open prices (aligned to history index)
# close_prices             pd.Series            historical close prices (aligned to history index)
# volumes                  pd.Series            historical volume values (aligned to history index)

# usd_change               float                price change from period start to latest (USD)
# percent_change           float                percent change from period start to latest (e.g., 4.18 means 4.18%)
# volatility               float                annualized volatility in percent (e.g., 43.12 means 43.12%)

# fifty_MA                 float                latest 50-day moving average value
# fifty_MAs_list           list[float]          50-day MA values across the selected period (aligned to dates_in_period)
# two_hundred_MA           float                latest 200-day moving average value
# two_hundred_MAs_list     list[float]          200-day MA values across the selected period (aligned to dates_in_period)

# current_volume           int                  latest trading day volume
# avg_volume               float                average volume over the selected period
# current_OBV              float                latest On-Balance Volume value (can be negative)
# OBVs_list                list[float]          OBV values across the selected period (aligned to dates_in_period)
# volume_colors            list[str]            color label per day based on close vs previous close (e.g., "green"/"red")

# period_high              float                highest price in the selected period
# period_low               float                lowest price in the selected period

# recommendations          dict[str, int]       analyst rating counts from yfinance: strongBuy, buy, hold, sell, strongSell
# recommendations_pct      dict[str, float]     buy/hold/sell distribution in percent: {"buy": x, "hold": y, "sell": z}

# trend                    str                  trend key from analyze_trend() (e.g., "strong_bullish")
# momentum                 str                  momentum key from analyze_momentum() (e.g., "mixed_signal")

# market_cap               int                  market capitalization in USD
# company_size             str                  company size label derived from market cap (e.g., "mega_cap", "large_cap", etc.)
# volatility_description   str                  volatility level key from analyze_volatility() (e.g., "very_high")

# volume_confirmation      str                  volume/OBV confirmation key (e.g., "bullish_confirm", "consolidation")
# recent_cross             str                  most recent MA cross key (e.g., "golden_cross", "no_cross")
# next_cross               str                  predicted next MA cross key (e.g., "possible_death_cross", "no_upcoming_cross")

# signal_score             int                  overall signal score (0–100)
# outlook                  str                  outlook key derived from signal score (e.g., "bullish")
# confidence_level         str                  confidence label ("High", "Moderate", "Low")

# report_path              str                  generated PDF output file path (e.g., "TSLA_Report.pdf")
# ---------------------------------------------------------------------------------------
