from src.data_loader import fetch_intraday_clean

def get_market_snapshot(symbol: str):
    """
    Returns current price, day change %, gainer/loser,
    and recent momentum proxy.
    """
    df = fetch_intraday_clean(symbol, interval="5m", period="1d")

    if len(df) < 2:
        return None

    open_price = df["Open"].iloc[0]
    current_price = df["Close"].iloc[-1]

    day_change_pct = (current_price - open_price) / open_price * 100

    status = "Gainer" if day_change_pct > 0 else "Loser"

    # Simple momentum proxy (last 1 hour)
    recent_return = (df["Close"].iloc[-1] - df["Close"].iloc[-12]) / df["Close"].iloc[-12] * 100

    if recent_return > 0.3:
        momentum = "Bullish"
    elif recent_return < -0.3:
        momentum = "Bearish"
    else:
        momentum = "Neutral"

    return {
    "current_price": float(current_price),
    "day_change_pct": float(day_change_pct),
    "status": status,
    "momentum": momentum
    }
