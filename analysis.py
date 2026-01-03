import pandas as pd
import numpy as np


def analyze_trend(price, fifty_MA, two_hundred_MA):
    if price > fifty_MA > two_hundred_MA:
        return "strong_bullish"
    elif fifty_MA > price > two_hundred_MA:
        return "weak_bullish"
    elif two_hundred_MA > price > fifty_MA:
        return "transitional"
    elif price > two_hundred_MA > fifty_MA:
        return "bear_rally"
    elif two_hundred_MA > fifty_MA > price:
        return "late_bearish"
    elif fifty_MA > two_hundred_MA > price:
        return "strong_bearish"
    else:
        return "neutral"


def get_trend_message(trend, ticker):
    message = {
        "strong_bullish": (
            f"STRONGLY BULLISH:\n{ticker} is trading above both the 50-day and 200-day moving averages, "
            "with the 50-day above the 200-day (golden cross).\n"
            "This indicates a healthy uptrend with strong momentum across multiple timeframes."
        ),
        "weak_bullish": (
            f"WEAK BULLISH:\n{ticker} is below the 50-day MA but above the 200-day, "
            "suggesting a pullback within an overall uptrend.\n"
            "Watch for support at the 200-day MA or a bounce back above the 50-day to resume the uptrend."
        ),
        "transitional": (
            f"TRANSITIONAL:\n{ticker} is trading between the 200-day and 50-day moving averages with the 200-day above the 50-day.\n"
            "This neutral zone suggests indecision—price could break up to challenge the bearish structure or fall back into the downtrend."
        ),
        "bear_rally": (
            f"BEAR RALLY:\n{ticker} is trading above both moving averages but the 200-day is above the 50-day (death cross still intact).\n"
            "This may be a temporary rally in a bear market or early signs of trend reversal.\n"
            "Caution is warranted as the long-term structure remains bearish."
        ),
        "late_bearish": (
            f"LATE BEARISH:\n{ticker} is trading below both the 50-day and 200-day moving averages, with the 200-day falling below the 50-day.\n"
            "This late-stage downtrend may signal exhaustion or a potential bottoming process, though caution is still advised."
        ),
        "strong_bearish": (
            f"STRONGLY BEARISH:\n{ticker} is trading below both moving averages with the 50-day below the 200-day (death cross).\n"
            "This indicates a confirmed downtrend with selling pressure across multiple timeframes.\n"
            "Further downside is likely unless price can reclaim key support levels."
        ),
        "neutral": (
            f"NEUTRAL:\n{ticker} is trading near its moving averages with no clear trend.\n"
            "The price is consolidating with neither bulls nor bears in control.\n"
            "Wait for a decisive break above resistance or below support before taking directional positions."
        ),
    }
    return message[trend]


def analyze_momentum(percent_change, price, high, low, period):
    percent_thresholds = {
        "1mo": [8, 3, -3, -8],
        "3mo": [15, 6, -6, -15],
        "6mo": [20, 8, -8, -20],
        "1y": [30, 12, -12, -30],
    }
    period_percent_threshold = percent_thresholds[period]

    if high == low:
        return "no_movement"

    range_position = round((price - low) / (high - low), 2)
    range_position_threshold = [0.8, 0.6, 0.4, 0.2]

    pc = percent_change
    pc_th = period_percent_threshold
    rp = range_position
    rp_th = range_position_threshold

    if (pc >= pc_th[0]) and (rp >= rp_th[0]):
        return "strong_buy_momentum"
    elif (pc <= pc_th[3]) and (rp <= rp_th[3]):
        return "strong_sell_momentum"
    elif (pc > 0) and (rp <= 0.3):
        return "bounce_attempt"
    elif (pc_th[1] <= pc < pc_th[0]) and (rp >= rp_th[1]):
        return "moderate_buy_momentum"
    elif (pc_th[2] <= pc <= pc_th[1]) and (rp_th[2] <= rp <= rp_th[1]):
        return "consolidation"
    elif (pc_th[3] < pc <= pc_th[2]) and (rp <= rp_th[2]):
        return "weak_sell_momentum"
    else:
        return "mixed_signal"


