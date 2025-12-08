import os
from datetime import datetime, timezone, timedelta

import requests

BASE_URL = "https://api.coingecko.com/api/v3"
API_KEY = os.getenv("CG_API_KEY")


class CoinGeckoError(Exception):
    pass


def _to_unix(date_str: str) -> int:
    dt = datetime.fromisoformat(date_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def fetch_range(start_date: str, end_date: str, coin: str, currency: str):
    if not API_KEY:
        raise CoinGeckoError("CG_API_KEY environment variable is not set")

    start_ts = _to_unix(start_date)
    end_ts = _to_unix(end_date) + 3600

    url = f"{BASE_URL}/coins/{coin}/market_chart/range"

    params = {
        "vs_currency": currency,
        "from": start_ts,
        "to": end_ts,
    }

    headers = {
        "x-cg-demo-api-key": API_KEY
    }

    r = requests.get(url, params=params, headers=headers, timeout=15)

    if r.status_code == 401:
        raise CoinGeckoError("CoinGecko returned 401 Unauthorized. Check API key and plan.")
    if r.status_code == 429:
        raise CoinGeckoError("CoinGecko rate limit exceeded. Try a smaller date range or later.")

    r.raise_for_status()
    data = r.json()

    prices = data.get("prices") or []
    volumes = data.get("total_volumes") or []

    candles = []
    for i, p in enumerate(prices):
        ts_ms, price = p
        vol = 0.0
        if i < len(volumes) and len(volumes[i]) > 1:
            vol = float(volumes[i][1])
        dt = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).date().isoformat()
        candles.append(
            {
                "date": dt,
                "price": float(price),
                "volume": vol,
            }
        )

    return candles
