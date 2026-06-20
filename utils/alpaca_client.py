import requests
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL

HEADERS = {
    "APCA-API-KEY-ID": ALPACA_API_KEY,
    "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY,
}
DATA_URL = "https://data.alpaca.markets"


def _get(path, base=None):
    url = f"{base or ALPACA_BASE_URL}{path}"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()


def _post(path, body):
    url = f"{ALPACA_BASE_URL}{path}"
    r = requests.post(url, json=body, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()


def _delete(path):
    url = f"{ALPACA_BASE_URL}{path}"
    r = requests.delete(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()


def get_account():
    return _get("/v2/account")


def get_positions():
    return _get("/v2/positions")


def get_position(symbol):
    try:
        return _get(f"/v2/positions/{symbol}")
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return None
        raise


def get_clock():
    return _get("/v2/clock")


def is_market_open():
    return get_clock().get("is_open", False)


def place_limit_order(symbol, qty, side, limit_price):
    body = {
        "symbol": symbol,
        "qty": str(qty),
        "side": side,
        "type": "limit",
        "time_in_force": "day",
        "limit_price": str(round(limit_price, 2)),
    }
    return _post("/v2/orders", body)


def place_stop_limit_order(symbol, qty, side, stop_price, limit_price):
    body = {
        "symbol": symbol,
        "qty": str(qty),
        "side": side,
        "type": "stop_limit",
        "time_in_force": "gtc",
        "stop_price": str(round(stop_price, 2)),
        "limit_price": str(round(limit_price, 2)),
    }
    return _post("/v2/orders", body)


def close_position(symbol):
    return _delete(f"/v2/positions/{symbol}")


def get_latest_bar(symbol):
    data = _get(f"/v2/stocks/{symbol}/bars/latest", base=DATA_URL)
    return data.get("bar", {})


def get_bars(symbol, timeframe="1Day", limit=30):
    path = f"/v2/stocks/{symbol}/bars?timeframe={timeframe}&limit={limit}&adjustment=raw"
    data = _get(path, base=DATA_URL)
    return data.get("bars", [])


def get_snapshot(symbol):
    data = _get(f"/v2/stocks/{symbol}/snapshot", base=DATA_URL)
    return data
