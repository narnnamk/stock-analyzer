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


def shorten_number(num):
    if num >= 1_000_000_000_000_000:
        num = f"{num / 1_000_000_000_000_000:.2f}"
        num = num.rstrip("0")
        num = num.rstrip(".")
        num = f"{num}Q"
    elif num >= 1_000_000_000_000:
        num = f"{num / 1_000_000_000_000:.2f}"
        num = num.rstrip("0")
        num = num.rstrip(".")
        num = f"{num}T"
    elif num >= 1_000_000_000:
        num = f"{num / 1_000_000_000:.2f}"
        num = num.rstrip("0")
        num = num.rstrip(".")
        num = f"{num}B"
    elif num >= 1_000_000:
        num = f"{num / 1_000_000:.2f}"
        num = num.rstrip("0")
        num = num.rstrip(".")
        num = f"{num}M"
    elif num >= 1_000:
        num = f"{num / 1_000:.2f}"
        num = num.rstrip("0")
        num = num.rstrip(".")
        num = f"{num}K"
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
    days,
    fifty_MA,
    twoH_MA,
):
    print("=" * 67)
    print(f"{ticker} Quick Stock Overview")
    print("=" * 67)
    print(f"Period: {period}")
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
    print(f"Volatility ({days}-Day): {volatility}%\n")
    print(f"50-Day MA: ${fifty_MA}")
    print(f"200-day MA: ${twoH_MA}")
    print("=" * 67)
