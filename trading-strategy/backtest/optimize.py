"""
Grid search over (score threshold, ATR stop multiplier, min R/R), fit ONLY on
in-sample data. The top candidates by in-sample expectancy are then run
against the untouched out-of-sample slice for confirmation -- parameter sets
whose edge doesn't survive that step are exactly the overfit cases the
project brief asks to flag, not to hide.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, replace

import pandas as pd

from config import StrategyConfig
from backtest.engine import simulate
from backtest.metrics import compute_metrics, Stats


@dataclass
class GridResult:
    score_threshold: float
    atr_stop_mult: float
    min_rr: float
    is_stats: Stats
    oos_stats: Stats | None = None

    @property
    def overfit_flag(self) -> bool:
        """
        True if this parameter set looked good in-sample but its edge
        collapses or reverses out-of-sample. "Collapses" = OOS expectancy is
        negative while IS expectancy was clearly positive, or OOS expectancy
        is less than half of IS expectancy.
        """
        if self.oos_stats is None:
            return False
        if self.is_stats.expectancy_r <= 0:
            return False
        if self.oos_stats.expectancy_r <= 0:
            return True
        return self.oos_stats.expectancy_r < 0.5 * self.is_stats.expectancy_r


def _cfg_with_params(base_cfg: StrategyConfig, score_threshold: float, atr_stop_mult: float,
                      min_rr: float) -> StrategyConfig:
    entry = replace(base_cfg.entry, min_score=score_threshold, min_rr=min_rr)
    risk = replace(base_cfg.risk, atr_stop_mult=atr_stop_mult)
    return replace(base_cfg, entry=entry, risk=risk)


def grid_search(df_is: pd.DataFrame, df_oos: pd.DataFrame, base_cfg: StrategyConfig, cost_type: str,
                 tick_size: float, timeframe: str, is_stock: bool, initial_equity: float = 100_000.0,
                 fractional: bool | None = None, top_n_confirm: int = 5) -> tuple[list[GridResult], list[GridResult]]:
    if fractional is None:
        fractional = not is_stock
    grid = base_cfg.optimization

    results: list[GridResult] = []
    for score_threshold, atr_stop_mult, min_rr in itertools.product(
        grid.score_thresholds, grid.atr_stop_mults, grid.min_rrs
    ):
        cfg = _cfg_with_params(base_cfg, score_threshold, atr_stop_mult, min_rr)
        is_result = simulate(df_is, cfg, cost_type, tick_size, initial_equity, fractional)
        is_stats = compute_metrics(is_result, timeframe, is_stock, initial_equity)
        results.append(GridResult(score_threshold, atr_stop_mult, min_rr, is_stats))

    considered = [r for r in results if r.is_stats.total_trades >= grid.min_trades_for_consideration]
    considered.sort(key=lambda r: r.is_stats.expectancy_r, reverse=True)

    top = considered[:top_n_confirm]
    for r in top:
        cfg = _cfg_with_params(base_cfg, r.score_threshold, r.atr_stop_mult, r.min_rr)
        oos_result = simulate(df_oos, cfg, cost_type, tick_size, initial_equity, fractional)
        r.oos_stats = compute_metrics(oos_result, timeframe, is_stock, initial_equity)

    return results, top
