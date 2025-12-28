import pandas as pd
import numpy as np

def detect_regime(df):
    df = df.copy()

    # ---- FIX: Flatten yfinance MultiIndex ----
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # --- Trend ---
    df["ma_20"] = df["Close"].rolling(20).mean()
    df["ma_50"] = df["Close"].rolling(50).mean()
    df["ma_slope"] = df["ma_20"].diff(5)

    # --- Volatility ---
    df["vol_30"] = df["ret_1d"].rolling(30).std()

    # --- Thresholds (force scalars) ---
    vol_high_thresh = float(df["vol_30"].quantile(0.75))
    slope_thresh = float(df["ma_slope"].abs().quantile(0.60))

    def classify(row):
        if row["vol_30"] > vol_high_thresh:
            return "High Volatility"
        elif abs(row["ma_slope"]) > slope_thresh:
            return "Trending"
        else:
            return "Sideways"

    df["regime"] = df.apply(classify, axis=1)

    return df
