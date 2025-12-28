import json
import os

WATCHLIST_FILE = "watchlist.json"

# -------------------------
# Internal state
# -------------------------
_watchlist = set()


# -------------------------
# Persistence helpers
# -------------------------
def _load_from_disk():
    global _watchlist
    if os.path.exists(WATCHLIST_FILE):
        try:
            with open(WATCHLIST_FILE, "r") as f:
                symbols = json.load(f)
                _watchlist = set(s.upper() for s in symbols)
        except Exception:
            _watchlist = set()
    else:
        _watchlist = set()


def _save_to_disk():
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(sorted(_watchlist), f)


# -------------------------
# Public API
# -------------------------
def get_watchlist():
    return sorted(_watchlist)


def add_symbol(symbol: str):
    _watchlist.add(symbol.upper())
    _save_to_disk()


def remove_symbol(symbol: str):
    _watchlist.discard(symbol.upper())
    _save_to_disk()


def replace_watchlist(symbols: list[str]):
    global _watchlist
    _watchlist = set(s.upper() for s in symbols)
    _save_to_disk()


# -------------------------
# Load on import
# -------------------------
_load_from_disk()
