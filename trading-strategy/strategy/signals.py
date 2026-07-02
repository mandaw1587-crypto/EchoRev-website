"""Entry-signal gate: score >= min_score AND R/R >= min_rr AND volume > 1.3x avg."""
from __future__ import annotations

from config import StrategyConfig
from strategy.risk import risk_reward


def evaluate_signal(row, cfg: StrategyConfig) -> str | None:
    """
    Returns "long", "short", or None. Evaluated on a CONFIRMED bar (the row
    passed in must already be fully closed data -- callers must never pass a
    forming/incomplete bar). If both directions qualify (rare, contradictory
    indicators), the higher-scoring direction wins.
    """
    vol_ok = (row["vol_sma20"] == row["vol_sma20"]) and row["vol_sma20"] > 0 and (
        row["volume"] > cfg.entry.min_volume_mult * row["vol_sma20"]
    )
    if not vol_ok:
        return None

    rr = risk_reward("long", row["close"], row["close"] - 1.0, cfg.risk)  # rr is direction/price-independent (see risk.py)
    rr_ok = rr >= cfg.entry.min_rr

    long_ok = row["score_long"] >= cfg.entry.min_score and rr_ok
    short_ok = row["score_short"] >= cfg.entry.min_score and rr_ok

    if long_ok and short_ok:
        return "long" if row["score_long"] >= row["score_short"] else "short"
    if long_ok:
        return "long"
    if short_ok:
        return "short"
    return None
