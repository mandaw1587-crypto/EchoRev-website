"""70/30 walk-forward split and paired in-sample/out-of-sample backtest run."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from config import StrategyConfig
from backtest.engine import simulate, BacktestResult
from backtest.metrics import compute_metrics, Stats


@dataclass
class WalkForwardResult:
    in_sample: BacktestResult
    out_sample: BacktestResult
    in_sample_stats: Stats
    out_sample_stats: Stats
    split_time: pd.Timestamp


def split_in_out_sample(df: pd.DataFrame, in_sample_frac: float = 0.70) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    df must already have indicators/structure/scores computed on the FULL
    series (see run_backtest.py's pipeline) -- those are causal per-bar
    computations, so pre-computing on the full series and splitting after is
    equivalent to computing on each half separately, EXCEPT it avoids losing
    ~200 bars of EMA200/pivot warmup right at the start of the out-of-sample
    slice. Splitting only decides which bars are eligible for entries; a bar
    still only ever uses its own historical past.
    """
    cutoff = int(len(df) * in_sample_frac)
    return df.iloc[:cutoff].copy(), df.iloc[cutoff:].copy()


def run_walk_forward(df_featured: pd.DataFrame, cfg: StrategyConfig, cost_type: str, tick_size: float,
                      timeframe: str, is_stock: bool, initial_equity: float = 100_000.0,
                      fractional: bool | None = None) -> WalkForwardResult:
    if fractional is None:
        fractional = not is_stock  # whole shares for stocks by default, fractional for crypto
    df_is, df_oos = split_in_out_sample(df_featured, cfg.walk_forward.in_sample_frac)

    is_result = simulate(df_is, cfg, cost_type, tick_size, initial_equity, fractional)
    oos_result = simulate(df_oos, cfg, cost_type, tick_size, initial_equity, fractional)

    is_stats = compute_metrics(is_result, timeframe, is_stock, initial_equity)
    oos_stats = compute_metrics(oos_result, timeframe, is_stock, initial_equity)
    split_time = df_oos.index[0] if len(df_oos) else df_is.index[-1]

    return WalkForwardResult(is_result, oos_result, is_stats, oos_stats, split_time)
