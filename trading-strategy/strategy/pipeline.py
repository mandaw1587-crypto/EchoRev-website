"""Compose indicators -> market structure -> HTF bias -> confluence scores."""
from __future__ import annotations

import pandas as pd

from config import StrategyConfig
from strategy.indicators import compute_all_indicators
from strategy.structure import compute_structure
from strategy.scoring import compute_htf_bias, compute_confluence_scores


def build_features(df: pd.DataFrame, cfg: StrategyConfig) -> pd.DataFrame:
    out = compute_all_indicators(df, cfg.indicators)
    out = compute_structure(out, cfg.structure)
    out["htf_bias"] = compute_htf_bias(out, cfg.indicators.ema_slow)
    out = compute_confluence_scores(out, cfg)
    return out
