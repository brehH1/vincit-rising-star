from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from coingecko import fetch_range
from analysis import group, bearish, max_volume, best_trade

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/analyze")
def analyze(start: date, end: date, coin: str = "bitcoin", currency: str = "eur"):
    pts = fetch_range(start, end, coin, currency)
    c = group(pts)
    return {
        "candles": c,
        "bearish": bearish(c),
        "max_volume": max_volume(c),
        "best_trade": best_trade(c)
    }
