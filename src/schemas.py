from pydantic import BaseModel, RootModel
from typing import Optional, List


class Snapshot(BaseModel):
    current_price: float
    day_change_pct: float
    status: str
    momentum: str


class Signal(BaseModel):
    symbol: str
    time_ist: str
    timeframe: str
    predicted_move_pct: float
    direction: str
    confidence: float
    regime: str
    trade_intensity: str
    time_utc: Optional[str] = None




class WatchlistItem(BaseModel):
    symbol: str
    snapshot: Optional[Snapshot] = None
    daily: Optional[Signal] = None
    intraday: Optional[Signal] =None
    error: Optional[str] = None


class WatchlistResponse(RootModel[List[WatchlistItem]]):
    pass
