from src.data_loader import fetch_intraday_clean
from src.intraday_features import add_intraday_features
from src.intraday_regime import detect_intraday_regime
from src.model_intraday import (
    prepare_intraday_dataset,
    train_intraday_model,
    predict_intraday
)
from src.output import unified_output

SYMBOL = "RELIANCE.NS"

# 1️⃣ Load intraday data
idf = fetch_intraday_clean(SYMBOL, interval="5m", period="5d")
idf = add_intraday_features(idf)
idf = detect_intraday_regime(idf)

# 2️⃣ Prepare dataset
X, y, idf_model = prepare_intraday_dataset(idf)

# 3️⃣ Train model
model = train_intraday_model(X, y)

# 4️⃣ Predict latest candle
X_latest = X.tail(1)
pred, direction, conf = predict_intraday(model, X_latest)

# 5️⃣ DEFINE latest row (THIS WAS MISSING)
latest = idf_model.iloc[-1]

# 6️⃣ Unified output
signal = unified_output(
    symbol=SYMBOL,
    time=latest.name,
    timeframe="INTRADAY",
    predicted_move=pred,
    direction=direction,
    confidence=conf,
    regime=latest["intraday_regime"],
)

print("\n--- FINAL INTRADAY SIGNAL ---")
for k, v in signal.items():
    print(f"{k:20}: {v}")
