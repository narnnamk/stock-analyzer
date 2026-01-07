def print_welcome_message():
    print("-" * 100)
    print("Welcome to Stock Analyzer!")
    print("-" * 100)
    print("This program provides a comprehensive analysis of a stock.")
    print("You can explore the stock's volatility, volume, and moving averages,")
    print("view visual graphs, and receive a summary recommendation at the end.")
    print(
        "Note: 1mo = 21 trading days, 3mo = 63 trading days, 6mo = 126 trading days, and 1y = 252 trading days."
    )
    print("-" * 100)


def remove_decimals(num):
    num = num.rstrip("0").rstrip(".")

    if "." not in num:
        return num

    whole = num.split(".")[0]

    if len(whole) >= 3:
        return whole
    elif len(whole) >= 2:
        return f"{float(num):.1f}".rstrip("0").rstrip(".")
    else:
        return num


def shorten_number(num):
    units = [
        (1_000_000_000_000_000, "Q"),
        (1_000_000_000_000, "T"),
        (1_000_000_000, "B"),
        (1_000_000, "M"),
        (1_000, "K"),
    ]

    for value, suffix in units:
        if num >= value:
            num = f"{num / value:.2f}"
            return f"{remove_decimals(num)}{suffix}"

    return num


def print_quick_overview(
    ticker,
    period,
    market_cap,
    size,
    price,
    usd_change,
    pct_change,
    curr_volume,
    avg_volume,
    high,
    low,
    volatility,
    volatility_level,
    days,
    fifty_MA,
    twoH_MA,
):
    print("=" * 100)
    print("STOCK ANALYZER")
    print(f"Ticker: {ticker} | Period: {period}")
    print("=" * 100)
    print("Quick Overview")
    print("-" * 100)
    print(f"Market Cap: {shorten_number(market_cap)}")
    print(f"Company Size: {size.replace('_', ' ').title()}\n")
    print(f"Current Price: ${price}")
    print(
        f"Change: {'+' if usd_change >= 0 else '-'}${abs(usd_change)} ({'+' if pct_change >= 0 else '-'}{abs(pct_change)}%)\n"
    )
    print(f"Volume: {shorten_number(curr_volume)}")
    print(f"Average Volume: {shorten_number(avg_volume)}\n")
    print(f"Period High: ${high}")
    print(f"Period Low: ${low}")
    print(
        f"Volatility ({days}-Day): {volatility}% ({volatility_level.replace('_', ' ').title()})\n"
    )
    print(f"50-Day MA: ${fifty_MA}")
    print(f"200-day MA: ${twoH_MA}")
    print("=" * 100)


def print_trend_message(trend):
    messages = {
        "strong_bullish": (
            "STRONG BULLISH - "
            "Price is above both the 50-day MA and 200-day MA.\n"
            "That usually signals strong upward structure and healthy momentum.\n"
            "As long as price holds above the 50-day MA, the trend remains in control."
        ),
        "weak_bullish": (
            "WEAK BULLISH - "
            "Price is below the 50-day MA, but still above the 200-day MA.\n"
            "This often happens during a pullback inside a bigger uptrend.\n"
            "A move back above the 50-day MA would strengthen the bullish case."
        ),
        "transitional": (
            "TRANSITIONAL - "
            "Price is above the 50-day MA, but still below the 200-day MA.\n"
            "That can signal an early recovery attempt, but the long-term trend is not confirmed.\n"
            "Breaking and holding above the 200-day MA would be a stronger trend shift."
        ),
        "bear_rally": (
            "BEAR RALLY - "
            "Price is above the 200-day MA, but the 200-day MA is also sitting above the 50-day MA.\n"
            "That means price has bounced, but the medium-term trend is still lagging behind.\n"
            "If the 50-day MA starts rising back above the 200-day MA, the trend improves."
        ),
        "late_bearish": (
            "LATE BEARISH - "
            "Both moving averages are above price, with the 200-day MA above the 50-day MA.\n"
            "That usually points to a longer-term downtrend that is still in control.\n"
            "A sustained move back above the 50-day MA would be the first sign of improvement."
        ),
        "strong_bearish": (
            "STRONG BEARISH - "
            "The 50-day MA is above the 200-day MA, and both are above price.\n"
            "That often signals strong downside pressure and aggressive selling phases.\n"
            "Price would need to reclaim the 200-day MA to reduce the bearish outlook."
        ),
        "neutral": (
            "NEUTRAL - "
            "Price and the 50/200-day MAs are not in a clean bullish or bearish structure.\n"
            "This can happen during sideways markets or choppy transitions.\n"
            "Waiting for a clearer alignment can help avoid false signals."
        ),
    }

    return print(f"Trend:\n{messages[trend]}\n")


