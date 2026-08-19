import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone

class DataFeed:
    def __init__(self, cfg):
        self.cfg = cfg
        self._exchange = None
        if cfg.data_mode == "live":
            import ccxt
            self._exchange = getattr(ccxt, cfg.exchange_id)({
                "enableRateLimit": True,
                "timeout": 15000,
            })
            self._exchange.load_markets()

    def fetch_ohlcv(self, timeframe, limit=300):
        if self.cfg.data_mode == "mock":
            return self._mock_ohlcv(limit, timeframe)
        ohlcv = self._exchange.fetch_ohlcv(self.cfg.symbol, timeframe=timeframe, limit=limit)
        if not ohlcv:
            raise RuntimeError("El exchange no devolvio velas.")
        return pd.DataFrame(
            ohlcv, columns=["timestamp","open","high","low","close","volume"]
        ).assign(timestamp=lambda x: pd.to_datetime(x["timestamp"], unit="ms", utc=True))

    def fetch_funding_rate(self):
        if self.cfg.data_mode == "mock":
            return 0.00005
        try:
            fr = self._exchange.fetch_funding_rate(self.cfg.symbol)
            return float(fr.get("fundingRate") or 0.0)
        except Exception:
            return 0.0

    def fetch_open_interest(self):
        if self.cfg.data_mode == "mock":
            return 1_000_000.0
        try:
            oi = self._exchange.fetch_open_interest(self.cfg.symbol)
            return float(oi.get("openInterestAmount") or oi.get("openInterestValue") or 0.0)
        except Exception:
            return 0.0

    @staticmethod
    def _mock_ohlcv(limit, timeframe):
        # Deterministic synthetic data for repeatable tests.
        mins = {"15m":15, "1h":60, "4h":240}.get(timeframe, 15)
        rng = np.random.default_rng(42 + mins)
        now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
        prices=[60000.0]
        for _ in range(limit-1):
            drift = 0.00008 if _ > limit*0.45 else 0.00002
            prices.append(prices[-1]*(1+rng.normal(drift,0.0015)))
        rows=[]
        for i,c in enumerate(prices):
            o=c*(1+rng.normal(0,0.0003))
            h=max(o,c)*(1+abs(rng.normal(0,0.0005)))
            l=min(o,c)*(1-abs(rng.normal(0,0.0005)))
            v=500*(1+rng.normal(0,0.15))
            rows.append([now-timedelta(minutes=mins*(limit-i)),o,h,l,c,max(v,1)])
        return pd.DataFrame(rows, columns=["timestamp","open","high","low","close","volume"])
