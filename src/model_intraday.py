import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Intraday features (keep it lean)
INTRADAY_FEATURES = [
    "ret_1",
    "ret_3",
    "vol_10",
    "body_ratio",
    "vol_spike",
    "time_sin",
    "time_cos",
]

def prepare_intraday_dataset(df):
    """
    Target: next-candle return
    """
    df = df.copy()
    HORIZON=36
    df["target_next"] = df["Close"].pct_change().shift(-HORIZON)

    df = df.dropna(subset=INTRADAY_FEATURES + ["target_next"])
    X = df[INTRADAY_FEATURES]
    y = df["target_next"]

    return X, y, df


def train_intraday_model(X, y):
    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=6,
        min_samples_leaf=20,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X, y)
    return model


def predict_intraday(model, X_latest):
    """
    Returns: predicted_return, direction, raw_confidence
    """
    pred = float(model.predict(X_latest)[0])
    direction = "UP" if pred > 0 else "DOWN"

    # Raw confidence proxy (same philosophy as daily)
    raw_confidence = min(abs(pred) / 0.0015, 1.0)

    return pred, direction, raw_confidence
