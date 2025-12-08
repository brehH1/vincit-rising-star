from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from coingecko import fetch_range, CoinGeckoError
from analysis import longest_bearish, highest_volume, best_trade

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/analyze")
def analyze(
    start: str = Query(..., description="Start date YYYY-MM-DD"),
    end: str = Query(..., description="End date YYYY-MM-DD"),
    coin: str = "bitcoin",
    currency: str = "eur",
):
    try:
        candles = fetch_range(start, end, coin, currency)
    except CoinGeckoError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to fetch data from CoinGecko.")

    if not candles:
        raise HTTPException(status_code=422, detail="No price data for given date range.")

    bearish = longest_bearish(candles)
    max_vol = highest_volume(candles)
    trade = best_trade(candles)

    return {
        "candles": candles,
        "bearish": bearish,
        "max_volume": max_vol,
        "best_trade": trade,
    }
