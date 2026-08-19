import csv, os
from datetime import datetime, timezone
PATH="trade_journal.csv"
FIELDS=["timestamp","candle_time","action","score","entry","stop","target","size","reasons"]

def log_signal(signal,size,path=PATH):
    row={
        "timestamp":datetime.now(timezone.utc).isoformat(),
        "candle_time":signal.candle_time,"action":signal.action,"score":signal.score,
        "entry":signal.entry,"stop":signal.stop,"target":signal.target,"size":size,
        "reasons":" | ".join(signal.reasons)
    }
    exists=os.path.isfile(path)
    with open(path,"a",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS)
        if not exists:w.writeheader()
        w.writerow(row)
