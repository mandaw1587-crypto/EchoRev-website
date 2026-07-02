"""
Stop-loss / target / position-sizing math. Pure functions, no state -- the
backtest engine calls these at signal time and holds the results in a Trade.
"""
from __future__ import annotations

from dataclasses import dataclass

from config import RiskConfig


@dataclass
class TradePlan:
    direction: str          # "long" | "short"
    entry: float
    stop: float
    tp1: float
    tp2: float
    tp3: float
    r_distance: float       # |entry - stop|, i.e. 1R in price terms
    size: float              # units/shares


def compute_stop(direction: str, close: float, atr: float, last_pivot_low: float,
                  last_pivot_high: float, cfg: RiskConfig) -> float | None:
    """Structure/ATR blended stop. Returns None if a required pivot is unknown yet."""
    if direction == "long":
        if last_pivot_low is None or last_pivot_low != last_pivot_low:  # NaN check
            return None
        candidate_structure = last_pivot_low - cfg.pivot_stop_buffer_atr * atr
        candidate_atr = close - cfg.atr_stop_mult * atr
        return min(candidate_structure, candidate_atr)
    else:
        if last_pivot_high is None or last_pivot_high != last_pivot_high:
            return None
        candidate_structure = last_pivot_high + cfg.pivot_stop_buffer_atr * atr
        candidate_atr = close + cfg.atr_stop_mult * atr
        return max(candidate_structure, candidate_atr)


def compute_targets(direction: str, entry: float, stop: float, cfg: RiskConfig) -> tuple[float, float, float]:
    r = abs(entry - stop)
    sign = 1 if direction == "long" else -1
    return entry + sign * cfg.tp1_r * r, entry + sign * cfg.tp2_r * r, entry + sign * cfg.tp3_r * r


def risk_reward(direction: str, entry: float, stop: float, cfg: RiskConfig) -> float:
    """
    R/R measured to TP2 (the "primary" target in a 3-target scheme, 2.5R by
    default). [ASSUMPTION / KNOWN LIMITATION, see README weaknesses]: because
    targets are fixed R-multiples of the stop distance rather than derived
    from actual structure (next resistance/support), this ratio is ALWAYS
    exactly cfg.tp2_r regardless of the specific setup -- it's a function of
    config, not of market conditions. The entry gate "R/R >= min_rr" is
    therefore non-discriminating for min_rr <= tp2_r and blocks everything
    for min_rr > tp2_r. We keep it because the brief specifies it explicitly,
    but this is flagged as a strategy weakness in results/report.md.
    """
    r = abs(entry - stop)
    if r == 0:
        return 0.0
    return cfg.tp2_r


def position_size(equity: float, entry: float, stop: float, cfg: RiskConfig,
                   fractional: bool = True) -> float:
    risk_amount = equity * cfg.risk_pct_of_equity
    per_unit_risk = abs(entry - stop)
    if per_unit_risk <= 0:
        return 0.0
    size = risk_amount / per_unit_risk
    if not fractional:
        size = float(int(size))
    return max(size, 0.0)


def build_trade_plan(direction: str, entry: float, atr: float, last_pivot_low: float,
                      last_pivot_high: float, equity: float, cfg: RiskConfig,
                      fractional: bool = True) -> TradePlan | None:
    stop = compute_stop(direction, entry, atr, last_pivot_low, last_pivot_high, cfg)
    if stop is None:
        return None
    r = abs(entry - stop)
    if r <= 0:
        return None
    tp1, tp2, tp3 = compute_targets(direction, entry, stop, cfg)
    size = position_size(equity, entry, stop, cfg, fractional=fractional)
    if size <= 0:
        return None
    return TradePlan(direction=direction, entry=entry, stop=stop, tp1=tp1, tp2=tp2, tp3=tp3,
                      r_distance=r, size=size)
