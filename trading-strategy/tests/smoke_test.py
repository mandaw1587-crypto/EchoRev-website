#!/usr/bin/env python3
"""
End-to-end smoke test on SYNTHETIC data.

This does NOT tell you anything about the strategy's real performance --
it exists purely to prove the pipeline (indicators -> structure -> scoring
-> signals -> backtest engine -> walk-forward -> optimizer) runs without
crashing, produces internally-consistent output, and doesn't leak future
data into past decisions. Run it after `pip install -r requirements.txt`
and before your first real `python run_backtest.py` call.

Usage: python tests/smoke_test.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd

from config import DEFAULT_CONFIG
from dataclasses import replace
from strategy.pipeline import build_features
from strategy.structure import _confirmed_pivots
from backtest.engine import simulate
from backtest.walkforward import run_walk_forward
from backtest.optimize import grid_search


def make_synthetic_ohlcv(n: int = 4000, seed: int = 7, start="2023-01-01", freq="1h") -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    t = pd.date_range(start, periods=n, freq=freq, tz="UTC")
    drift = np.linspace(0, 0.0002, n)
    noise = rng.normal(0, 0.004, n)
    cyc = 0.01 * np.sin(np.linspace(0, 60 * np.pi, n))
    log_ret = drift + noise + np.diff(np.concatenate([[0], cyc]))
    close = 100 * np.exp(np.cumsum(log_ret))

    open_ = np.concatenate([[close[0]], close[:-1]]) * (1 + rng.normal(0, 0.0008, n))
    intrabar = np.abs(rng.normal(0, 0.003, n)) + 1e-4
    high = np.maximum(open_, close) * (1 + intrabar)
    low = np.minimum(open_, close) * (1 - intrabar)
    volume = np.abs(rng.normal(1_000_000, 250_000, n)) * (1 + 0.5 * np.abs(noise) / noise.std())

    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close, "volume": volume}, index=t)


def check_pivot_lag_is_causal():
    """
    Craft a price series with a hand-placed local max and verify the
    confirmed-pivot series only reveals it 5 bars later, never earlier.
    """
    n = 30
    high = pd.Series(np.full(n, 100.0))
    peak_idx = 15
    high.iloc[peak_idx] = 150.0  # unambiguous local max within any +/-5 window
    confirmed = _confirmed_pivots(high, left=5, right=5, is_high=True)

    assert pd.isna(confirmed.iloc[peak_idx + 4]), "pivot leaked 1 bar early -- LOOKAHEAD BUG"
    assert confirmed.iloc[peak_idx + 5] == 150.0, "pivot not confirmed exactly 5 bars after formation"
    print("  [ok] pivot confirmation lag is exactly 5 bars (no lookahead)")


def main():
    print("=" * 70)
    print("SMOKE TEST -- SYNTHETIC DATA ONLY. These numbers are NOT a real")
    print("backtest result and must never be reported as strategy performance.")
    print("=" * 70)

    print("\n[1/5] Checking pivot confirmation has no lookahead...")
    check_pivot_lag_is_causal()

    print("\n[2/5] Generating synthetic OHLCV and building features...")
    df = make_synthetic_ohlcv()
    df_feat = build_features(df, DEFAULT_CONFIG)
    n_nan_score = df_feat["score_long"].isna().sum()
    assert n_nan_score == 0, "score_long has NaNs -- scoring should always clip to a number"
    assert (df_feat["score_long"].between(0, 100)).all(), "score_long out of [0,100] bounds"
    assert (df_feat["score_short"].between(0, 100)).all(), "score_short out of [0,100] bounds"
    print(f"  [ok] {len(df_feat)} bars featured, scores bounded in [0,100]")
    print(f"  bars with score_long >= 85: {(df_feat['score_long'] >= 85).sum()}")
    print(f"  bars with score_short >= 85: {(df_feat['score_short'] >= 85).sum()}")

    print("\n[3/5] Running the backtest engine directly...")
    result = simulate(df_feat, DEFAULT_CONFIG, cost_type="crypto", tick_size=0.10,
                       initial_equity=100_000.0, fractional=True)
    assert np.isfinite(result.equity_curve).all(), "equity curve has non-finite values"
    print(f"  [ok] {len(result.trades)} trades, final equity ${result.final_equity:,.2f}")
    for t in result.trades[:3]:
        print(f"    {t.direction:5s} entry={t.entry_price:.2f} r_mult={t.r_multiple:+.2f} "
              f"bars_held={t.bars_held} exit_reason={t.exit_reason}")

    print("\n[4/5] Running walk-forward split (70/30)...")
    wf = run_walk_forward(df_feat, DEFAULT_CONFIG, "crypto", 0.10, "1h", is_stock=False)
    print(f"  [ok] in-sample trades={wf.in_sample_stats.total_trades}, "
          f"out-of-sample trades={wf.out_sample_stats.total_trades}")
    print(f"  in-sample expectancy={wf.in_sample_stats.expectancy_r:+.3f}R, "
          f"out-of-sample expectancy={wf.out_sample_stats.expectancy_r:+.3f}R")

    print("\n[5/5] Running a tiny grid search (reduced grid for speed)...")
    small_grid = replace(DEFAULT_CONFIG.optimization,
                          score_thresholds=(80, 90), atr_stop_mults=(1.5, 2.5), min_rrs=(1.5, 2.5),
                          min_trades_for_consideration=1)
    small_cfg = replace(DEFAULT_CONFIG, optimization=small_grid)
    from backtest.walkforward import split_in_out_sample
    df_is, df_oos = split_in_out_sample(df_feat, small_cfg.walk_forward.in_sample_frac)
    grid_results, top = grid_search(df_is, df_oos, small_cfg, "crypto", 0.10, "1h", is_stock=False,
                                     top_n_confirm=3)
    print(f"  [ok] {len(grid_results)} grid combos evaluated, {len(top)} confirmed on out-of-sample")
    for r in top:
        oos_e = f"{r.oos_stats.expectancy_r:+.3f}R" if r.oos_stats else "n/a"
        print(f"    score>={r.score_threshold} atr={r.atr_stop_mult} rr={r.min_rr} "
              f"IS_exp={r.is_stats.expectancy_r:+.3f}R OOS_exp={oos_e} overfit={r.overfit_flag}")

    print("\n" + "=" * 70)
    print("SMOKE TEST PASSED. Pipeline runs end-to-end without crashing.")
    print("Again: this used synthetic random-walk data, not real markets --")
    print("run `python run_backtest.py --ticker <X> --tf <Y>` for real results.")
    print("=" * 70)


if __name__ == "__main__":
    main()
