import os, subprocess, sys
os.environ["DATA_MODE"]="mock"
os.environ["EXECUTION_MODE"]="paper"
from config import Config
from data_feed import DataFeed
from indicators import add_all_indicators
from signals import generate_signal
from fundamental import build_fundamental_snapshot
cfg=Config()
feed=DataFeed(cfg)
e=add_all_indicators(feed.fetch_ohlcv("15m",300),cfg)
t=add_all_indicators(feed.fetch_ohlcv("4h",300),cfg)
f=build_fundamental_snapshot(cfg,feed.fetch_funding_rate(),feed.fetch_open_interest())
s=generate_signal(e,t,f,cfg)
assert s.action in {"long","short","none"}
assert 0 <= s.score <= cfg.max_score
if s.action!="none":
    assert s.entry and s.stop and s.target
print("OK - self_test passed")
print(f"action={s.action} score={s.score} entry={s.entry} stop={s.stop} target={s.target}")
