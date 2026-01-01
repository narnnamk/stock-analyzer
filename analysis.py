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


# Strong bullish: price > 50 > 200
# Weak bullish: 50 > price > 200
# Transitional: 200 > price > 50
# Bear rally: price > 200 > 50 ← Your question
# Strong bearish: 50 > 200 > price
# Late bearish: 200 > 50 > price
