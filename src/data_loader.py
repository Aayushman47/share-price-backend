import yfinance as yf
import pandas as pd

def fetch_daily(symbol, period="3mo"):
    df = yf.download(symbol, interval="1d", period=period)
    df.dropna(inplace=True)
    return df

def fetch_intraday(symbol, interval="5m", period="5d"):
    df = yf.download(symbol, interval=interval, period=period)
    df.dropna(inplace=True)
    return df

def fetch_intraday_clean(symbol, interval="5m", period="5d"):
    df = fetch_intraday(symbol, interval=interval, period=period)

    # Flatten MultiIndex if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.dropna()
    return df

def get_intraday_candles_15m(symbol: str):
    df = fetch_intraday_clean(
        symbol=symbol,
        interval="15m",
        period="2d"
    )

    if df is None or df.empty:
        return []

    candles = []
    for idx, row in df.iterrows():
        candles.append({
            "time": int(pd.Timestamp(idx).timestamp()),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
        })

    return candles