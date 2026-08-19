import sys, traceback
from config import Config
from data_feed import DataFeed
from indicators import add_all_indicators
from fundamental import build_fundamental_snapshot
from signals import generate_signal
from risk_manager import RiskManager
from journal import log_signal
from alerts import send_telegram_alert

def run_once(cfg=None, feed=None):
    cfg=cfg or Config()
    feed=feed or DataFeed(cfg)
    e=add_all_indicators(feed.fetch_ohlcv(cfg.timeframe_entry,300),cfg)
    t=add_all_indicators(feed.fetch_ohlcv(cfg.timeframe_trend,300),cfg)
    f=build_fundamental_snapshot(cfg,feed.fetch_funding_rate(),feed.fetch_open_interest())
    s=generate_signal(e,t,f,cfg)
    rm=RiskManager(cfg)

    if s.action=="none":
        msg=f"BTC SIGNAL | NONE | score={s.score} | {', '.join(s.reasons[-3:])}"
        print(msg)
        return s,msg

    if not rm.risk_reward_ok(s.entry,s.stop,s.target):
        msg="BTC SIGNAL | DESCARTADA | R:R inválido"
        print(msg); return s,msg

    size=rm.position_size(s.entry,s.stop)
    msg=(f"BTC {s.action.upper()} | score={s.score}/{cfg.max_score}\n"
         f"Entry {s.entry:.2f} | SL {s.stop:.2f} | TP {s.target:.2f}\n"
         f"R:R 1:{cfg.reward_risk:.1f} | size {size:.6f} BTC\n"
         f"Vela {s.candle_time}\n" + "\n".join("• "+x for x in s.reasons))
    print(msg)
    log_signal(s,size)
    if not cfg.send_only_signals or s.action!="none":
        send_telegram_alert(cfg,msg)
    return s,msg

if __name__=="__main__":
    try:
        run_once()
    except Exception as exc:
        print("ERROR:",exc)
        traceback.print_exc()
        send_telegram_alert(Config(),f"BTC BOT ERROR: {exc}")
        sys.exit(1)
