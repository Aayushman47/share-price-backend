from sklearn.ensemble import RandomForestRegressor

FEATURES = [
    "ret_1d",
    "ret_3d",
    "ret_5d",
    "volatility",
    "rsi",
    "range_pos"
]

def prepare_daily_dataset(df):
    df = df.copy()
    df["target"] = df["Close"].pct_change().shift(-1)
    df = df.dropna(subset=FEATURES + ["target"])
    X = df[FEATURES]
    y = df["target"]
    return X, y, df

def train_daily_model(X, y):
    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=5,
        min_samples_leaf=10,
        random_state=42
    )
    model.fit(X, y)
    return model

def predict_next_day(model, X_latest):
    pred = float(model.predict(X_latest)[0])
    direction = "UP" if pred > 0 else "DOWN"
    confidence = min(abs(pred) / 0.01, 1.0)
    return pred, direction, confidence