def print_momentum_message(momentum):
    messages = {
        "strong_buy": (
            "STRONG BUY - "
            "The percent gain for this period is high, and price is trading near the top of its range.\n"
            "That usually means buyers are in control and the move has strength.\n"
            "Be careful with sudden pullbacks after strong runs."
        ),
        "moderate_buy": (
            "MODERATE BUY - "
            "The percent gain is solid for the period, and price is in the upper part of the range.\n"
            "This suggests steady buying pressure and healthy trend continuation.\n"
            "Holding in the upper range keeps the momentum strong."
        ),
        "bounce_attempt": (
            "BOUNCE ATTEMPT - "
            "The period return is positive, but price is still close to the lower part of the range.\n"
            "That can happen when a stock is trying to recover after weakness.\n"
            "A push toward the middle or upper range would confirm stronger momentum."
        ),
        "consolidation": (
            "CONSOLIDATION - "
            "Price is sitting around the middle of the range without a strong percent move.\n"
            "This often means the market is undecided right now.\n"
            "A break out of the range is usually the next important signal."
        ),
        "weak_sell": (
            "WEAK SELL - "
            "The period return is negative and price is sitting in the lower part of its range.\n"
            "Sellers have an advantage, but it does not look like a full breakdown yet.\n"
            "A recovery back toward the mid-range would improve the signal."
        ),
        "strong_sell": (
            "STRONG SELL - "
            "The percent drop for this period is large, and price is near the bottom of its range.\n"
            "This often signals strong selling pressure and weak demand.\n"
            "It usually takes a strong reversal to shift this momentum."
        ),
        "mixed_signal": (
            "MIXED SIGNAL - "
            "The percent change and the range position do not line up into a strong setup.\n"
            "This can happen in choppy markets where price swings both ways.\n"
            "Waiting for a cleaner signal may reduce false entries."
        ),
        "no_movement": (
            "NO MOVEMENT - "
            "The high and low are the same, so the range is flat.\n"
            "This can happen with very low volume or limited data.\n"
            "Momentum cannot be judged reliably in this situation."
        ),
    }

    return print(f"Momentum:\n{messages[momentum]}\n")


def print_volume_message(volume_confirmation: str):
    messages = {
        "bullish_confirm": (
            "BULLISH CONFIRM - Volume confirms the bullish move.\n"
            "Price has been trending up and OBV is also rising.\n"
            "That usually means buying pressure is supporting the uptrend."
        ),
        "bearish_confirm": (
            "BEARISH CONFIRM - Volume confirms the bearish move.\n"
            "Price has been trending down and OBV is also falling.\n"
            "That usually means selling pressure is supporting the downtrend."
        ),
        "bearish_divergence": (
            "BEARISH DIVERGENCE - "
            "Price is moving up, but OBV is moving down.\n"
            "That can mean the rally is not supported by real buying pressure.\n"
            "Be cautious, because this setup can lead to pullbacks or reversals."
        ),
        "bullish_divergence": (
            "BULLISH DIVERGENCE - "
            "Price is moving down, but OBV is moving up.\n"
            "That can mean buyers are quietly stepping in while price is still weak.\n"
            "If price stabilizes, this can be an early reversal clue."
        ),
        "accumulation": (
            "ACCUMULATION - "
            "Price is mostly flat, but OBV is trending up.\n"
            "That can mean investors are buying in the background without moving price much.\n"
            "A breakout is more likely if this accumulation continues."
        ),
        "distribution": (
            "DISTRIBUTION - "
            "Price is mostly flat, but OBV is trending down.\n"
            "That can mean selling is happening quietly while price still looks stable.\n"
            "A breakdown is more likely if this distribution continues."
        ),
        "weak_bullish": (
            "WEAK BULLISH - "
            "Price is trending up, but OBV is mostly flat.\n"
            "That can mean the move is drifting higher without strong demand.\n"
            "This trend can continue, but it is easier to fade if buyers do not step in."
        ),
        "weak_bearish": (
            "WEAK BEARISH - "
            "Price is trending down, but OBV is mostly flat.\n"
            "That can mean the drop is happening without strong selling pressure.\n"
            "This can turn into a bounce if buyers show up."
        ),
        "consolidation": (
            "CONSOLIDATION - "
            "Neither price nor OBV is showing a strong direction.\n"
            "This often happens during consolidation and indecision.\n"
            "Waiting for a clear volume shift can help confirm the next move."
        ),
    }

    return print(
        f"Volume:\n{messages.get(volume_confirmation, 'Volume explanation is unavailable right now.')}\n"
    )


