from dataclasses import dataclass, field

@dataclass
class TradeSignal:
    action: str
    score: int
    reasons: list[str] = field(default_factory=list)
    entry: float|None = None
    stop: float|None = None
    target: float|None = None
    candle_time: str|None = None

def _closed(df):
    # The last exchange candle can still be forming. Never use it.
    return df.iloc[:-1].copy() if len(df) > 3 else df.copy()

def generate_signal(df_entry, df_trend, fundamentals, cfg):
    e=_closed(df_entry)
    t=_closed(df_trend)
    if len(e)<max(cfg.ema_slow,cfg.atr_period,cfg.volume_period)+5 or len(t)<cfg.ema_trend+5:
        return TradeSignal("none",0,["Datos insuficientes"])

    last, prev=e.iloc[-1], e.iloc[-2]
    tl=t.iloc[-1]
    long_score=short_score=0
    lr=[]; sr=[]

    # 1) 4H regime
    trend_long = tl.close > tl.ema_trend and tl.ema_fast > tl.ema_trend
    trend_short = tl.close < tl.ema_trend and tl.ema_fast < tl.ema_trend
    if trend_long: long_score+=2; lr.append("4H: precio y EMA20 sobre EMA200")
    if trend_short: short_score+=2; sr.append("4H: precio y EMA20 bajo EMA200")

    # 2) 15m pullback near EMA20
    dist=abs(last.close-last.ema_fast)/last.close
    near=dist <= cfg.pullback_max_pct or (last.low <= last.ema_fast <= last.high)
    if near and last.close >= last.ema_fast: long_score+=1; lr.append("15m: pullback/retest de EMA20")
    if near and last.close <= last.ema_fast: short_score+=1; sr.append("15m: pullback/retest de EMA20")

    # 3) RSI trigger: actual cross, not just being inside an extreme zone
    if prev.rsi <= cfg.rsi_long_trigger < last.rsi:
        long_score+=1; lr.append(f"RSI cruza {cfg.rsi_long_trigger:.0f} al alza")
    if prev.rsi >= cfg.rsi_short_trigger > last.rsi:
        short_score+=1; sr.append(f"RSI cruza {cfg.rsi_short_trigger:.0f} a la baja")

    # 4) MACD histogram direction
    if prev.macd_hist <= 0 < last.macd_hist:
        long_score+=1; lr.append("MACD histograma cruza positivo")
    if prev.macd_hist >= 0 > last.macd_hist:
        short_score+=1; sr.append("MACD histograma cruza negativo")

    # 5) Volume confirmation
    vr=float(last.volume_ratio) if last.volume_ratio == last.volume_ratio else 0
    if vr >= cfg.volume_min_ratio:
        long_score+=1; short_score+=1
        lr.append(f"Volumen OK ({vr:.2f}x)")
        sr.append(f"Volumen OK ({vr:.2f}x)")

    # 6) Funding/sentiment are filters, not arbitrary score points
    long_block = fundamentals.funding_rate >= cfg.funding_rate_block
    short_block = fundamentals.funding_rate <= -cfg.funding_rate_block
    if fundamentals.fear_greed_value is not None:
        long_block |= fundamentals.fear_greed_value >= cfg.fear_greed_block_long
        short_block |= fundamentals.fear_greed_value <= cfg.fear_greed_block_short

    candidates=[]
    if trend_long and long_score >= cfg.min_score and not long_block:
        candidates.append(("long",long_score,lr))
    if trend_short and short_score >= cfg.min_score and not short_block:
        candidates.append(("short",short_score,sr))
    if not candidates:
        return TradeSignal("none", max(long_score,short_score), lr+sr)

    action,score,reasons=max(candidates,key=lambda x:x[1])
    entry=float(last.close)
    atr=float(last.atr)
    if not (atr>0):
        return TradeSignal("none",score,reasons+["ATR inválido"])
    risk=cfg.stop_atr_mult*atr
    if action=="long":
        stop=entry-risk; target=entry+cfg.reward_risk*risk
    else:
        stop=entry+risk; target=entry-cfg.reward_risk*risk
    candle=str(last.timestamp)
    return TradeSignal(action,score,reasons,entry,stop,target,candle)
