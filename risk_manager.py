from dataclasses import dataclass
from datetime import date

@dataclass
class RiskManager:
    cfg: object
    def position_size(self, entry, stop):
        risk_amount=self.cfg.capital_total*self.cfg.risk_per_trade_pct/100
        distance=abs(entry-stop)
        if distance<=0: return 0.0
        size=risk_amount/distance
        max_notional=self.cfg.capital_total*self.cfg.max_leverage
        return min(size,max_notional/entry)

    def risk_reward_ok(self, entry, stop, target):
        risk=abs(entry-stop)
        return risk>0 and abs(target-entry)/risk >= self.cfg.reward_risk*0.999