def print_MA_cross(recent, next):
    print("MA Cross:")
    print(f"Recent Cross: {recent.replace('_', ' ').title()}")
    print(f"Next Cross: {next.replace('_', ' ').title()}\n")


def print_summary(score, outlook, confidence):
    print("Summary:")
    print(f"Signal Score: {score}/100")
    print(f"Outlook: {outlook.replace('_', ' ').title()}")
    print(f"Confidence: {confidence}\n")
    print_summary_message(score, outlook, confidence)


def print_summary_message(score, outlook, confidence):
    outlook_word = {
        "strong_bullish": "strongly bullish",
        "bullish": "bullish",
        "neutral": "neutral",
        "bearish": "bearish",
        "strong_bearish": "strongly bearish",
    }

    confidence_word = {
        "High": "high",
        "Moderate": "moderate",
        "Low": "low",
    }

    outlook_line = {
        "strong_bullish": "The overall picture leans clearly to the upside.",
        "bullish": "The balance of signals is slightly positive.",
        "neutral": "The signals are split and the direction is not very clear.",
        "bearish": "The balance of signals is slightly negative.",
        "strong_bearish": "The overall picture leans clearly to the downside.",
    }

    confidence_line = {
        "High": "A good number of indicators are telling a similar story.",
        "Moderate": "There is some agreement, but a few areas are still mixed.",
        "Low": "Different indicators are pulling in different directions right now.",
    }

    next_step_line = {
        "strong_bullish": "If price stays strong, the trend is likely to remain intact, but sharp pullbacks are still possible.",
        "bullish": "If the stock can keep building strength, the outlook can improve, but it's worth watching for any loss of momentum.",
        "neutral": "A breakout or breakdown from the current range is usually what brings clarity from here.",
        "bearish": "A bounce can happen at any time, but it would take follow-through to shift the outlook back to neutral.",
        "strong_bearish": "Stabilization is the first thing to look for before expecting a bigger recovery.",
    }

    risk_line = {
        "High": "Even with higher confidence, it's smart to manage risk because markets can flip quickly.",
        "Moderate": "Keeping risk controlled makes sense until the picture becomes cleaner.",
        "Low": "It may be better to stay patient or keep sizing small until signals line up better.",
    }

    paragraph = (
        f"With a signal score of {score}/100, the overall setup looks {outlook_word[outlook]}. "
        f"{outlook_line[outlook]}\n"
        f"Confidence is {confidence_word[confidence]}, which means {confidence_line[confidence].lower()}\n"
        f"{next_step_line[outlook]}\n"
        f"{risk_line[confidence]}"
    )

    return print(paragraph)


def print_stock_analysis(
    trend,
    momentum,
    volume_confirmation,
    recent,
    next,
    score,
    outlook,
    confidence,
):
    print("Technical Analysis")
    print("-" * 100)
    print_trend_message(trend)
    print_momentum_message(momentum)
    print_volume_message(volume_confirmation)
    print_MA_cross(recent, next)
    print("-" * 100)
    print_summary(score, outlook, confidence)
    print("=" * 100)
