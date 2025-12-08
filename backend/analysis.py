def longest_bearish(candles):
    if not candles:
        return {"length": 0, "start": None, "end": None}

    best_len = 0
    best_start = None
    best_end = None

    current_len = 0
    current_start = None
    prev_price = candles[0]["price"]
    prev_date = candles[0]["date"]

    for c in candles[1:]:
        price = c["price"]
        date = c["date"]

        if price < prev_price:
            if current_len == 0:
                current_start = prev_date
            current_len += 1
            if current_len > best_len:
                best_len = current_len
                best_start = current_start
                best_end = date
        else:
            current_len = 0
            current_start = None

        prev_price = price
        prev_date = date

    return {
        "length": best_len,
        "start": best_start,
        "end": best_end,
    }


def highest_volume(candles):
    if not candles:
        return {"date": None, "volume": 0.0}
    m = max(candles, key=lambda c: c["volume"])
    return {"date": m["date"], "volume": float(m["volume"])}


def best_trade(candles):
    if not candles:
        return {"buy": None, "sell": None, "profit": 0.0}

    min_price = candles[0]["price"]
    min_date = candles[0]["date"]
    best_profit = 0.0
    best_buy = None
    best_sell = None

    for c in candles[1:]:
        price = c["price"]
        date = c["date"]

        profit = price - min_price
        if profit > best_profit:
            best_profit = profit
            best_buy = min_date
            best_sell = date

        if price < min_price:
            min_price = price
            min_date = date

    if best_profit <= 0:
        return {"buy": None, "sell": None, "profit": 0.0}

    return {
        "buy": best_buy,
        "sell": best_sell,
        "profit": float(round(best_profit, 2)),
    }
