import time
import threading

from src.cache import clean_expired
from src.signal_engine import get_signal
from src.watchlist_store import get_watchlist


# You can change this later or load from DB / file

# ---------------------------
# Prediction refresher
# ---------------------------
def refresh_predictions():
    while True:
        try:
            symbols = get_watchlist()
            print(f"[SCHEDULER] Refreshing {len(symbols)} symbols")

            for symbol in symbols:
                get_signal(symbol, "DAILY")
                get_signal(symbol, "INTRADAY")

            print("[SCHEDULER] Refresh done")
        except Exception as e:
            print("[SCHEDULER] Refresh error:", e)

        time.sleep(15 * 60)



# ---------------------------
# Cache cleaner
# ---------------------------
def cache_cleaner():
    while True:
        try:
            # Clean anything older than 30 minutes
            clean_expired(ttl_seconds=30 * 60)
            print("[SCHEDULER] Cache cleaned")
        except Exception as e:
            print("[SCHEDULER] Cache clean error:", e)

        # Run every 5 minutes
        time.sleep(5 * 60)


# ---------------------------
# Entry point
# ---------------------------
def start_scheduler():
    threading.Thread(
        target=refresh_predictions,
        daemon=True
    ).start()

    threading.Thread(
        target=cache_cleaner,
        daemon=True
    ).start()

    print("[SCHEDULER] Background tasks started")
