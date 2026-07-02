"""
Custom event-driven backtest engine.

WHY NOT backtesting.py / vectorbt: this strategy scales out of a position at
three separate R-multiple targets, moves its stop to breakeven after the
first scale-out, and then trails the remainder under swing structure. That's
a stateful, multi-leg position-management routine that neither
backtesting.py (single bracket SL/TP per trade) nor vectorbt (vectorized,
awkward for path-dependent partial exits) models cleanly or transparently.
A ~300-line bar-by-bar loop over pandas rows is easy to audit line-by-line
for lookahead bugs, which matters more here than raw speed -- see the
"honesty rules" in the project brief. Runtime is still fine: a few seconds
per ticker/timeframe even at 15m granularity over 2 years.

LOOKAHEAD / EXECUTION MODEL:
  - Signals are evaluated on bar i using only data confirmed as of bar i's
    close (indicators, structure, scores are all causal -- see
    strategy/indicators.py and strategy/structure.py).
  - A qualifying signal at bar i is filled at bar i+1's OPEN (never at bar
    i's own close), i.e. the next tradable price after the decision.
  - Every fill (entry, stop, TP1/TP2/TP3) is nudged by 1 tick against the
    trader on top of commission, and gap-through bars fill at the open price
    when the open itself is already beyond the stop/target (see
    backtest/costs.py and _fill_price below).
  - Within a single bar with an open position, at most ONE exit event is
    processed (current stop first -- worst case for the trader -- otherwise
    the next unfilled target in TP1->TP2->TP3 order). This avoids guessing
    the intrabar path when a wide-range bar could technically satisfy two
    levels; the alternative (letting a bar cascade through TP1 and TP2 in
    one shot) would systematically flatter results.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from config import StrategyConfig
from backtest.costs import commission_cost, apply_slippage
from strategy.risk import build_trade_plan
from strategy.signals import evaluate_signal


@dataclass
class ExitFill:
    time: pd.Timestamp
    price: float
    size: float
    reason: str  # "stop" | "tp1" | "tp2" | "tp3"


@dataclass
class ClosedTrade:
    direction: str
    entry_time: pd.Timestamp
    entry_price: float
    orig_size: float
    r_distance: float
    stop_initial: float
    entry_bar: int
    exit_bar: int
    exits: list[ExitFill] = field(default_factory=list)
    commission_paid: float = 0.0

    @property
    def exit_time(self) -> pd.Timestamp:
        return self.exits[-1].time

    @property
    def pnl(self) -> float:
        sign = 1 if self.direction == "long" else -1
        gross = sum(sign * (e.price - self.entry_price) * e.size for e in self.exits)
        return gross - self.commission_paid

    @property
    def r_multiple(self) -> float:
        if self.r_distance <= 0:
            return 0.0
        sign = 1 if self.direction == "long" else -1
        weighted = sum(sign * (e.price - self.entry_price) * e.size for e in self.exits)
        return weighted / (self.r_distance * self.orig_size)

    @property
    def exit_reason(self) -> str:
        return self.exits[-1].reason if self.exits else ""

    @property
    def bars_held(self) -> int:
        return self.exit_bar - self.entry_bar


@dataclass
class BacktestResult:
    trades: list[ClosedTrade]
    equity_curve: pd.Series
    final_equity: float


@dataclass
class _OpenPosition:
    direction: str
    entry_time: pd.Timestamp
    entry_bar: int
    entry_price: float
    orig_size: float
    remaining_size: float
    stop: float
    stop_initial: float
    tp1: float
    tp2: float
    tp3: float
    r_distance: float
    filled_tp1: bool = False
    filled_tp2: bool = False
    exits: list = field(default_factory=list)
    commission_paid: float = 0.0

    def unrealized(self, price: float) -> float:
        sign = 1 if self.direction == "long" else -1
        return sign * (price - self.entry_price) * self.remaining_size


def _fill_price(open_: float, level: float, direction: str, side: str) -> float:
    """
    side: "stop" or "target". Handles gap-through bars: if the bar's open is
    already past the level, fill at the open (can't fill better than the
    market gapped); otherwise fill at the level itself (assume the resting
    stop/limit order executes there).
    """
    if direction == "long":
        return min(open_, level) if side == "stop" else max(open_, level)
    else:
        return max(open_, level) if side == "stop" else min(open_, level)


def simulate(
    df: pd.DataFrame,
    cfg: StrategyConfig,
    cost_type: str,
    tick_size: float,
    initial_equity: float = 100_000.0,
    fractional: bool = True,
) -> BacktestResult:
    """
    df must already have indicators, structure, and score columns (see
    strategy/indicators.py, strategy/structure.py, strategy/scoring.py) and
    an 'htf_bias' column.
    """
    n = len(df)
    idx = df.index
    o = df["open"].to_numpy()
    h = df["high"].to_numpy()
    l = df["low"].to_numpy()
    c = df["close"].to_numpy()
    atr = df["atr14"].to_numpy()
    last_pl = df["last_pivot_low"].to_numpy()
    last_ph = df["last_pivot_high"].to_numpy()

    equity = initial_equity
    equity_curve = np.empty(n)
    trades: list[ClosedTrade] = []

    position: _OpenPosition | None = None
    pending_direction: str | None = None
    pending_stop = pending_tp1 = pending_tp2 = pending_tp3 = pending_r = pending_size = None
    last_signal_bar: int | None = None

    tp1_frac = cfg.risk.tp1_close_pct
    tp2_frac = cfg.risk.tp2_close_pct
    tp3_frac = 1.0 - tp1_frac - tp2_frac

    for i in range(n):
        row_time = idx[i]

        # --- 1. Fill a pending entry scheduled from bar i-1 ---
        if pending_direction is not None:
            direction = pending_direction
            adverse = 1 if direction == "long" else -1
            raw_entry = o[i]
            entry_price = apply_slippage(raw_entry, adverse, tick_size, cfg.cost.slippage_ticks)
            commission = commission_cost(entry_price * pending_size, cost_type, cfg.cost)
            position = _OpenPosition(
                direction=direction, entry_time=row_time, entry_bar=i, entry_price=entry_price,
                orig_size=pending_size, remaining_size=pending_size, stop=pending_stop,
                stop_initial=pending_stop,
                tp1=pending_tp1, tp2=pending_tp2, tp3=pending_tp3, r_distance=pending_r,
                commission_paid=commission,
            )
            equity -= commission
            pending_direction = None

        # --- 2. Manage an open position against this bar's range ---
        if position is not None:
            direction = position.direction
            sign = 1 if direction == "long" else -1

            stop_hit = (l[i] <= position.stop) if direction == "long" else (h[i] >= position.stop)
            if stop_hit:
                fill = _fill_price(o[i], position.stop, direction, "stop")
                fill = apply_slippage(fill, sign, tick_size, cfg.cost.slippage_ticks)
                notional = fill * position.remaining_size
                comm = commission_cost(notional, cost_type, cfg.cost)
                position.exits.append(ExitFill(row_time, fill, position.remaining_size, "stop"))
                position.commission_paid += comm
                equity += sign * (fill - position.entry_price) * position.remaining_size - comm
                position.remaining_size = 0.0
                trade = ClosedTrade(direction, position.entry_time, position.entry_price,
                                     position.orig_size, position.r_distance, position.stop_initial,
                                     position.entry_bar, i, position.exits, position.commission_paid)
                trades.append(trade)
                position = None
            else:
                next_target = None
                next_frac = None
                next_label = None
                if not position.filled_tp1:
                    next_target, next_frac, next_label = position.tp1, tp1_frac, "tp1"
                elif not position.filled_tp2:
                    next_target, next_frac, next_label = position.tp2, tp2_frac, "tp2"
                else:
                    next_target, next_frac, next_label = position.tp3, tp3_frac, "tp3"

                target_hit = (h[i] >= next_target) if direction == "long" else (l[i] <= next_target)
                if target_hit:
                    fill = _fill_price(o[i], next_target, direction, "target")
                    fill = apply_slippage(fill, -sign, tick_size, cfg.cost.slippage_ticks)
                    close_size = position.orig_size * next_frac if next_label != "tp3" \
                        else position.remaining_size
                    close_size = min(close_size, position.remaining_size)
                    notional = fill * close_size
                    comm = commission_cost(notional, cost_type, cfg.cost)
                    position.exits.append(ExitFill(row_time, fill, close_size, next_label))
                    position.commission_paid += comm
                    equity += sign * (fill - position.entry_price) * close_size - comm
                    position.remaining_size -= close_size

                    if next_label == "tp1":
                        position.filled_tp1 = True
                        position.stop = position.entry_price  # move to breakeven
                    elif next_label == "tp2":
                        position.filled_tp2 = True

                    if position.remaining_size <= 1e-9:
                        trade = ClosedTrade(direction, position.entry_time, position.entry_price,
                                             position.orig_size, position.r_distance, position.stop_initial,
                                             position.entry_bar, i, position.exits, position.commission_paid)
                        trades.append(trade)
                        position = None
                elif position.filled_tp1:
                    # Trail stop toward the newest CONFIRMED swing extreme.
                    # position.stop already sits at breakeven (set when TP1
                    # filled), and max()/min() here only ever tighten it
                    # further, so it can never trail back below breakeven.
                    if direction == "long" and last_pl[i] == last_pl[i]:  # not NaN
                        position.stop = max(position.stop, last_pl[i])
                    elif direction == "short" and last_ph[i] == last_ph[i]:
                        position.stop = min(position.stop, last_ph[i])

        # --- 3. Evaluate a new signal on this confirmed bar (only if flat) ---
        if position is None and pending_direction is None:
            cooldown_ok = last_signal_bar is None or (i - last_signal_bar) >= cfg.entry.cooldown_bars
            if cooldown_ok and i + 1 < n:
                row = df.iloc[i]
                direction = evaluate_signal(row, cfg)
                if direction is not None:
                    last_signal_bar = i
                    plan = build_trade_plan(
                        direction, c[i], atr[i], last_pl[i], last_ph[i], equity, cfg.risk,
                        fractional=fractional,
                    )
                    if plan is not None:
                        pending_direction = direction
                        pending_stop, pending_tp1, pending_tp2, pending_tp3 = plan.stop, plan.tp1, plan.tp2, plan.tp3
                        pending_r, pending_size = plan.r_distance, plan.size

        # --- 4. Mark-to-market equity for this bar ---
        mtm = position.unrealized(c[i]) if position is not None else 0.0
        equity_curve[i] = equity + mtm

    return BacktestResult(trades=trades, equity_curve=pd.Series(equity_curve, index=idx), final_equity=equity)
