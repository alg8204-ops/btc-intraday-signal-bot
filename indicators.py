import pandas as pd
import numpy as np

def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return (100 - 100/(1+rs)).fillna(50)

def macd(series, fast=12, slow=26, signal=9):
    fast_e = ema(series, fast)
    slow_e = ema(series, slow)
    line = fast_e - slow_e
    sig = ema(line, signal)
    return line, sig, line-sig

def atr(df, period=14):
    prev_close = df["close"].shift(1)
    tr = pd.concat([
        df["high"]-df["low"],
        (df["high"]-prev_close).abs(),
        (df["low"]-prev_close).abs()
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1/period, min_periods=period, adjust=False).mean()

def add_all_indicators(df, cfg):
    df = df.copy()
    df["ema_fast"] = ema(df["close"], cfg.ema_fast)
    df["ema_slow"] = ema(df["close"], cfg.ema_slow)
    df["ema_trend"] = ema(df["close"], cfg.ema_trend)
    df["rsi"] = rsi(df["close"], cfg.rsi_period)
    df["macd"], df["macd_signal"], df["macd_hist"] = macd(
        df["close"], cfg.macd_fast, cfg.macd_slow, cfg.macd_signal
    )
    df["atr"] = atr(df, cfg.atr_period)
    df["volume_sma"] = df["volume"].rolling(cfg.volume_period).mean()
    df["volume_ratio"] = df["volume"] / df["volume_sma"].replace(0, np.nan)
    return df
