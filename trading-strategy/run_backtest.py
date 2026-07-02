#!/usr/bin/env python3
"""
Single entry point for the A+ Setup Analyzer Python port.

Examples:
    python run_backtest.py --ticker BTC/USDT --tf 1h
    python run_backtest.py --ticker SPY --tf 15m --lookback-days 60
    python run_backtest.py --ticker AAPL --tf 1h --optimize
    python run_backtest.py --all                    # every ticker x timeframe in the brief
    python run_backtest.py --all --optimize --report results/report.md
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from config import DEFAULT_CONFIG, COST_TYPE_BY_ASSET, TICK_SIZES
from data.fetchers import fetch
from strategy.pipeline import build_features
from backtest.walkforward import run_walk_forward, split_in_out_sample
from backtest.optimize import grid_search
from backtest.metrics import Stats

RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

DEFAULT_TICKERS = [
    ("SPY", "1h"), ("SPY", "15m"),
    ("QQQ", "1h"), ("QQQ", "15m"),
    ("AAPL", "1h"), ("AAPL", "15m"),
    ("TSLA", "1h"), ("TSLA", "15m"),
    ("BTC/USDT", "1h"), ("BTC/USDT", "15m"),
    ("ETH/USDT", "1h"), ("ETH/USDT", "15m"),
]


def resolve_asset_meta(ticker: str) -> tuple[str, float, bool]:
    cost_type = COST_TYPE_BY_ASSET.get(ticker, "crypto" if "/" in ticker else "stock")
    tick_size = TICK_SIZES.get(ticker, 0.01)
    return cost_type, tick_size, cost_type == "stock"


def plot_equity_curves(wf, ticker: str, tf: str) -> Path:
    fig, ax = plt.subplots(figsize=(10, 5))
    is_curve, oos_curve = wf.in_sample.equity_curve, wf.out_sample.equity_curve
    ax.plot(is_curve.index, is_curve.values, label="In-sample (70%)")
    if len(oos_curve):
        offset = is_curve.iloc[-1] - oos_curve.iloc[0] if len(is_curve) else 0.0
        ax.plot(oos_curve.index, oos_curve.values + offset, label="Out-of-sample (30%, offset to connect visually)")
    ax.axvline(wf.split_time, color="gray", linestyle="--", label="Walk-forward split")
    ax.set_title(f"{ticker} {tf} — equity curve")
    ax.set_ylabel("Equity ($)")
    ax.legend()
    fig.tight_layout()
    fname = RESULTS_DIR / f"equity_{ticker.replace('/', '-')}_{tf}.png"
    fig.savefig(fname, dpi=120)
    plt.close(fig)
    return fname


def stats_row(label: str, s: Stats) -> str:
    return (f"| {label} | {s.total_trades} | {s.win_rate:.1f}% | {s.profit_factor:.2f} | "
            f"{s.expectancy_r:+.3f}R | {s.avg_win_r:+.2f}R | {s.avg_loss_r:+.2f}R | "
            f"{s.max_drawdown_pct:.1f}% | {s.sharpe:.2f} | {s.avg_trade_duration_bars:.1f} | "
            f"{s.total_return_pct:+.1f}% |")


STATS_HEADER = ("| Split | Trades | Win rate | Profit factor | Expectancy | Avg win | Avg loss | "
                 "Max DD | Sharpe | Avg duration (bars) | Total return |\n"
                 "|---|---|---|---|---|---|---|---|---|---|---|")


def run_one(ticker: str, tf: str, lookback_days: int, optimize: bool, cfg=DEFAULT_CONFIG) -> dict:
    cost_type, tick_size, is_stock = resolve_asset_meta(ticker)
    df_raw = fetch(ticker, tf, lookback_days)
    if len(df_raw) < 250:
        print(f"[run_backtest] WARNING: only {len(df_raw)} bars for {ticker} {tf} -- "
              f"too little history for reliable EMA200/pivot warmup or a meaningful walk-forward split.")

    df_feat = build_features(df_raw, cfg)
    wf = run_walk_forward(df_feat, cfg, cost_type, tick_size, tf, is_stock)
    plot_path = plot_equity_curves(wf, ticker, tf)

    print(f"\n=== {ticker} {tf} ({df_raw.index.min()} -> {df_raw.index.max()}, {len(df_raw)} bars) ===")
    print(STATS_HEADER)
    print(stats_row("In-sample", wf.in_sample_stats))
    print(stats_row("Out-of-sample", wf.out_sample_stats))
    print(f"Equity curve saved to {plot_path}")

    out = {
        "ticker": ticker, "tf": tf, "df_raw": df_raw, "wf": wf, "plot_path": plot_path,
        "grid_results": None, "grid_top": None,
    }

    if optimize:
        df_is, df_oos = split_in_out_sample(df_feat, cfg.walk_forward.in_sample_frac)
        print(f"\n[run_backtest] grid search on in-sample data only "
              f"({len(cfg.optimization.score_thresholds)}x{len(cfg.optimization.atr_stop_mults)}"
              f"x{len(cfg.optimization.min_rrs)} = "
              f"{len(cfg.optimization.score_thresholds)*len(cfg.optimization.atr_stop_mults)*len(cfg.optimization.min_rrs)} combos)...")
        grid_results, top = grid_search(df_is, df_oos, cfg, cost_type, tick_size, tf, is_stock)
        print(f"[run_backtest] top {len(top)} candidates by in-sample expectancy, confirmed on out-of-sample:")
        print("| score>= | ATR mult | min R/R | IS trades | IS expectancy | OOS trades | OOS expectancy | overfit? |")
        print("|---|---|---|---|---|---|---|---|")
        for r in top:
            oos_txt = f"{r.oos_stats.expectancy_r:+.3f}R" if r.oos_stats else "n/a"
            oos_trades = r.oos_stats.total_trades if r.oos_stats else "n/a"
            flag = "YES -- overfit" if r.overfit_flag else "no"
            print(f"| {r.score_threshold} | {r.atr_stop_mult} | {r.min_rr} | {r.is_stats.total_trades} | "
                  f"{r.is_stats.expectancy_r:+.3f}R | {oos_trades} | {oos_txt} | {flag} |")
        out["grid_results"], out["grid_top"] = grid_results, top

    return out


def write_report(all_results: list[dict], report_path: Path, lookback_days: int) -> None:
    lines = ["# A+ Setup Analyzer — Backtest Report", "",
              f"Generated by `run_backtest.py`. Requested lookback: {lookback_days} days per ticker "
              f"(actual coverage per ticker/timeframe is shown below and may be shorter -- see "
              f"README's data-limitation notes for intraday stock history via Yahoo Finance).", ""]

    for r in all_results:
        ticker, tf = r["ticker"], r["tf"]
        df_raw, wf = r["df_raw"], r["wf"]
        lines += [f"## {ticker} {tf}", "",
                   f"Data range: {df_raw.index.min()} -> {df_raw.index.max()} ({len(df_raw)} bars)", "",
                   STATS_HEADER,
                   stats_row("In-sample (70%)", wf.in_sample_stats),
                   stats_row("Out-of-sample (30%)", wf.out_sample_stats), "",
                   f"![{ticker} {tf} equity curve]({r['plot_path'].name})", ""]
        if r["grid_top"]:
            lines += ["**Grid search (in-sample fit, out-of-sample confirmed):**", "",
                       "| score>= | ATR mult | min R/R | IS trades | IS expectancy | OOS trades | "
                       "OOS expectancy | overfit? |",
                       "|---|---|---|---|---|---|---|---|"]
            for gr in r["grid_top"]:
                oos_txt = f"{gr.oos_stats.expectancy_r:+.3f}R" if gr.oos_stats else "n/a"
                oos_trades = gr.oos_stats.total_trades if gr.oos_stats else "n/a"
                flag = "YES -- overfit" if gr.overfit_flag else "no"
                lines.append(f"| {gr.score_threshold} | {gr.atr_stop_mult} | {gr.min_rr} | "
                              f"{gr.is_stats.total_trades} | {gr.is_stats.expectancy_r:+.3f}R | "
                              f"{oos_trades} | {oos_txt} | {flag} |")
            lines.append("")

    report_path.write_text("\n".join(lines))
    print(f"\n[run_backtest] wrote {report_path}")


def main():
    p = argparse.ArgumentParser(description="Backtest the A+ Setup Analyzer port.")
    p.add_argument("--ticker", help="e.g. SPY, AAPL, BTC/USDT")
    p.add_argument("--tf", default="1h", help="1h or 15m (default 1h)")
    p.add_argument("--lookback-days", type=int, default=730, help="requested history in days (default 730 = ~2y)")
    p.add_argument("--optimize", action="store_true", help="run the in-sample grid search after the baseline")
    p.add_argument("--all", action="store_true", help="run every ticker/timeframe combo from the brief")
    p.add_argument("--report", default=str(RESULTS_DIR / "report.md"), help="path to write the markdown report")
    args = p.parse_args()

    if not args.all and not args.ticker:
        p.error("pass --ticker TICKER or --all")

    combos = DEFAULT_TICKERS if args.all else [(args.ticker, args.tf)]
    all_results = []
    for ticker, tf in combos:
        try:
            all_results.append(run_one(ticker, tf, args.lookback_days, args.optimize))
        except Exception as e:  # noqa: BLE001 -- keep going through the rest of the batch
            print(f"[run_backtest] FAILED {ticker} {tf}: {e}", file=sys.stderr)

    if all_results:
        write_report(all_results, Path(args.report), args.lookback_days)


if __name__ == "__main__":
    main()
