"""
OHLCV fetchers: yfinance for stocks, ccxt for crypto. Both cache to
data/cache/*.csv so repeated runs (e.g. during grid-search optimization)
don't re-hit the network.

IMPORTANT DATA LIMITATION (read before assuming you have 2 years of 15m
bars): Yahoo Finance's free intraday endpoints are historically capped --
15m/5m/2m bars are only available for roughly the trailing 60 calendar days,
1m for ~7-30 days, and only 60m/1h bars go back the full ~730 days. This is a
Yahoo-side restriction, not something this code can work around. So:
  - "SPY/QQQ/AAPL/TSLA" at tf=1h: ~2 years is achievable.
  - "SPY/QQQ/AAPL/TSLA" at tf=15m: you will get ~60 days, not 2 years. The
    fetcher does not silently pretend otherwise -- it fetches what the API
    actually returns and logs the resulting date range so you can see the
    real coverage before trusting any stats built on it.
  - Crypto via ccxt/Binance has no such limitation -- 15m/1h go back however
    far the exchange's history goes, fetched here via paginated
    fetch_ohlcv() calls.
If you need genuine 2-year 15m stock history, you'll need a paid data
vendor (Polygon, Databento, IBKR, etc.) -- swap it in behind the same
fetch_stock_data() signature.
"""
from __future__ import annotations

import time
from pathlib import Path

import pandas as pd

CACHE_DIR = Path(__file__).resolve().parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)

_YF_INTRADAY_MAX_DAYS = {
    "1m": 7, "2m": 60, "5m": 60, "15m": 60, "30m": 60, "90m": 60, "60m": 730, "1h": 730,
}


def _cache_path(symbol: str, tf: str, source: str) -> Path:
    safe = symbol.replace("/", "-")
    return CACHE_DIR / f"{source}_{safe}_{tf}.csv"


def _normalize_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={c: c.lower() for c in df.columns})
    df = df[["open", "high", "low", "close", "volume"]].astype(float)
    df = df[~df.index.duplicated(keep="last")].sort_index()
    return df


def fetch_stock_data(ticker: str, interval: str = "1h", lookback_days: int = 730,
                      use_cache: bool = True, force_refresh: bool = False) -> pd.DataFrame:
    """
    interval: yfinance interval string, e.g. "1h", "15m", "1d".
    lookback_days: how far back you WANT; actual coverage is capped by Yahoo
    (see module docstring) and the real range actually returned is logged.
    """
    import yfinance as yf

    cache_file = _cache_path(ticker, interval, "yf")
    if use_cache and not force_refresh and cache_file.exists():
        df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
        print(f"[fetchers] loaded {ticker} {interval} from cache: "
              f"{df.index.min()} -> {df.index.max()} ({len(df)} bars)")
        return df

    max_days = _YF_INTRADAY_MAX_DAYS.get(interval, lookback_days)
    effective_days = min(lookback_days, max_days)
    if effective_days < lookback_days:
        print(f"[fetchers] WARNING: Yahoo caps '{interval}' history at ~{max_days}d; "
              f"requested {lookback_days}d, fetching {effective_days}d instead. "
              f"This is a real data-availability limit, not a bug.")

    period = f"{effective_days}d"
    raw = yf.download(ticker, period=period, interval=interval, auto_adjust=True,
                       progress=False, multi_level_index=False)
    if raw.empty:
        raise RuntimeError(f"yfinance returned no data for {ticker} @ {interval}")

    df = _normalize_ohlcv(raw)
    print(f"[fetchers] fetched {ticker} {interval}: {df.index.min()} -> {df.index.max()} ({len(df)} bars)")
    if use_cache:
        df.to_csv(cache_file)
    return df


def fetch_crypto_data(symbol: str = "BTC/USDT", timeframe: str = "1h", lookback_days: int = 730,
                       exchange_id: str = "binance", use_cache: bool = True,
                       force_refresh: bool = False) -> pd.DataFrame:
    """Paginated OHLCV pull via ccxt -- Binance keeps full history, so 2+
    years at 15m/1h is achievable here (unlike the yfinance stock path)."""
    import ccxt

    cache_file = _cache_path(symbol, timeframe, exchange_id)
    if use_cache and not force_refresh and cache_file.exists():
        df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
        print(f"[fetchers] loaded {symbol} {timeframe} from cache: "
              f"{df.index.min()} -> {df.index.max()} ({len(df)} bars)")
        return df

    exchange = getattr(ccxt, exchange_id)({"enableRateLimit": True})
    tf_ms = exchange.parse_timeframe(timeframe) * 1000
    since = exchange.milliseconds() - lookback_days * 24 * 60 * 60 * 1000
    limit = 1000

    now_ms = exchange.milliseconds()
    rows = []
    while True:
        batch = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
        if not batch:
            break
        rows.extend(batch)
        next_since = batch[-1][0] + tf_ms
        if next_since <= since or next_since >= now_ms or len(batch) < limit:
            break
        since = next_since
        time.sleep(exchange.rateLimit / 1000.0)

    if not rows:
        raise RuntimeError(f"ccxt returned no data for {symbol} @ {timeframe}")

    raw = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "volume"])
    raw = raw.drop_duplicates(subset="ts").sort_values("ts")
    raw.index = pd.to_datetime(raw["ts"], unit="ms", utc=True)
    df = _normalize_ohlcv(raw)

    print(f"[fetchers] fetched {symbol} {timeframe}: {df.index.min()} -> {df.index.max()} ({len(df)} bars)")
    if use_cache:
        df.to_csv(cache_file)
    return df


def fetch(symbol: str, timeframe: str, lookback_days: int = 730, **kwargs) -> pd.DataFrame:
    """Dispatch to the crypto or stock fetcher based on symbol shape (contains '/')."""
    if "/" in symbol:
        return fetch_crypto_data(symbol, timeframe, lookback_days, **kwargs)
    return fetch_stock_data(symbol, timeframe, lookback_days, **kwargs)
