import pandas as pd
import numpy as np

def detect_intraday_regime(df):
    df = df.copy()

    # ---- VWAP ----
    typical_price = (df["High"] + df["Low"] + df["Close"]) / 3
    vwap = (typical_price * df["Volume"]).cumsum() / df["Volume"].cumsum()
    df["vwap"] = vwap

    # VWAP slope (short horizon)
    df["vwap_slope"] = df["vwap"].diff(5)

    # ---- Volatility (short) ----
    df["vol_10"] = df["ret_1"].rolling(10).std()

    # ---- Candle conviction ----
    df["conviction"] = df["body_ratio"]

    # ---- Thresholds (adaptive) ----
    vol_high = df["vol_10"].quantile(0.75)
    slope_th = df["vwap_slope"].abs().quantile(0.60)
    conviction_th = df["conviction"].quantile(0.55)

    def classify(row):
        if row["vol_10"] > vol_high:
            return "High Volatility"
        elif abs(row["vwap_slope"]) > slope_th and row["conviction"] > conviction_th:
            return "Trending"
        else:
            return "Choppy"

    df["intraday_regime"] = df.apply(classify, axis=1)

    return df
