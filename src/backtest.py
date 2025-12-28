import pandas as pd
from tqdm import tqdm

def walk_forward_backtest(
    df,
    prepare_fn,
    train_fn,
    predict_fn,
    features,
    min_train_size=40
):
    """
    Walk-forward backtest for next-day prediction
    """

    results = []

    for i in tqdm(range(min_train_size, len(df) - 1)):
        train_df = df.iloc[:i]
        test_df = df.iloc[i:i+1]

        # Prepare data
        X_train, y_train, _ = prepare_fn(train_df)

        # Train model
        model = train_fn(X_train, y_train)

        # Predict
        X_test = test_df[features]
        pred, direction, confidence = predict_fn(model, X_test)

        actual_return = float(test_df["target"].iloc[0])
        regime = test_df["regime"].iloc[0]

        results.append({
            "date": test_df.index[0],
            "predicted_return": pred,
            "actual_return": actual_return,
            "direction": direction,
            "confidence": confidence,
            "regime": regime
        })

    return pd.DataFrame(results)
