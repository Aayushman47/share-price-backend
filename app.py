from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from src.signal_engine import get_signal, get_watchlist
from src.schemas import WatchlistResponse
from src.scheduler import start_scheduler
from src.watchlist_store import (
    get_watchlist as get_symbols_store,
    add_symbol,
    remove_symbol,
    replace_watchlist,
)

# -------------------------------------------------
# App setup
# -------------------------------------------------
app = FastAPI(
    title="Share Price Prediction API",
    description="Daily & Intraday share price prediction system",
    version="1.0",
)

# Start background scheduler ONCE
start_scheduler()

# CORS (frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"
                   "https://share-price-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Core prediction endpoints
# -------------------------------------------------

@app.get("/signal")
def signal(symbol: str, timeframe: str = "DAILY"):
    try:
        if timeframe == "DAILY":
            df = fetch_daily(symbol)
        else:
            df = fetch_intraday_clean(symbol)

        # existing ML / signal logic
        return result

    except ValueError as e:
        # Yahoo blocked / no data
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


@app.post(
    "/watchlist",
    response_model=WatchlistResponse,
    operation_id="get_watchlist",
)
def watchlist(symbols: List[str]):
    """
    Get predictions for a list of symbols (max 30 enforced internally)
    """
    return get_watchlist([s.upper() for s in symbols])


# -------------------------------------------------
# Dynamic watchlist management (used by scheduler)
# -------------------------------------------------

@app.get("/watchlist/symbols")
def get_watchlist_symbols():
    """
    Return current dynamic watchlist used by scheduler
    """
    return get_symbols_store()


@app.post("/watchlist/add")
def add_to_watchlist(symbol: str):
    """
    Add one symbol to dynamic watchlist
    """
    add_symbol(symbol)
    return {"status": "added", "symbol": symbol.upper()}


@app.post("/watchlist/remove")
def remove_from_watchlist(symbol: str):
    """
    Remove one symbol from dynamic watchlist
    """
    remove_symbol(symbol)
    return {"status": "removed", "symbol": symbol.upper()}


@app.post("/watchlist/replace")
def replace_watchlist_symbols(symbols: List[str]):
    """
    Replace entire dynamic watchlist (used by frontend)
    """
    replace_watchlist(symbols)
    return {"status": "replaced", "count": len(symbols)}
