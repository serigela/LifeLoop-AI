"""Load bundled, synthetic CSV examples for a repeatable local demo."""

from datetime import datetime
from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_transactions(now=None):
    rows = pd.read_csv(DATA_DIR / "transactions.csv")
    rows["timestamp"] = pd.to_datetime(rows.pop("date"))
    return _rebase(rows, now)


def load_activities(now=None):
    rows = pd.read_csv(DATA_DIR / "calendar_events.csv")
    rows["timestamp"] = pd.to_datetime(rows.pop("date") + " " + rows.pop("time"))
    rows = rows.rename(columns={"event_type": "activity_type"})
    return _rebase(rows, now)


def _rebase(rows, now=None):
    """Keep sample spacing while moving its latest date to the demo date."""
    if rows.empty:
        raise ValueError("The bundled sample CSV is empty")
    today = pd.Timestamp(now if now is not None else datetime.now()).normalize()
    offset = today - rows["timestamp"].max().normalize()
    rows["timestamp"] += offset
    return rows.sort_values("timestamp").reset_index(drop=True)
