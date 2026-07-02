# A+ Setup Analyzer — Backtest Report

**Status: pipeline validated, real-market numbers not yet generated.**

This report was written from inside a sandboxed environment whose network
policy blocks Yahoo Finance and Binance (the two data sources this project
needs — see "Why there are no real numbers here yet" below). Everything in
`strategy/`, `backtest/`, `data/`, and `run_backtest.py` is complete,
runs, and has been validated end-to-end on synthetic data (see the smoke
test evidence below). **You need to run it once on your own machine to get
the real win rate / expectancy** — that's the whole point of this project,
and it's a five-minute step (`pip install -r requirements.txt && python
run_backtest.py --all --optimize`).

## Why there are no real numbers here yet

I tested outbound access from the build environment before writing any
code: `curl` to `query1.finance.yahoo.com` and `api.binance.com` both got a
`403` at the egress proxy — blocked by the sandbox's organization network
policy, not a bug in this code. I confirmed this with you before building
and you asked me to build the complete, real project and validate the
*pipeline* with synthetic data rather than fabricate results. That's what
follows.

## What "validated" means here — the smoke test

`tests/smoke_test.py` generates a synthetic random-walk OHLCV series (not
real market data — has no real edge to find) and runs it through the exact
same code path `run_backtest.py` uses: indicators → structure → confluence
scoring → signal gate → the bar-by-bar backtest engine → the 70/30
walk-forward split → a reduced grid search. It also directly unit-tests
that a pivot is never visible before its 5-bar confirmation lag (the
easiest place for a lookahead bug to hide). Output from an actual run:

```
======================================================================
SMOKE TEST -- SYNTHETIC DATA ONLY. These numbers are NOT a real
backtest result and must never be reported as strategy performance.
======================================================================

[1/5] Checking pivot confirmation has no lookahead...
  [ok] pivot confirmation lag is exactly 5 bars (no lookahead)

[2/5] Generating synthetic OHLCV and building features...
  [ok] 4000 bars featured, scores bounded in [0,100]
  bars with score_long >= 85: 36
  bars with score_short >= 85: 3

[3/5] Running the backtest engine directly...
  [ok] 7 trades, final equity $100,015.35
    long  entry=81.04 r_mult=-1.02 bars_held=49 exit_reason=stop
    long  entry=81.30 r_mult=+1.14 bars_held=69 exit_reason=stop
    long  entry=88.02 r_mult=-1.04 bars_held=24 exit_reason=stop

[4/5] Running walk-forward split (70/30)...
  [ok] in-sample trades=3, out-of-sample trades=4
  in-sample expectancy=-0.307R, out-of-sample expectancy=+0.398R

[5/5] Running a tiny grid search (reduced grid for speed)...
  [ok] 8 grid combos evaluated, 3 confirmed on out-of-sample
    score>=90 atr=1.5 rr=1.5 IS_exp=-0.307R OOS_exp=+0.398R overfit=False
    score>=90 atr=1.5 rr=2.5 IS_exp=-0.307R OOS_exp=+0.398R overfit=False
    score>=90 atr=2.5 rr=1.5 IS_exp=-0.307R OOS_exp=+0.404R overfit=False

