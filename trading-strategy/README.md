# A+ Setup Analyzer — Python Backtest Port

A faithful Python port of the "A+ Setup Analyzer" Pine Script confluence
system, built to actually run backtests, measure real performance, and
optimize parameters (things Pine Script can't do on its own).

## Provenance — read this first

The original `a_plus_setup_analyzer.pine` file was **not present** in the
repository this project was built in. Everything here was ported from the
detailed written strategy brief (indicators, structure rules, exact point
weights, entry/exit rules, stop/target formulas, sizing) instead of the
literal source file. [`a_plus_setup_analyzer.pine`](a_plus_setup_analyzer.pine)
in this repo is a **reconstruction** written to document that same logic as
a canonical reference for the Python code — it is not a decompiled/recovered
original. Anywhere the brief left a rule underspecified (exact RSI band,
"near structure" distance, how the 50%-at-TP1 split extends to TP2/TP3,
etc.), the choice made is tagged `[ASSUMPTION]` in both that file and
`config.py`. **If you have the real `.pine` file, diff it against the
reference and tell me the deltas** — the Python code should match the real
source, not this reconstruction.

## Why a custom backtest engine instead of backtesting.py/vectorbt

This strategy scales out of a position at three separate R-multiple
targets, moves its stop to breakeven after the first scale-out, and then
trails the remainder under swing structure. That's a stateful, multi-leg
position-management routine that neither `backtesting.py` (one bracket
SL/TP per trade) nor `vectorbt` (vectorized, awkward for path-dependent
partial exits) models cleanly or transparently. `backtest/engine.py` is a
~250-line bar-by-bar loop instead — slower, but easy to audit line-by-line
for lookahead bugs, which matters more here than raw speed (see "Honesty
rules" below). It's still fast: a few seconds per ticker/timeframe even at
15-minute granularity over 2 years.

## Project layout

```
config.py                     all weights/thresholds in one place (documented + tunable)
a_plus_setup_analyzer.pine    reference spec (see Provenance above)
strategy/
  indicators.py                EMA9/20/50/200, RSI14, MACD(12,26,9), ATR14, daily VWAP, vol SMA20
  structure.py                 pivots (5/5, causal), HH/HL/LH/LL, 3-bar FVGs, fake breakouts
  scoring.py                   0-100 confluence score (long & short) + daily HTF filter
  risk.py                      stop/target/position-size math
  signals.py                   entry gate (score >= 85, R/R >= min, volume > 1.3x avg)
  pipeline.py                  composes the above into one build_features(df, cfg) call
data/
  fetchers.py                  yfinance (stocks) + ccxt (crypto), CSV cache in data/cache/
backtest/
  engine.py                    the bar-by-bar simulator (entries, partial exits, costs)
  costs.py                     commission + slippage
  metrics.py                   win rate, profit factor, expectancy (R), max DD, Sharpe, etc.
  walkforward.py               70/30 in-sample / out-of-sample split + paired run
  optimize.py                  in-sample grid search, out-of-sample confirmation, overfit flag
run_backtest.py                CLI entry point
tests/smoke_test.py            synthetic-data pipeline sanity check (NOT a performance test)
results/                       equity curve PNGs + report.md land here
```

## Setup

```bash
cd trading-strategy
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Requires Python 3.11+.

## Sanity-check the pipeline before trusting it

```bash
python tests/smoke_test.py
```

This runs the full pipeline (indicators → structure → scoring → signals →
engine → walk-forward → grid search) on **synthetic random-walk data** and
checks for crashes, NaN/out-of-range scores, non-finite equity, and a
direct lookahead check on pivot confirmation timing. It is not a
performance benchmark — synthetic data has no real edge to find. Its
output is reproduced in `results/report.md` labeled accordingly.

## Running real backtests

Single ticker/timeframe:

```bash
python run_backtest.py --ticker BTC/USDT --tf 1h
python run_backtest.py --ticker SPY --tf 1h --optimize
```

Everything from the brief in one shot (SPY/QQQ/AAPL/TSLA at 1h+15m,
BTC/USDT + ETH/USDT at 1h+15m), with grid-search optimization and a
regenerated `results/report.md`:

```bash
python run_backtest.py --all --optimize
```

Flags:
- `--ticker TICKER` — e.g. `SPY`, `AAPL`, `BTC/USDT` (slash form routes to ccxt/crypto automatically)
- `--tf 1h|15m` — timeframe (default `1h`)
- `--lookback-days N` — requested history in days (default 730 ≈ 2 years; see data limitation below)
- `--optimize` — run the in-sample grid search (score threshold, ATR stop multiplier, min R/R) and confirm the top candidates out-of-sample
- `--all` — run every ticker/timeframe combo from the brief
- `--report PATH` — where to write the markdown report (default `results/report.md`)

Each run prints an in-sample vs out-of-sample stats table to the console,
saves an equity curve PNG to `results/`, and (re)writes `results/report.md`.
Data is cached in `data/cache/*.csv` after the first fetch so repeated runs
(especially `--optimize`, which reuses the same in-sample/out-of-sample
data across the whole grid) don't keep re-hitting the network.

## Data availability — an important real constraint, not a bug

Yahoo Finance's free intraday endpoints (used via `yfinance`) are capped:
**15-minute stock bars are only available for roughly the trailing 60
days**, not 2 years — Yahoo doesn't serve more, no matter what's requested.
1-hour stock bars go back the full ~730 days. `data/fetchers.py` fetches
whatever the API actually returns, prints the real date range, and warns
loudly rather than silently truncating and pretending you have 2 years of
15-minute SPY data when you have 60 days. Crypto via `ccxt`/Binance has no
such limit — 15m and 1h both go back the full requested window. If you need
genuine 2-year 15-minute stock history, you'll need a paid vendor (Polygon,
Databento, IBKR, etc.) behind the same `fetch_stock_data()` signature.

## Honesty rules this code follows

- **No lookahead.** Every indicator is a causal, bar-by-bar computation.
  Pivots (5-left/5-right) are only exposed 5 bars after they form —
  `strategy/structure.py`'s `_confirmed_pivots` shifts them forward by
  `right` bars, and `tests/smoke_test.py` has a direct unit check for this.
  Signals are evaluated on a fully-closed bar and filled at the *next*
  bar's open, never the signal bar's own close.
  The daily HTF filter uses only the last **completed** daily bar, never
  the still-forming session.
- **Walk-forward, not curve-fit.** `--optimize` only ever touches the first
  70% of the data; the grid search never sees the final 30%. Reported
  out-of-sample numbers come from parameters chosen without looking at that
  data.
- **Overfit detection is automatic**, not something you have to eyeball:
  `GridResult.overfit_flag` in `backtest/optimize.py` flags any parameter
  set whose out-of-sample expectancy goes negative or drops below half its
  in-sample value.
- **Realistic costs and fills.** 0.05%/side commission for stocks, 0.10%
  for crypto, plus 1 tick of slippage applied against the trader on *every*
  fill (entry, stop, and each partial target) — not just entries. Bars that
  gap through a level fill at the worse of (open, level), never at a price
  better than what the market actually offered.
- **No cherry-picked windows.** `--all` runs the full fixed ticker list
  from the brief; there's no mechanism in this codebase to select "the good
  ticker" or "the good period" before reporting.

## Config / tuning

Every weight and threshold lives in `config.py` (`StrategyConfig` and its
sub-dataclasses) — nothing is hardcoded inline in the strategy modules.
Change a value there (or pass an alternate `StrategyConfig` into
`build_features`/`simulate`/`run_walk_forward`) to test variants.

## Known limitations (see `results/report.md` for the full write-up)

1. The `R/R >= min_rr` entry gate is measured against a fixed target
   R-multiple (2.5R), not the trade's actual structure-derived reward, so
   it doesn't discriminate between setups — see `strategy/risk.py`.
2. Several scoring components (EMA stack, EMA200, VWAP, HTF bias) are
   correlated trend proxies that can jointly hit 40/100 points just from
   "price is trending," inflating scores in trending regimes without truly
   independent confirmation.
3. No drawdown/loss-streak circuit breaker — the system will keep taking
   1%-risk trades through an extended losing streak with no built-in pause.

Full detail, plus the honest win-rate/expectancy verdict from an actual
run, is in `results/report.md`.
