import pandas as pd
import numpy as np
from ta.volatility import AverageTrueRange
from ta.momentum import RSIIndicator

def add_daily_features(df):
    df = df.copy()

    df["ret_1d"] = df["Close"].pct_change(1)
    df["ret_3d"] = df["Close"].pct_change(3)
    df["ret_5d"] = df["Close"].pct_change(5)

    df["volatility"] = df["ret_1d"].rolling(10).std()

    close = df["Close"].squeeze()
    df["rsi"] = RSIIndicator(close, window=14).rsi()


    df["range_pos"] = (df["Close"] - df["Low"]) / (df["High"] - df["Low"])

    return df.dropna()