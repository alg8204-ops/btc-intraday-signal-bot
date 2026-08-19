import os
from dataclasses import dataclass, field

def env_bool(name: str, default: bool=False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in {"1","true","yes","on"}

@dataclass
class Config:
    exchange_id: str = os.getenv("EXCHANGE_ID", "binance")
    symbol: str = os.getenv("SYMBOL", "BTC/USDT")
    timeframe_entry: str = os.getenv("TIMEFRAME_ENTRY", "15m")
    timeframe_trend: str = os.getenv("TIMEFRAME_TREND", "4h")

    # SAFE BY DESIGN: this version is signal/paper only. No live order code.
    data_mode: str = os.getenv("DATA_MODE", "live")
    execution_mode: str = os.getenv("EXECUTION_MODE", "paper")

    # Technical model
    ema_fast: int = 20
    ema_slow: int = 50
    ema_trend: int = 200
    rsi_period: int = 14
    rsi_long_trigger: float = 35.0
    rsi_short_trigger: float = 65.0
    atr_period: int = 14
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    volume_period: int = 20
    volume_min_ratio: float = 0.90
    pullback_max_pct: float = 0.006
    min_score: int = 6
    max_score: int = 6

    # Risk model (paper sizing only)
    capital_total: float = float(os.getenv("CAPITAL", "1000"))
    risk_per_trade_pct: float = 0.50
    max_daily_loss_pct: float = 2.0
    stop_atr_mult: float = 1.5
    reward_risk: float = 2.0
    max_leverage: float = 1.5

    # Funding / sentiment filters
    funding_rate_extreme: float = 0.0005
    funding_rate_block: float = 0.0010
    fear_greed_block_long: int = 90
    fear_greed_block_short: int = 10

    # Runtime
    loop_interval_seconds: int = 900
    telegram_bot_token: str = field(default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN", ""))
    telegram_chat_id: str = field(default_factory=lambda: os.getenv("TELEGRAM_CHAT_ID", ""))
    send_only_signals: bool = field(default_factory=lambda: env_bool("SEND_ONLY_SIGNALS", True))
