def trade_intensity(regime, confidence):
    if regime == "Trending" and confidence >= 0.60:
        return "FULL"
    elif regime in ["Trending", "High Volatility"] and confidence >= 0.45:
        return "LIGHT"
    else:
        return "OBSERVE"


import pytz

IST = pytz.timezone("Asia/Kolkata")

def trade_intensity(regime, confidence):
    if regime == "Trending" and confidence >= 0.60:
        return "FULL"
    elif regime in ["Trending", "High Volatility"] and confidence >= 0.45:
        return "LIGHT"
    else:
        return "OBSERVE"


def unified_output(
    symbol,
    time,
    timeframe,
    predicted_move,
    direction,
    confidence,
    regime
):
    # Handle timestamps safely
    time_utc = None
    time_ist = None

    if hasattr(time, "tzinfo") and time.tzinfo is not None:
        time_utc = str(time)
        time_ist = time.tz_convert(IST).strftime("%Y-%m-%d %H:%M:%S")
    else:
        # DAILY case ("NEXT_DAY")
        time_utc = str(time)
        time_ist = str(time)

    return {
        "symbol": symbol,
        "time_ist": time_ist,
        "timeframe": timeframe,
        "predicted_move_pct": round(predicted_move * 100, 3),
        "direction": direction,
        "confidence": round(confidence, 2),
        "regime": regime,
        "trade_intensity": trade_intensity(regime, confidence),
    }
