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
        return "strong_buy"
    elif (pc <= pc_th[3]) and (rp <= rp_th[3]):
        return "strong_sell"
    elif (pc > 0) and (rp <= 0.3):
        return "bounce_attempt"
    elif (pc_th[1] <= pc < pc_th[0]) and (rp >= rp_th[1]):
        return "moderate_buy"
    elif (pc_th[2] <= pc <= pc_th[1]) and (rp_th[2] <= rp <= rp_th[1]):
        return "consolidation"
    elif (pc_th[3] < pc <= pc_th[2]) and (rp <= rp_th[2]):
        return "weak_sell"
    else:
        return "mixed_signal"


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


def get_volume_confirmation(OBVs_list, close_prices, days):
    up_days = 0
    down_days = 0
    for i in range(-1, -days + 1, -1):
        if close_prices.iloc[i] > close_prices.iloc[i - 1]:
            up_days += 1
        elif close_prices.iloc[i] < close_prices.iloc[i - 1]:
            down_days += 1
    price_direction = None
    if up_days > days * 0.6:
        price_direction = "up"
    elif down_days > days * 0.6:
        price_direction = "down"
    else:
        price_direction = "flat"

    up_obv = 0
    down_obv = 0
    for i in range(-1, -len(OBVs_list) + 1, -1):
        if OBVs_list[i] > OBVs_list[i - 1]:
            up_obv += 1
        elif OBVs_list[i] < OBVs_list[i - 1]:
            down_obv += 1
    OBV_direction = None
    if up_obv > len(OBVs_list) * 0.6:
        OBV_direction = "up"
    elif down_obv > len(OBVs_list) * 0.6:
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


def find_recent_cross(fifty_MAs, two_hundred_MAs):
    for i in range(len(fifty_MAs) - 1, 0, -1):
        prev_50 = fifty_MAs[i - 1]
        prev_200 = two_hundred_MAs[i - 1]
        curr_50 = fifty_MAs[i]
        curr_200 = two_hundred_MAs[i]

        if prev_50 < prev_200 and curr_50 > curr_200:
            return "golden_cross"

        if prev_50 > prev_200 and curr_50 < curr_200:
            return "death_cross"

    return "no_cross"


def predict_next_cross(fifty_MAs, two_hundred_MAs):
    prev_gap = fifty_MAs[-2] - two_hundred_MAs[-2]
    curr_gap = fifty_MAs[-1] - two_hundred_MAs[-1]

    if abs(curr_gap) < abs(prev_gap):
        if prev_gap > 0 and curr_gap > 0 and curr_gap < prev_gap:
            return "possible_death_cross"

        if prev_gap < 0 and curr_gap < 0 and curr_gap > prev_gap:
            return "possible_golden_cross"

    return "no_upcoming_cross"


def get_signal_score(trend, momentum, volume_confirmation, recent_cross, next_cross):
    """
    Calculate stock score based on multiple technical indicators.
    Score range: 0-100 (normalized from -10 to +10 internal scale)
    """
    trend_score = {
        "strong_bullish": 3,
        "weak_bullish": 2,
        "transitional": 0,
        "bear_rally": 1,
        "late_bearish": -2,
        "strong_bearish": -3,
        "neutral": 0,
    }

    momentum_score = {
        "strong_buy": 2,
        "moderate_buy": 1,
        "bounce_attempt": 0,
        "consolidation": 0,
        "mixed_signal": 0,
        "weak_sell": -1,
        "strong_sell": -2,
    }

    volume_score = {
        "bullish_confirm": 2,
        "accumulation": 1,
        "weak_bullish": 1,
        "consolidation": 0,
        "bearish_divergence": -1,
        "distribution": -1,
        "weak_bearish": -1,
        "bearish_confirm": -2,
        "bullish_divergence": 1.5,
    }

    cross_score = {
        "golden_cross": 2,
        "possible_golden_cross": 1,
        "no_cross": 0,
        "no_upcoming_cross": 0,
        "possible_death_cross": -1,
        "death_cross": -2,
    }

    recent_weight = 0.7
    next_weight = 0.3

    weighted_cross = (
        cross_score[recent_cross] * recent_weight
        + cross_score[next_cross] * next_weight
    )

    score = (
        trend_score[trend]
        + momentum_score[momentum]
        + volume_score[volume_confirmation]
        + weighted_cross
    )

    max_score = 3 + 2 + 2 + (2 * 0.7 + 1 * 0.3)
    min_score = -3 + -2 + -2 + (-2 * 0.7 + -1 * 0.3)

    signal_score = round(((score - min_score) / (max_score - min_score)) * 100)

    signal_score = max(0, min(100, signal_score))

    return signal_score


def interpret_signal_score(score):
    if score >= 75:
        return "strong_bullish"
    elif score >= 60:
        return "bullish"
    elif score >= 40:
        return "neutral"
    elif score >= 25:
        return "bearish"
    else:
        return "strong_bearish"


def get_confidence(trend, momentum, volume_confirmation, recent_cross):
    bullish_confirmations = 0
    bearish_confirmations = 0

    if trend in ["strong_bullish", "weak_bullish", "bear_rally"]:
        bullish_confirmations += 1
    if momentum in ["strong_buy_momentum", "moderate_buy_momentum"]:
        bullish_confirmations += 1
    if volume_confirmation in ["bullish_confirm", "accumulation", "bullish_divergence"]:
        bullish_confirmations += 1
    if recent_cross in ["golden_cross", "possible_golden_cross"]:
        bullish_confirmations += 1

    if trend in ["strong_bearish", "late_bearish"]:
        bearish_confirmations += 1
    if momentum in ["strong_sell_momentum", "weak_sell_momentum"]:
        bearish_confirmations += 1
    if volume_confirmation in ["bearish_confirm", "distribution", "bearish_divergence"]:
        bearish_confirmations += 1
    if recent_cross in ["death_cross", "possible_death_cross"]:
        bearish_confirmations += 1

    max_confirmations = max(bullish_confirmations, bearish_confirmations)

    if max_confirmations >= 3:
        confidence = "High"
    elif max_confirmations == 2:
        confidence = "Moderate"
    else:
        confidence = "Low"

    return confidence