def get_momentum_message(momentum, ticker):
    messages = {
        "strong_buy_momentum": (
            f"{ticker} shows strong bullish momentum.\n"
            "Price is near the period high with a large positive gain, suggesting aggressive buying pressure."
        ),
        "moderate_buy_momentum": (
            f"{ticker} shows moderate bullish momentum.\n"
            "Price is trending higher with decent gains and positioned above the midpoint, "
            "suggesting sustained buying interest without overheating."
        ),
        "bounce_attempt": (
            f"{ticker} may be attempting a bounce from recent lows.\n"
            "Price shows positive change despite being in the lower range, "
            "but this is an early signal requiring confirmation from follow-through."
        ),
        "consolidation": (
            f"{ticker} is consolidating.\n"
            "Price movement is minimal with trading near the middle of its recent range, "
            "suggesting equilibrium between buyers and sellers."
        ),
        "weak_sell_momentum": (
            f"{ticker} shows weak bearish momentum.\n"
            "Price is drifting lower and positioned below the midpoint, "
            "indicating mild selling pressure without panic."
        ),
        "strong_sell_momentum": (
            f"{ticker} shows strong bearish momentum.\n"
            "Price is near the period low with a large negative change, indicating heavy selling pressure."
        ),
        "mixed_signal": (
            f"{ticker} shows mixed momentum signals.\n"
            "Price position and percentage change are not aligned, "
            "suggesting uncertainty or transition between trends."
        ),
        "no_movement": (
            f"{ticker} traded flat during this period with no significant price range."
        ),
    }
    return messages[momentum]


def analyze_volatility(volatility, company_size):
    volatility_thresholds = {
        "mega_cap": [0.5, 0.8, 1.2, 1.8],
        "large_cap": [0.6, 1.0, 1.5, 2.2],
        "mid_cap": [0.8, 1.2, 1.8, 2.8],
        "small_cap": [1.0, 1.5, 2.2, 3.5],
        "micro_cap": [1.5, 2.0, 3.0, 5.0],
    }
    vt = volatility_thresholds[company_size]

    if volatility <= vt[0]:
        return "very_low"
    elif volatility <= vt[1]:
        return "low"
    elif volatility <= vt[2]:
        return "moderate"
    elif volatility <= vt[3]:
        return "high"
    else:
        return "very_high"


def get_volatility_message(volatility_description, ticker):
    messages = {
        "very_low": (
            f"{ticker} shows very low volatility.\n"
            "Price movements are exceptionally small and stable, suggesting minimal risk "
            "but also limited short-term price appreciation potential."
        ),
        "low": (
            f"{ticker} has low volatility.\n"
            "The stock is relatively stable with modest price fluctuations, "
            "typical of established companies or defensive sectors."
        ),
        "moderate": (
            f"{ticker} is experiencing moderate volatility.\n"
            "Price movements are noticeable, offering a balance between risk and potential returns."
        ),
        "high": (
            f"{ticker} shows high volatility.\n"
            "The stock experiences sharp price swings, indicating elevated risk "
            "but also potential short-term trading opportunities."
        ),
        "very_high": (
            f"{ticker} has very high volatility.\n"
            "Extreme price fluctuations suggest significant risk, speculative activity, "
            "and potential for large gains or losses in short periods."
        ),
    }
    return messages[volatility_description]


def get_trend_confirmation(OBVs_list, close_prices, days):
    higher_close = 0
    for i in range(-1, -days + 1, -1):
        if close_prices.iloc[i] > close_prices.iloc[i - 1]:
            higher_close += 1
    price_direction = None
    if higher_close > days * 0.6:
        price_direction = "up"
    elif higher_close < days * 0.4:
        price_direction = "down"
    else:
        price_direction = "flat"

    higher_obv = 0
    for i in range(-1, -len(OBVs_list) + 1, -1):
        if OBVs_list[i] > OBVs_list[i - 1]:
            higher_obv += 1
    OBV_direction = None
    if higher_obv > len(OBVs_list) * 0.6:
        OBV_direction = "up"
    elif higher_obv < len(OBVs_list) * 0.4:
        OBV_direction = "down"
    else:
        OBV_direction = "flat"

    if price_direction == "up" and OBV_direction == "up":
        return "bullish_confirm"
    elif price_direction == "down" and OBV_direction == "down":
        return "bearish_confirm"
    elif price_direction == "up" and OBV_direction == "down":
        return "bearish_divergence"
    elif price_direction == "down" and OBV_direction == "up":
        return "bullish_divergence"
    elif price_direction == "flat" and OBV_direction == "up":
        return "accumulation"
    elif price_direction == "flat" and OBV_direction == "down":
        return "distribution"
    elif price_direction == "up" and OBV_direction == "flat":
        return "weak_bullish"
    elif price_direction == "down" and OBV_direction == "flat":
        return "weak_bearish"
    else:
        return "consolidation"
