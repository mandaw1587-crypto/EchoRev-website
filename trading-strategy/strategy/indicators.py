"""
Technical indicators matching Pine Script's ta.* semantics.

Pine's ta.ema/ta.rsi/ta.atr all use Wilder-style recursive smoothing (RSI and
ATR use alpha = 1/length, i.e. RMA; EMA uses alpha = 2/(length+1)). We
replicate that exactly rather than using pandas' default spans, since a plain
SMA-seeded EMA drifts from Pine's values over long series.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from config import IndicatorConfig


def ema(series: pd.Series, length: int) -> pd.Series:
    return series.ewm(span=length, adjust=False, min_periods=length).mean()


def rma(series: pd.Series, length: int) -> pd.Series:
    """Wilder's smoothed moving average (alpha = 1/length), used by RSI and ATR."""
    return series.ewm(alpha=1.0 / length, adjust=False, min_periods=length).mean()


def rsi(close: pd.Series, length: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = rma(gain, length)
    avg_loss = rma(loss, length)
    rs = avg_gain / avg_loss.replace(0.0, np.nan)
    out = 100 - (100 / (1 + rs))
    out = out.where(avg_loss != 0, 100.0)
    out = out.where(~((avg_gain == 0) & (avg_loss == 0)), 50.0)
    return out


def macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    macd_line = ema(close, fast) - ema(close, slow)
    signal_line = ema(macd_line, signal)
    hist = macd_line - signal_line
    return macd_line, signal_line, hist


def true_range(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    prev_close = close.shift(1)
    tr = pd.concat(
        [high - low, (high - prev_close).abs(), (low - prev_close).abs()], axis=1
    ).max(axis=1)
    return tr


def atr(high: pd.Series, low: pd.Series, close: pd.Series, length: int = 14) -> pd.Series:
    return rma(true_range(high, low, close), length)


def daily_vwap(df: pd.DataFrame) -> pd.Series:
    """
    VWAP anchored to the calendar day (resets at the first bar of each new
    session), matching Pine's ta.vwap() default daily anchor. `df.index` must
    be a tz-aware or naive DatetimeIndex.
    """
    typical = (df["high"] + df["low"] + df["close"]) / 3.0
    pv = typical * df["volume"]
    day = df.index.normalize()
    cum_pv = pv.groupby(day).cumsum()
    cum_vol = df["volume"].groupby(day).cumsum()
    return cum_pv / cum_vol.replace(0.0, np.nan)


def volume_sma(volume: pd.Series, length: int = 20) -> pd.Series:
    return volume.rolling(length, min_periods=length).mean()


def compute_all_indicators(df: pd.DataFrame, cfg: IndicatorConfig) -> pd.DataFrame:
    """
    df must have columns: open, high, low, close, volume, and a DatetimeIndex.
    Returns a copy of df with indicator columns appended. All indicators here
    are computed causally (each row only uses data up to and including that
    row) so they carry no lookahead by construction.
    """
    out = df.copy()
    out["ema9"] = ema(out["close"], cfg.ema_fast)
    out["ema20"] = ema(out["close"], cfg.ema_mid)
    out["ema50"] = ema(out["close"], cfg.ema_slow)
    out["ema200"] = ema(out["close"], cfg.ema_trend)
    out["rsi14"] = rsi(out["close"], cfg.rsi_len)
    macd_line, signal_line, hist = macd(out["close"], cfg.macd_fast, cfg.macd_slow, cfg.macd_signal)
    out["macd_line"] = macd_line
    out["macd_signal"] = signal_line
    out["macd_hist"] = hist
    out["atr14"] = atr(out["high"], out["low"], out["close"], cfg.atr_len)
    out["vwap"] = daily_vwap(out)
    out["vol_sma20"] = volume_sma(out["volume"], cfg.vol_sma_len)
    return out
