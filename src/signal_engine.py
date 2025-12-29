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


def _safe_response(symbol, timeframe, message):
    return {
        "status": "NO_SIGNAL",
        "symbol": symbol,
        "timeframe": timeframe,
        "message": message
    }


def get_signal(symbol: str, timeframe: str):
    cache_key = (symbol, timeframe)

    # 1️⃣ CACHE
    cached = get_cache(cache_key)
    if cached:
        return cached["data"]

    try:
        # ================= DAILY =================
        if timeframe == "DAILY":
            df = fetch_daily(symbol, period="6mo")

            if df is None or df.empty:
                return _safe_response(symbol, timeframe, "No daily price data")

            df = add_daily_features(df)
            df = detect_regime(df)

            X, y, df_model = prepare_daily_dataset(df)

            if X is None or y is None or len(X) < 30 or y.nunique() < 2:
                return _safe_response(
                    symbol,
                    timeframe,
                    "Not enough clean data to train daily model"
                )

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
                regime=latest.get("regime", "UNKNOWN"),
            )

            set_cache(cache_key, result)
            return result

        # ================= INTRADAY =================
        if timeframe == "INTRADAY":
            df = fetch_intraday_clean(symbol, interval="5m", period="5d")

            if df is None or df.empty:
                return _safe_response(symbol, timeframe, "No intraday data")

            df = add_intraday_features(df)
            df = detect_intraday_regime(df)

            X, y, df_model = prepare_intraday_dataset(df)

            if X is None or y is None or len(X) < 30 or y.nunique() < 2:
                return _safe_response(
                    symbol,
                    timeframe,
                    "Not enough clean data to train intraday model"
                )

            model = train_intraday_model(X, y)

            pred, direction, confidence = predict_intraday(model, X.tail(1))
            latest = df_model.iloc[-1]

            result = unified_output(
                symbol=symbol,
                time=str(latest.name),
                timeframe="INTRADAY",
                predicted_move=pred,
                direction=direction,
                confidence=confidence,
                regime=latest.get("intraday_regime", "UNKNOWN"),
            )

            set_cache(cache_key, result)
            return result

        return _safe_response(symbol, timeframe, "Invalid timeframe")

    except Exception as e:
        return _safe_response(symbol, timeframe, str(e))


def get_watchlist(symbols: list[str]):
    results = []

    for symbol in symbols[:30]:
        try:
            results.append({
                "symbol": symbol,
                "snapshot": get_market_snapshot(symbol),
                "daily": get_signal(symbol, "DAILY"),
                "intraday": get_signal(symbol, "INTRADAY"),
            })
        except Exception as e:
            results.append({
                "symbol": symbol,
                "error": str(e)
            })

    return results
