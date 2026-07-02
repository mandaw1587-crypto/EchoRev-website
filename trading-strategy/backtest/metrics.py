"""Performance statistics computed from a BacktestResult."""
from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np
import pandas as pd

from backtest.engine import BacktestResult

# Approximate bars/year used only to annualize Sharpe -- doesn't affect any
# other reported number (win rate, expectancy, drawdown are all
# annualization-independent).
BARS_PER_YEAR = {
    "1h": 24 * 365,      # crypto default; overridden for stocks below
    "15m": 4 * 24 * 365,
    "1h_stock": int(6.5 * 252),
    "15m_stock": int(6.5 * 4 * 252),
}


def bars_per_year(timeframe: str, is_stock: bool) -> int:
    key = f"{timeframe}_stock" if is_stock and f"{timeframe}_stock" in BARS_PER_YEAR else timeframe
    return BARS_PER_YEAR.get(key, 252)


@dataclass
class Stats:
    total_trades: int
    win_rate: float
    profit_factor: float
    expectancy_r: float
    avg_win_r: float
    avg_loss_r: float
    max_drawdown_pct: float
    sharpe: float
    avg_trade_duration_bars: float
    total_return_pct: float
    final_equity: float

    def as_dict(self) -> dict:
        return asdict(self)


def _max_drawdown(equity: pd.Series) -> float:
    if equity.empty:
        return 0.0
    running_max = equity.cummax()
    dd = (equity - running_max) / running_max.replace(0, np.nan)
    return float(dd.min() * 100) if dd.notna().any() else 0.0


def _sharpe(equity: pd.Series, periods_per_year: int) -> float:
    rets = equity.pct_change().dropna()
    if rets.std(ddof=0) == 0 or len(rets) < 2:
        return 0.0
    return float((rets.mean() / rets.std(ddof=0)) * np.sqrt(periods_per_year))


def compute_metrics(result: BacktestResult, timeframe: str, is_stock: bool,
                     initial_equity: float) -> Stats:
    trades = result.trades
    n = len(trades)
    if n == 0:
        return Stats(0, 0.0, 0.0, 0.0, 0.0, 0.0,
                     _max_drawdown(result.equity_curve), 0.0, 0.0,
                     (result.final_equity / initial_equity - 1) * 100, result.final_equity)

    r_multiples = np.array([t.r_multiple for t in trades])
    pnls = np.array([t.pnl for t in trades])
    wins = pnls > 0
    losses = pnls <= 0

    gross_win = pnls[wins].sum() if wins.any() else 0.0
    gross_loss = -pnls[losses].sum() if losses.any() else 0.0
    profit_factor = (gross_win / gross_loss) if gross_loss > 0 else (float("inf") if gross_win > 0 else 0.0)

    ppy = bars_per_year(timeframe, is_stock)

    return Stats(
        total_trades=n,
        win_rate=float(wins.mean() * 100),
        profit_factor=float(profit_factor),
        expectancy_r=float(r_multiples.mean()),
        avg_win_r=float(r_multiples[wins].mean()) if wins.any() else 0.0,
        avg_loss_r=float(r_multiples[losses].mean()) if losses.any() else 0.0,
        max_drawdown_pct=_max_drawdown(result.equity_curve),
        sharpe=_sharpe(result.equity_curve, ppy),
        avg_trade_duration_bars=float(np.mean([t.bars_held for t in trades])),
        total_return_pct=(result.final_equity / initial_equity - 1) * 100,
        final_equity=result.final_equity,
    )
