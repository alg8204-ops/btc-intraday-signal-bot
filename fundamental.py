import json, urllib.request
from dataclasses import dataclass
from datetime import datetime

_cache={"data":None,"at":None}
CACHE_SECONDS=3600

@dataclass
class FundamentalSnapshot:
    funding_rate: float
    open_interest: float
    funding_bias: str
    fear_greed_value: int|None
    fear_greed_classification: str|None

def fetch_fear_greed_index():
    now=datetime.utcnow()
    if _cache["data"] and _cache["at"] and (now-_cache["at"]).total_seconds()<CACHE_SECONDS:
        return _cache["data"]
    try:
        req=urllib.request.Request(
            "https://api.alternative.me/fng/?limit=1",
            headers={"User-Agent":"btc-signal-bot/2.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            item=json.loads(r.read())["data"][0]
        data={"value":int(item["value"]),"classification":item["value_classification"]}
        _cache.update(data=data, at=now)
        return data
    except Exception:
        return _cache["data"]

def build_fundamental_snapshot(cfg, funding_rate, open_interest):
    if funding_rate >= cfg.funding_rate_extreme:
        bias="long_crowded"
    elif funding_rate <= -cfg.funding_rate_extreme:
        bias="short_crowded"
    else:
        bias="neutral"
    fg=fetch_fear_greed_index()
    return FundamentalSnapshot(
        funding_rate, open_interest, bias,
        fg["value"] if fg else None,
        fg["classification"] if fg else None
    )
