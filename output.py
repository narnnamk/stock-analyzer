import textwrap
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def print_welcome_message():
    width = 100
    print()
    print("=" * width)
    print("Welcome to Stock Analyzer!")
    print("-" * width)
    print("Enter a stock ticker and a time period to generate a stock analysis report.")
    print(
        "The report evaluates trend, momentum, volume confirmation, volatility, and MA crosses,"
    )
    print(
        "includes technical charts, and ends with a signal score, outlook, and confidence level."
    )
    print("Note: 1mo = 21 trading days, 3mo = 63, 6mo = 126, and 1y = 252.")
    print("=" * width)


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
    sign = "-" if num < 0 else ""
    num = abs(num)
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
            return f"{sign}{remove_decimals(num)}{suffix}"

    return f"{sign}{num}"


def add_zero_to_price_decimals(price):
    if len(str(price).split(".")[1]) == 1:
        return str(price) + "0"
    return price


def get_trend_message(trend):
    messages = {
        "strong_bullish": (
            "Price is above both the 50-day MA and 200-day MA. "
            "That usually signals strong upward structure and healthy momentum. "
            "As long as price holds above the 50-day MA, the trend remains in control."
        ),
        "weak_bullish": (
            "Price is below the 50-day MA, but still above the 200-day MA. "
            "This often happens during a pullback inside a bigger uptrend. "
            "A move back above the 50-day MA would strengthen the bullish case."
        ),
        "transitional": (
            "Price is above the 50-day MA, but still below the 200-day MA. "
            "That can signal an early recovery attempt, but the long-term trend is not confirmed. "
            "Breaking and holding above the 200-day MA would be a stronger trend shift."
        ),
        "bear_rally": (
            "Price is above the 200-day MA, but the 200-day MA is also sitting above the 50-day MA. "
            "That means price has bounced, but the medium-term trend is still lagging behind. "
            "If the 50-day MA starts rising back above the 200-day MA, the trend improves."
        ),
        "late_bearish": (
            "Both moving averages are above price, with the 200-day MA above the 50-day MA. "
            "That usually points to a longer-term downtrend that is still in control. "
            "A sustained move back above the 50-day MA would be the first sign of improvement."
        ),
        "strong_bearish": (
            "The 50-day MA is above the 200-day MA, and both are above price. "
            "That often signals strong downside pressure and aggressive selling phases. "
            "Price would need to reclaim the 200-day MA to reduce the bearish outlook."
        ),
        "neutral": (
            "Price and the 50/200-day MAs are not in a clean bullish or bearish structure. "
            "This can happen during sideways markets or choppy transitions. "
            "Waiting for a clearer alignment can help avoid false signals. "
        ),
    }

    return messages[trend]


def get_momentum_message(momentum):
    messages = {
        "strong_buy": (
            "The percent gain for this period is high, and price is trading near the top of its range. "
            "That usually means buyers are in control and the move has strength. "
            "Be careful with sudden pullbacks after strong runs."
        ),
        "moderate_buy": (
            "The percent gain is solid for the period, and price is in the upper part of the range. "
            "This suggests steady buying pressure and healthy trend continuation. "
            "Holding in the upper range keeps the momentum strong."
        ),
        "bounce_attempt": (
            "The period return is positive, but price is still close to the lower part of the range. "
            "That can happen when a stock is trying to recover after weakness. "
            "A push toward the middle or upper range would confirm stronger momentum."
        ),
        "consolidation": (
            "Price is sitting around the middle of the range without a strong percent move. "
            "This often means the market is undecided right now. "
            "A break out of the range is usually the next important signal."
        ),
        "weak_sell": (
            "The period return is negative and price is sitting in the lower part of its range. "
            "Sellers have an advantage, but it does not look like a full breakdown yet. "
            "A recovery back toward the mid-range would improve the signal."
        ),
        "strong_sell": (
            "The percent drop for this period is large, and price is near the bottom of its range. "
            "This often signals strong selling pressure and weak demand. "
            "It usually takes a strong reversal to shift this momentum."
        ),
        "mixed_signal": (
            "The percent change and the range position do not line up into a strong setup. "
            "This can happen in choppy markets where price swings both ways. "
            "Waiting for a cleaner signal may reduce false entries."
        ),
        "no_movement": (
            "The high and low are the same, so the range is flat. "
            "This can happen with very low volume or limited data. "
            "Momentum cannot be judged reliably in this situation."
        ),
    }

    return messages[momentum]


