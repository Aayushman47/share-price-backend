import numpy as np
import pandas as pd

def add_intraday_features(df):
    df = df.copy()

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]

    # ---- Returns (short horizon) ----
    df["ret_1"] = close.pct_change(1)
    df["ret_3"] = close.pct_change(3)

    # ---- Volatility (intraday) ----
    df["vol_10"] = df["ret_1"].rolling(10).std()

    # ---- Candle structure ----
    df["range"] = high - low
    df["body"] = (close - df["Open"]).abs()
    df["body_ratio"] = df["body"] / (df["range"] + 1e-8)

    # ---- Volume spike ----
    df["vol_ma"] = volume.rolling(20).mean()
    df["vol_spike"] = volume / (df["vol_ma"] + 1e-8)

    # ---- Time-of-day encoding (important!) ----
    minutes = df.index.hour * 60 + df.index.minute
    df["time_sin"] = np.sin(2 * np.pi * minutes / 390)
    df["time_cos"] = np.cos(2 * np.pi * minutes / 390)

    return df.dropna()
