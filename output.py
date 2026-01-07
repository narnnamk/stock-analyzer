def print_welcome_message():
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
    print("=" * 67)
    print("STOCK ANALYZER")
    print(f"Ticker: {ticker} | Period: {period}")
    print("=" * 67)
    print("Quick Overview")
    print("-" * 67)
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
    print("=" * 67)


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

    return print(f"Trend:\n{messages[trend]}")


def print_stock_analysis(ticker, trend):
    print(f"{ticker} Technical Analysis")
    print("-" * 67)
    print_trend_message(trend)
    print("=" * 67)
