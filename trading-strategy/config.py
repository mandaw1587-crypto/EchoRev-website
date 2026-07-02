"""
Central configuration for the A+ Setup Analyzer Python port.

Every threshold and weight here is taken directly from the strategy brief /
a_plus_setup_analyzer.pine reference doc. Values marked [ASSUMPTION] were not
fully specified in the source and were chosen deliberately — see the .pine
reference file for the reasoning. Change them here, not scattered through the
code, if you want to test alternatives.
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class IndicatorConfig:
    ema_fast: int = 9
    ema_mid: int = 20
    ema_slow: int = 50
    ema_trend: int = 200
    rsi_len: int = 14
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    atr_len: int = 14
    vol_sma_len: int = 20


@dataclass(frozen=True)
class StructureConfig:
    pivot_left: int = 5
    pivot_right: int = 5           # pivot confirmed pivot_right bars after it forms
    fvg_valid_bars: int = 10       # FVG usable for scoring for this many bars after formation


@dataclass(frozen=True)
class ScoreWeights:
    structure: float = 15
    ema_stack: float = 12
    ema_stack_partial: float = 6     # [ASSUMPTION] partial credit, 2-of-3 pairwise stack
    ema200: float = 10
    vwap: float = 8
    rsi_band: float = 8
    macd: float = 10
    volume_full: float = 10
    volume_partial: float = 5        # [ASSUMPTION] half credit if vol > 1.0x avg but < 1.3x
    near_structure: float = 10
    fvg: float = 7
    htf: float = 10
    fake_breakout_penalty: float = -15


@dataclass(frozen=True)
class ScoreThresholds:
    rsi_long_band: tuple = (45, 70)   # [ASSUMPTION]
    rsi_short_band: tuple = (30, 55)  # [ASSUMPTION]
    near_structure_atr_mult: float = 1.0  # [ASSUMPTION]
    volume_full_mult: float = 1.3
    volume_partial_mult: float = 1.0


@dataclass(frozen=True)
class EntryConfig:
    min_score: float = 85.0
    min_rr: float = 2.0
    min_volume_mult: float = 1.3
    cooldown_bars: int = 10


@dataclass(frozen=True)
class RiskConfig:
    atr_stop_mult: float = 1.5
    pivot_stop_buffer_atr: float = 0.25
    tp1_r: float = 1.5
    tp2_r: float = 2.5
    tp3_r: float = 4.0
    tp1_close_pct: float = 0.50
    tp2_close_pct: float = 0.25       # [ASSUMPTION] of ORIGINAL size; remainder (0.25) closes at TP3
    risk_pct_of_equity: float = 0.01


@dataclass(frozen=True)
class CostConfig:
    stock_commission_per_side: float = 0.0005   # 0.05%
    crypto_commission_per_side: float = 0.0010  # 0.10%
    slippage_ticks: int = 1


@dataclass(frozen=True)
class WalkForwardConfig:
    in_sample_frac: float = 0.70


@dataclass(frozen=True)
class OptimizationGrid:
    score_thresholds: tuple = (75, 80, 85, 90, 95)
    atr_stop_mults: tuple = (1.0, 1.5, 2.0, 2.5, 3.0)
    min_rrs: tuple = (1.5, 2.0, 2.5, 3.0)
    min_trades_for_consideration: int = 20  # ignore parameter sets with too few IS trades


@dataclass(frozen=True)
class StrategyConfig:
    indicators: IndicatorConfig = field(default_factory=IndicatorConfig)
    structure: StructureConfig = field(default_factory=StructureConfig)
    weights: ScoreWeights = field(default_factory=ScoreWeights)
    thresholds: ScoreThresholds = field(default_factory=ScoreThresholds)
    entry: EntryConfig = field(default_factory=EntryConfig)
    risk: RiskConfig = field(default_factory=RiskConfig)
    cost: CostConfig = field(default_factory=CostConfig)
    walk_forward: WalkForwardConfig = field(default_factory=WalkForwardConfig)
    optimization: OptimizationGrid = field(default_factory=OptimizationGrid)


DEFAULT_CONFIG = StrategyConfig()

# Tick sizes used for 1-tick slippage modeling. [ASSUMPTION] approximate
# typical tick/price-increment sizes; override per-symbol if you need exact
# venue tick sizes.
TICK_SIZES = {
    "SPY": 0.01,
    "QQQ": 0.01,
    "AAPL": 0.01,
    "TSLA": 0.01,
    "BTC/USDT": 0.10,
    "ETH/USDT": 0.01,
}

COST_TYPE_BY_ASSET = {
    "SPY": "stock", "QQQ": "stock", "AAPL": "stock", "TSLA": "stock",
    "BTC/USDT": "crypto", "ETH/USDT": "crypto",
}