======================================================================
SMOKE TEST PASSED. Pipeline runs end-to-end without crashing.
======================================================================
```

Note the identical results for `rr=1.5` and `rr=2.5` in step 5 — that's not
a bug, it's the R/R gate limitation described below manifesting immediately
even on random data (both thresholds sit below the fixed 2.5R the gate
actually checks against, so they behave identically).

Do not mistake any number above for a strategy edge. Random walks have no
edge to find; a real run will show real, possibly unflattering, results.

## How to generate the real report

```bash
cd trading-strategy
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python tests/smoke_test.py        # optional re-confirmation
python run_backtest.py --all --optimize
```

This overwrites this file with per-ticker in-sample/out-of-sample tables
(win rate, profit factor, expectancy in R, max drawdown, Sharpe, trade
count, average duration), equity curve PNGs in `results/`, and grid-search
tables with the automatic overfit flag. Re-run
`python run_backtest.py --ticker X --tf Y` any time to check one
market/timeframe on its own.

**When you have real output, read it literally.** If it says 45% win rate
and +0.3R expectancy, that IS the answer — a 45% win rate with big enough
average winners is a real, profitable edge, and the code's job (and mine)
is to report that number accurately, not to make it look like 60%.

## Recommended parameter set

The values in `config.py` (`EntryConfig`, `RiskConfig`) — score threshold
85, ATR stop multiplier 1.5, min R/R 2.0 — are the brief's specified
defaults and the sensible starting point for `--optimize`'s grid search
(which sweeps score 75–95, ATR multiplier 1.0–3.0, min R/R 1.5–3.0 around
them). **I'm not publishing a "recommended" deviation from those defaults
here because I have no real data to justify one** — that would be exactly
the kind of unearned, flattering number this project explicitly asked me
not to produce. Once you run `--optimize`, the top-of-grid in-sample
candidates and their out-of-sample confirmation will be in the per-ticker
sections this file gets rewritten with; treat any candidate the grid search
marks `overfit=True` as a parameter set that only works in-sample, i.e. not
usable.

## Top 3 weaknesses found in the strategy (from building and testing the logic)

### 1. The R/R entry filter doesn't actually discriminate between setups

Targets are fixed R-multiples of the stop distance (TP1=1.5R, TP2=2.5R,
TP3=4R) rather than derived from real structure (next resistance/support,
a measured move, a liquidity pool). That means "reward" in the `R/R >=
min_rr` check is *always exactly 2.5* (see `strategy/risk.py:risk_reward`)
regardless of the specific setup — it's a function of `config.py`, not of
the market. The gate collapses to a step function of `min_rr` alone: every
setup passes when `min_rr <= 2.5`, and nothing passes when `min_rr > 2.5`.
The grid search will show this directly (`rr=1.5` and `rr=2.0` and `rr=2.5`
producing identical trade counts). **Fix:** derive at least one target from
actual structure (e.g. the next opposing pivot beyond entry) and gate R/R
against that measured distance, so a setup with a resistance level 1.2R
away actually gets rejected instead of waved through.

### 2. Several scoring components are correlated trend proxies, inflating scores in trending regimes

EMA stack (12pts), EMA200 filter (10pts), VWAP (8pts), and HTF bias (10pts)
— 40 of the 100 possible points — are all measuring approximately the same
underlying fact ("is price in an uptrend/downtrend right now"). In a strong
trend they tend to move together, so a setup can clear most of the way to
the 85-point threshold from trend alignment alone, without independent
confirmation from structure, FVGs, or volume. This likely concentrates
entries in trending stretches (fine) but with less true diversification of
evidence than "11 independent 0-15pt signals" would suggest, and probably
means the strategy behaves more like "buy strength, sell weakness" with
extra steps than the confluence framing implies. **Fix:** cap the combined
contribution of directly-correlated trend components, or require a minimum
score contribution from the more independent components (structure, FVG,
near-structure, volume) separately from the trend-stack ones.

### 3. No drawdown or loss-streak circuit breaker

Position sizing is 1% risk per trade, which is sound, but the system has
no mechanism to pause after a string of losses. The 10-bar cooldown only
throttles signal frequency, not risk exposure through a bad regime. A
45%-ish win-rate system (a perfectly viable outcome per the honesty rules
above) will have real losing streaks — 10+ consecutive -1R trades is not
an edge case over a 2-year backtest — and as specified, the system just
keeps firing at full size through one. **Fix:** add an equity-drawdown or
consecutive-loss circuit breaker (e.g. pause new entries after N
consecutive losses or X% equity drawdown from peak, resume after a cooldown
or explicit reassessment), and/or scale risk-per-trade down during a
drawdown.

## Data availability caveat (operational, not a strategy flaw)

Yahoo Finance's free intraday API caps 15-minute stock bars at roughly the
trailing 60 days — nowhere near the requested 2 years. 1-hour stock bars
get the full ~730 days. `data/fetchers.py` reports the real fetched date
range every run rather than silently pretending otherwise. Crypto via
`ccxt`/Binance has no such cap. If 2 years of 15-minute SPY/QQQ/AAPL/TSLA
data matters for your analysis, you'll need a paid data vendor behind
`fetch_stock_data()`'s signature — the rest of the pipeline is agnostic to
where the OHLCV came from.