def get_volume_message(volume_confirmation: str):
    messages = {
        "bullish_confirm": (
            "Volume confirms the bullish move. "
            "Price has been trending up and OBV is also rising. "
            "That usually means buying pressure is supporting the uptrend."
        ),
        "bearish_confirm": (
            "Volume confirms the bearish move. "
            "Price has been trending down and OBV is also falling. "
            "That usually means selling pressure is supporting the downtrend."
        ),
        "bearish_divergence": (
            "Price is moving up, but OBV is moving down. "
            "That can mean the rally is not supported by real buying pressure. "
            "Be cautious, because this setup can lead to pullbacks or reversals."
        ),
        "bullish_divergence": (
            "Price is moving down, but OBV is moving up. "
            "That can mean buyers are quietly stepping in while price is still weak. "
            "If price stabilizes, this can be an early reversal clue."
        ),
        "accumulation": (
            "Price is mostly flat, but OBV is trending up. "
            "That can mean investors are buying in the background without moving price much. "
            "A breakout is more likely if this accumulation continues."
        ),
        "distribution": (
            "Price is mostly flat, but OBV is trending down. "
            "That can mean selling is happening quietly while price still looks stable. "
            "A breakdown is more likely if this distribution continues."
        ),
        "weak_bullish": (
            "Price is trending up, but OBV is mostly flat. "
            "That can mean the move is drifting higher without strong demand. "
            "This trend can continue, but it is easier to fade if buyers do not step in."
        ),
        "weak_bearish": (
            "Price is trending down, but OBV is mostly flat. "
            "That can mean the drop is happening without strong selling pressure. "
            "This can turn into a bounce if buyers show up."
        ),
        "consolidation": (
            "Neither price nor OBV is showing a strong direction. "
            "This often happens during consolidation and indecision. "
            "Waiting for a clear volume shift can help confirm the next move."
        ),
    }

    return messages[volume_confirmation]


def get_summary_message(score, outlook, confidence):
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
        f"{outlook_line[outlook]} "
        f"Confidence is {confidence_word[confidence]}, which means {confidence_line[confidence].lower()} "
        f"{next_step_line[outlook]} "
        f"{risk_line[confidence]}"
    )

    return paragraph


def wrap_text(text):
    return textwrap.wrap(text, width=84, break_long_words=False, break_on_hyphens=False)


def print_header(c, x, y, divider, line_space, name, ticker, period):
    c.drawString(x, y, divider)
    y -= line_space
    first_row = f"{name.upper()} STOCK ANALYSIS REPORT"
    c.drawString(x, y, f"{first_row:^84}")
    y -= line_space
    ticker_row = f"Ticker: {ticker} | Period: {period}"
    c.drawString(x, y, f"{ticker_row:^84}")
    y -= line_space
    c.drawString(x, y, divider)
    y -= line_space

    return x, y


def print_overview(
    c,
    x,
    y,
    line_space,
    thin,
    usd_change,
    pct_change,
    price,
    high,
    low,
    volatility,
    volatility_level,
    curr_volume,
    avg_volume,
    mkt_cap,
    divider,
):
    c.drawString(x, y, f"{'QUICK OVERVIEW':^84}")
    y -= line_space
    c.drawString(x, y, thin)
    y -= line_space

    c.drawString(
        x,
        y,
        f"{'Current Price':<21}{'Period High':<21}{'Period Low':<21}{'Price Change':<21}",
    )
    y -= line_space

    change_str = f"{usd_change:+,.2f} ({pct_change:+.2f}%)"
    price_row = f"${price:<20,.2f}${high:<20,.2f}${low:<20,.2f}{change_str:21}"
    c.drawString(x, y, price_row)
    y -= line_space
    y -= line_space
    c.drawString(
        x,
        y,
        f"{'Volume':<21}{'Average Volume':<21}{'Market Cap':<21}{'Volatility':<21}",
    )
    y -= line_space

    volatility_str = f"{volatility}% ({volatility_level.replace('_', ' ').title()})"
    volume_row = f"{shorten_number(curr_volume):<21}{shorten_number(avg_volume):<21}{shorten_number(mkt_cap):<21}{volatility_str:<21}"
    c.drawString(x, y, volume_row)
    y -= line_space
    c.drawString(x, y, divider)
    y -= line_space

    return x, y


