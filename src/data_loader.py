import yfinance as yf
import pandas as pd

def fetch_daily(symbol, period="3mo"):
    df = yf.download(
        symbol,
        interval="1d",
        period=period,
        progress=False,
        threads=False
    )

    if df is None or df.empty:
        raise ValueError(f"No daily data returned for {symbol}")

    df = df.dropna()
    return df

def fetch_intraday(symbol, interval="5m", period="5d"):
    df = yf.download(
        symbol,
        interval=interval,
        period=period,
        progress=False,
        threads=False
    )

    if df is None or df.empty:
        raise ValueError(f"No intraday data returned for {symbol}")

    df = df.dropna()
    return df

def fetch_intraday_clean(symbol, interval="5m", period="5d"):
    df = fetch_intraday(symbol, interval=interval, period=period)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.dropna()

    if df.empty:
        raise ValueError(f"No clean intraday data for {symbol}")

    return df