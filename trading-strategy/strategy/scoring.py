"""
Higher-timeframe filter and confluence scoring (0-100), computed separately
for the long and short case at every bar. See a_plus_setup_analyzer.pine for
the point weights and the [ASSUMPTION]-tagged rules this implements.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from config import StrategyConfig
from strategy.indicators import ema


def compute_htf_bias(df: pd.DataFrame, ema_len: int = 50) -> pd.Series:
    """
    Daily close vs daily EMA50, mapped back onto the intraday index. Uses only
    the LAST COMPLETED daily bar for every intraday bar in the following
    session -- the still-forming "today" daily bar is never used, which is
    what keeps this lookahead-free (an intraday bar at 10:30 today must not
    see today's not-yet-final daily close/EMA).

    Returns a Series of {1: bullish, -1: bearish, 0: unknown/insufficient data}
    aligned to df.index.
    """
    daily = df["close"].resample("1D").last().dropna()
    daily_ema = ema(daily, ema_len)
    daily_bias = pd.Series(
        np.where(daily > daily_ema, 1, np.where(daily < daily_ema, -1, 0)),
        index=daily.index,
    )
    # Shift by one COMPLETED day: bias known for "today" is actually
    # yesterday's completed daily bar's bias.
    daily_bias_lagged = daily_bias.shift(1)

    day_key = df.index.normalize()
    mapped = day_key.map(daily_bias_lagged)
    return pd.Series(mapped, index=df.index).fillna(0).astype(int)


def _ema_stack_score_vec(df: pd.DataFrame, direction: str, w) -> np.ndarray:
    if direction == "long":
        checks = [df["ema9"] > df["ema20"], df["ema20"] > df["ema50"], df["ema9"] > df["ema50"]]
    else:
        checks = [df["ema9"] < df["ema20"], df["ema20"] < df["ema50"], df["ema9"] < df["ema50"]]
    passed = sum(c.astype(int) for c in checks)
    return np.select([passed == 3, passed == 2], [w.ema_stack, w.ema_stack_partial], default=0.0)


def _rsi_band_score_vec(rsi_series: pd.Series, direction: str, cfg: StrategyConfig) -> np.ndarray:
    lo, hi = cfg.thresholds.rsi_long_band if direction == "long" else cfg.thresholds.rsi_short_band
    in_band = (rsi_series >= lo) & (rsi_series <= hi)
    return np.where(in_band.fillna(False), cfg.weights.rsi_band, 0.0)


def _volume_score_vec(volume: pd.Series, vol_sma: pd.Series, cfg: StrategyConfig) -> np.ndarray:
    ratio = volume / vol_sma.replace(0.0, np.nan)
    return np.select(
        [ratio > cfg.thresholds.volume_full_mult, ratio > cfg.thresholds.volume_partial_mult],
        [cfg.weights.volume_full, cfg.weights.volume_partial],
        default=0.0,
    )


def _near_structure_score_vec(df: pd.DataFrame, direction: str, cfg: StrategyConfig) -> np.ndarray:
    ref = df["last_pivot_low"] if direction == "long" else df["last_pivot_high"]
    dist = (df["close"] - ref).abs()
    within = dist <= cfg.thresholds.near_structure_atr_mult * df["atr14"]
    return np.where(within.fillna(False), cfg.weights.near_structure, 0.0)


def compute_confluence_scores(df: pd.DataFrame, cfg: StrategyConfig) -> pd.DataFrame:
    """
    df must already have indicators (indicators.py) and structure
    (structure.py) columns, plus an 'htf_bias' column (compute_htf_bias).
    Adds 'score_long' and 'score_short' columns, each clamped to [0, 100].
    """
    out = df.copy()
    w = cfg.weights

    structure_long = np.where(out["bullish_structure"], w.structure, 0.0)
    structure_short = np.where(out["bearish_structure"], w.structure, 0.0)

    ema200_long = np.where(out["close"] > out["ema200"], w.ema200, 0.0)
    ema200_short = np.where(out["close"] < out["ema200"], w.ema200, 0.0)

    vwap_long = np.where(out["close"] > out["vwap"], w.vwap, 0.0)
    vwap_short = np.where(out["close"] < out["vwap"], w.vwap, 0.0)

    macd_long = np.where((out["macd_line"] > out["macd_signal"]) & (out["macd_hist"] > 0), w.macd, 0.0)
    macd_short = np.where((out["macd_line"] < out["macd_signal"]) & (out["macd_hist"] < 0), w.macd, 0.0)

    fvg_long = np.where(out["has_active_bull_fvg"], w.fvg, 0.0)
    fvg_short = np.where(out["has_active_bear_fvg"], w.fvg, 0.0)

    htf_long = np.where(out["htf_bias"] == 1, w.htf, 0.0)
    htf_short = np.where(out["htf_bias"] == -1, w.htf, 0.0)

    penalty_long = np.where(out["fake_breakout_bear"], w.fake_breakout_penalty, 0.0)
    penalty_short = np.where(out["fake_breakout_bull"], w.fake_breakout_penalty, 0.0)

    ema_stack_long = _ema_stack_score_vec(out, "long", w)
    ema_stack_short = _ema_stack_score_vec(out, "short", w)
    rsi_long = _rsi_band_score_vec(out["rsi14"], "long", cfg)
    rsi_short = _rsi_band_score_vec(out["rsi14"], "short", cfg)
    vol_score = _volume_score_vec(out["volume"], out["vol_sma20"], cfg)
    near_long = _near_structure_score_vec(out, "long", cfg)
    near_short = _near_structure_score_vec(out, "short", cfg)

    score_long = (
        structure_long + ema_stack_long + ema200_long + vwap_long + rsi_long
        + macd_long + vol_score + near_long + fvg_long + htf_long + penalty_long
    )
    score_short = (
        structure_short + ema_stack_short + ema200_short + vwap_short + rsi_short
        + macd_short + vol_score + near_short + fvg_short + htf_short + penalty_short
    )

    out["score_long"] = np.clip(score_long, 0, 100)
    out["score_short"] = np.clip(score_short, 0, 100)
    return out