def print_technical(
    c,
    x,
    y,
    line_space,
    thin,
    fifty_MA,
    twoH_MA,
    recent,
    next,
    trend,
    momentum,
    volume_confirmation,
    divider,
):
    c.drawString(x, y, f"{'TECHNICAL ANALYSIS':^84}")
    y -= line_space
    c.drawString(x, y, thin)
    y -= line_space
    c.drawString(x, y, f"{'50-Day MA':<21}{'200-Day MA':<21}{'Recent':<21}{'Next':<21}")
    y -= line_space
    MA_row = f"${fifty_MA:<20}${twoH_MA:<20}{recent.replace('_', ' ').title():<21}{next.replace('_', ' ').title():<21}"
    c.drawString(x, y, MA_row)
    y -= line_space
    y -= line_space

    trend_message = get_trend_message(trend)
    trend_lines = wrap_text(trend_message)
    c.drawString(x, y, f"Trend - {trend.replace('_', ' ').upper()}")
    y -= line_space
    for i in range(len(trend_lines)):
        c.drawString(x, y, trend_lines[i])
        y -= line_space
    y -= line_space

    momentum_message = get_momentum_message(momentum)
    momentum_lines = wrap_text(momentum_message)
    c.drawString(x, y, f"Momentum - {momentum.replace('_', ' ').upper()}")
    y -= line_space
    for i in range(len(momentum_lines)):
        c.drawString(x, y, momentum_lines[i])
        y -= line_space
    y -= line_space

    volume_message = get_volume_message(volume_confirmation)
    volume_lines = wrap_text(volume_message)
    c.drawString(x, y, f"Volume - {volume_confirmation.replace('_', ' ').upper()}")
    y -= line_space
    for i in range(len(volume_lines)):
        c.drawString(x, y, volume_lines[i])
        y -= line_space
    c.drawString(x, y, divider)

    return x, y


def draw_charts(line_space, c, x, y, thin, ticker, w):
    y -= line_space
    c.drawString(x, y, f"{'VISUAL CHARTS':^84}")
    y -= line_space
    c.drawString(x, y, thin)
    y -= line_space
    y -= 300
    c.drawImage(f"{ticker}_charts.png", ((w - 500) // 2), y, width=500, height=300)
    c.showPage()

    return x, y


def print_summary(c, x, y, divider, line_space, thin, score, outlook, confidence):
    c.drawString(x, y, divider)
    y -= line_space
    c.drawString(x, y, f"{'SUMMARY':^84}")
    y -= line_space
    c.drawString(x, y, thin)
    y -= line_space
    c.drawString(x, y, f"{'Signal Score':<13}: {score}/100")
    y -= line_space
    c.drawString(x, y, f"{'Outlook':<13}: {outlook.replace('_', ' ').title()}")
    y -= line_space
    c.drawString(x, y, f"{'Confidence':<13}: {confidence}")
    y -= line_space
    y -= line_space

    summary_message = get_summary_message(score, outlook, confidence)
    summary_lines = wrap_text(summary_message)
    for line in summary_lines:
        c.drawString(x, y, line)
        y -= line_space
    c.drawString(x, y, divider)

    y -= line_space
    disclaimer = "Note: This report is for educational purposes only and is not financial advice."
    c.drawString(x, y, disclaimer)
    y -= line_space
    c.drawString(x, y, divider)
    y -= line_space

    return x, y


def get_report(
    ticker,
    name,
    period,
    usd_change,
    pct_change,
    price,
    high,
    low,
    volatility,
    volatility_level,
    curr_volume,
    avg_volume,
    mkt_cap,
    fifty_MA,
    twoH_MA,
    recent,
    next,
    trend,
    momentum,
    volume_confirmation,
    score,
    outlook,
    confidence,
):
    c = canvas.Canvas(f"{ticker}_Report.pdf", pagesize=A4)
    w, h = A4

    side_margin = 72
    top_margin = 72
    x = side_margin
    y = h - top_margin

    fontsize = 9
    line_space = fontsize * 1.3

    c.setFont("Courier", fontsize)

    width_chars = 84
    divider = "=" * width_chars
    thin = "-" * width_chars

    # Header
    x, y = print_header(c, x, y, divider, line_space, name, ticker, period)

    # Quick Overview
    x, y = print_overview(
        c,
        x,
        y,
        line_space,
        thin,
        usd_change,
        pct_change,
        price,
        high,
        low,
        volatility,
        volatility_level,
        curr_volume,
        avg_volume,
        mkt_cap,
        divider,
    )

    # Technical Analysis
    x, y = print_technical(
        c,
        x,
        y,
        line_space,
        thin,
        fifty_MA,
        twoH_MA,
        recent,
        next,
        trend,
        momentum,
        volume_confirmation,
        divider,
    )

    # charts
    x, y = draw_charts(line_space, c, x, y, thin, ticker, w)

    # page 2
    w, h = A4

    side_margin = 72
    top_margin = 72
    x = side_margin
    y = h - top_margin

    fontsize = 9
    line_space = fontsize * 1.3

    c.setFont("Courier", fontsize)

    width_chars = 84
    divider = "=" * width_chars
    thin = "-" * width_chars

    # summary
    x, y = print_summary(c, x, y, divider, line_space, thin, score, outlook, confidence)

    c.save()
