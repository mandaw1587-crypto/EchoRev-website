"""Commission + slippage modeling."""
from __future__ import annotations

from config import CostConfig


def commission_rate(cost_type: str, cfg: CostConfig) -> float:
    return cfg.crypto_commission_per_side if cost_type == "crypto" else cfg.stock_commission_per_side


def commission_cost(notional: float, cost_type: str, cfg: CostConfig) -> float:
    return abs(notional) * commission_rate(cost_type, cfg)


def apply_slippage(price: float, adverse_direction: int, tick_size: float, ticks: int) -> float:
    """
    adverse_direction: +1 means slippage pushes the fill price UP (bad for a
    buy fill), -1 means it pushes the fill price DOWN (bad for a sell fill).
    Always moves the fill against the trader by `ticks` ticks.
    """
    return price + adverse_direction * ticks * tick_size
