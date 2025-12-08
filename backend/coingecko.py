import os
import requests

API_KEY = os.getenv("CG_API_KEY")

def fetch_range(start_ts, end_ts, coin, currency):
    url = (
        f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart/range"
        f"?vs_currency={currency}&from={start_ts}&to={end_ts}"
    )

    headers = {
        "x-cg-demo-api-key": API_KEY
    }

    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()

    prices = data.get("prices", [])
    volumes = data.get("total_volumes", [])

    return [
        {
            "date": p[0] // 1000,
            "price": p[1],
            "volume": volumes[i][1] if i < len(volumes) else 0
        }
        for i, p in enumerate(prices)
    ]
