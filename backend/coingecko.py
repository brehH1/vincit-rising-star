import datetime as dt
import requests

def fetch_range(start, end, coin_id, currency):
    s = dt.datetime.combine(start, dt.time(0, 0), tzinfo=dt.timezone.utc)
    e = dt.datetime.combine(end + dt.timedelta(days=1), dt.time(1, 0), tzinfo=dt.timezone.utc)
    url = "https://api.coingecko.com/api/v3/coins/" + coin_id + "/market_chart/range"
    r = requests.get(url, params={
        "vs_currency": currency,
        "from": int(s.timestamp()),
        "to": int(e.timestamp())
    })
    r.raise_for_status()
    d = r.json()
    prices = d.get("prices", [])
    vols = d.get("total_volumes", [])
    vd = {ts: v for ts, v in vols}
    out = []
    for ts, p in prices:
        out.append({
            "timestamp": ts,
            "price": p,
            "volume": vd.get(ts, 0.0)
        })
    return out
