import datetime as dt

def group(points):
    days = {}
    for p in points:
        t = dt.datetime.utcfromtimestamp(p["timestamp"] / 1000).date()
        days.setdefault(t, []).append(p)
    out = []
    for day in sorted(days.keys()):
        ps = sorted(days[day], key=lambda x: x["timestamp"])
        out.append({
            "date": day.isoformat(),
            "price": ps[0]["price"],
            "volume": ps[-1]["volume"]
        })
    return out

def bearish(candles):
    if not candles:
        return {"length": 0, "start": None, "end": None}
    ml = 0
    ms = 0
    cl = 0
    cs = 0
    for i in range(1, len(candles)):
        if candles[i]["price"] < candles[i-1]["price"]:
            if cl == 0:
                cs = i-1
            cl += 1
        else:
            if cl > ml:
                ml = cl
                ms = cs
            cl = 0
    if cl > ml:
        ml = cl
        ms = cs
    if ml == 0:
        return {"length": 0, "start": None, "end": None}
    return {
        "length": ml,
        "start": candles[ms]["date"],
        "end": candles[ms+ml]["date"]
    }

def max_volume(candles):
    if not candles:
        return {"date": None, "volume": 0}
    m = max(candles, key=lambda c: c["volume"])
    return {"date": m["date"], "volume": m["volume"]}

def best_trade(candles):
    if len(candles) < 2:
        return {"buy": None, "sell": None, "profit": 0}
    mp = candles[0]["price"]
    md = candles[0]["date"]
    bp = 0
    bd = None
    sd = None
    for c in candles[1:]:
        pr = c["price"] - mp
        if pr > bp:
            bp = pr
            bd = md
            sd = c["date"]
        if c["price"] < mp:
            mp = c["price"]
            md = c["date"]
    if bp <= 0:
        return {"buy": None, "sell": None, "profit": 0}
    return {"buy": bd, "sell": sd, "profit": bp}
