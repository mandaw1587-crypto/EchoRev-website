"""
Market structure: confirmed pivots, HH/HL/LH/LL classification, Fair Value
Gaps, and fake-breakout detection.

LOOKAHEAD SAFETY: a 5-left/5-right pivot cannot be known until 5 bars after
it forms (you need the 5 bars to its right to confirm it's a local extreme).
Every "last pivot" value used anywhere in this module (and consumed by
scoring.py / the backtest engine) is shifted so it only becomes visible on
its confirmation bar, never on the bar it actually occurred on.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from config import StructureConfig


def _confirmed_pivots(price: pd.Series, left: int, right: int, is_high: bool) -> pd.Series:
    """
    Returns a series aligned to `price.index` that is NaN everywhere except on
    confirmation bars (index i + right), where it holds the pivot price that
    formed at bar i. Uses a centered rolling window purely to *identify* the
    extreme (that's just arithmetic on already-known future values once we're
    at the confirmation bar) then shifts forward by `right` bars so the value
    is only exposed once genuinely known.
    """
    window = left + right + 1
    roll_extreme = price.rolling(window, center=True).max() if is_high else price.rolling(window, center=True).min()
    is_pivot = (price == roll_extreme) & roll_extreme.notna()
    pivot_val = price.where(is_pivot)
    return pivot_val.shift(right)


def _last_and_prev(events: pd.Series, full_index: pd.Index) -> tuple[pd.Series, pd.Series]:
    """
    events: sparse series (NaN except on confirmation bars) already aligned to
    full_index. Returns (last_value_as_of_each_bar, previous_value_as_of_each_bar)
    both forward-filled so every bar knows the two most recent CONFIRMED pivots.
    """
    ev = events.dropna()
    last = events.ffill()
    prev_at_events = pd.Series(ev.shift(1).values, index=ev.index)
    prev = prev_at_events.reindex(full_index).ffill()
    return last, prev


def compute_structure(df: pd.DataFrame, cfg: StructureConfig) -> pd.DataFrame:
    """
    df needs columns: high, low, close. Returns df with structure columns
    appended. All columns are lookahead-safe: at bar j they only reflect
    information confirmed on or before bar j.
    """
    out = df.copy()
    left, right = cfg.pivot_left, cfg.pivot_right

    ph_events = _confirmed_pivots(out["high"], left, right, is_high=True)
    pl_events = _confirmed_pivots(out["low"], left, right, is_high=False)
    out["pivot_high_confirmed"] = ph_events
    out["pivot_low_confirmed"] = pl_events

    last_ph, prev_ph = _last_and_prev(ph_events, out.index)
    last_pl, prev_pl = _last_and_prev(pl_events, out.index)
    out["last_pivot_high"] = last_ph
    out["prev_pivot_high"] = prev_ph
    out["last_pivot_low"] = last_pl
    out["prev_pivot_low"] = prev_pl

    out["bullish_structure"] = (last_ph > prev_ph) & (last_pl > prev_pl)
    out["bearish_structure"] = (last_ph < prev_ph) & (last_pl < prev_pl)

    # Fake breakout: wick through the *currently known* pivot with close back inside.
    # Bearish fake breakout (false break of resistance): high pokes above last
    # confirmed pivot high, close comes back under it.
    out["fake_breakout_bear"] = (out["high"] > last_ph) & (out["close"] < last_ph) & last_ph.notna()
    # Bullish fake breakout (false break of support): low pokes below last
    # confirmed pivot low, close comes back above it.
    out["fake_breakout_bull"] = (out["low"] < last_pl) & (out["close"] > last_pl) & last_pl.notna()

    # --- Fair Value Gaps (3-bar), formed causally at bar i using bars i, i-1, i-2 ---
    high_2back = out["high"].shift(2)
    low_2back = out["low"].shift(2)
    bull_fvg_formed = out["low"] > high_2back
    bear_fvg_formed = out["high"] < low_2back
    out["bull_fvg_formed"] = bull_fvg_formed
    out["bear_fvg_formed"] = bear_fvg_formed
    out["bull_fvg_gap_low"] = np.where(bull_fvg_formed, high_2back, np.nan)
    out["bull_fvg_gap_high"] = np.where(bull_fvg_formed, out["low"], np.nan)
    out["bear_fvg_gap_low"] = np.where(bear_fvg_formed, out["high"], np.nan)
    out["bear_fvg_gap_high"] = np.where(bear_fvg_formed, low_2back, np.nan)

    out["has_active_bull_fvg"], out["has_active_bear_fvg"] = _active_fvg_flags(out, cfg.fvg_valid_bars)
    return out


def _active_fvg_flags(df: pd.DataFrame, valid_bars: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Single forward pass tracking open (unfilled, not-yet-expired) FVGs. A
    bullish FVG [gap_low, gap_high] is filled once price trades back down to
    gap_low (low <= gap_low); a bearish FVG is filled once price trades back
    up to gap_high (high >= gap_high). Both expire after `valid_bars` bars.
    """
    n = len(df)
    has_bull = np.zeros(n, dtype=bool)
    has_bear = np.zeros(n, dtype=bool)
    bull_gaps: list[tuple[int, float]] = []  # (formed_at_idx, gap_low)
    bear_gaps: list[tuple[int, float]] = []  # (formed_at_idx, gap_high)

    lows = df["low"].to_numpy()
    highs = df["high"].to_numpy()
    bull_formed = df["bull_fvg_formed"].to_numpy()
    bear_formed = df["bear_fvg_formed"].to_numpy()
    bull_gap_low = df["bull_fvg_gap_low"].to_numpy()
    bear_gap_high = df["bear_fvg_gap_high"].to_numpy()

    for i in range(n):
        bull_gaps = [(t, gl) for (t, gl) in bull_gaps if (i - t) <= valid_bars and lows[i] > gl]
        bear_gaps = [(t, gh) for (t, gh) in bear_gaps if (i - t) <= valid_bars and highs[i] < gh]

        if bull_formed[i] and not np.isnan(bull_gap_low[i]):
            bull_gaps.append((i, bull_gap_low[i]))
        if bear_formed[i] and not np.isnan(bear_gap_high[i]):
            bear_gaps.append((i, bear_gap_high[i]))

        has_bull[i] = len(bull_gaps) > 0
        has_bear[i] = len(bear_gaps) > 0

    return has_bull, has_bear
