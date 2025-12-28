from src.data_loader import fetch_daily, fetch_intraday_clean
from src.features import add_daily_features
from src.regime import detect_regime
from src.intraday_features import add_intraday_features
from src.intraday_regime import detect_intraday_regime
from src.market_snapshot import get_market_snapshot
from src.cache import get_cache, set_cache
from src.model_daily import (
    prepare_daily_dataset,
    train_daily_model,
    predict_next_day
)
from src.model_intraday import (
    prepare_intraday_dataset,
    train_intraday_model,
    predict_intraday
)
from src.output import unified_output


def get_signal(symbol: str, timeframe: str):
    cache_key = (symbol, timeframe)

    # ✅ 1. CHECK CACHE FIRST
    cached = get_cache(cache_key)
    if cached:
        return cached["data"]

    # ================= DAILY =================
    if timeframe == "DAILY":
        df = fetch_daily(symbol, period="6mo")
        df = add_daily_features(df)
        df = detect_regime(df)

        X, y, df_model = prepare_daily_dataset(df)
        model = train_daily_model(X, y)

        pred, direction, confidence = predict_next_day(model, X.tail(1))
        latest = df_model.iloc[-1]

        result = unified_output(
            symbol=symbol,
            time="NEXT_DAY",
            timeframe="DAILY",
            predicted_move=pred,
            direction=direction,
            confidence=confidence,
            regime=latest["regime"],
        )

        # ✅ 2. SAVE TO CACHE
        set_cache(cache_key, result)
        return result

    # ================= INTRADAY =================
    elif timeframe == "INTRADAY":
        df = fetch_intraday_clean(symbol, interval="5m", period="5d")
        df = add_intraday_features(df)
        df = detect_intraday_regime(df)

        X, y, df_model = prepare_intraday_dataset(df)
        model = train_intraday_model(X, y)

        pred, direction, confidence = predict_intraday(model, X.tail(1))
        latest = df_model.iloc[-1]

        result = unified_output(
            symbol=symbol,
            time=latest.name,
            timeframe="INTRADAY",
            predicted_move=pred,
            direction=direction,
            confidence=confidence,
            regime=latest["intraday_regime"],
        )

        # ✅ 2. SAVE TO CACHE
        set_cache(cache_key, result)
        return result

    else:
        raise ValueError("Invalid timeframe")
    
def get_watchlist(symbols: list[str]):
    results = []

    for symbol in symbols[:30]:  # hard cap at 30
        try:
            snapshot = get_market_snapshot(symbol)
            daily_signal = get_signal(symbol, "DAILY")
            intraday_signal = get_signal(symbol, "INTRADAY")

            results.append({
                "symbol": symbol,
                "snapshot": snapshot,
                "daily": daily_signal,
                "intraday": intraday_signal,
            })

        except Exception as e:
            results.append({
                "symbol": symbol,
                "error": str(e)
            })

    return results

