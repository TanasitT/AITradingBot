"""US momentum executor: places the pre-open plan's orders and manages their stops.

Runs from main.py; enter() also runs from scripts/routine_entries.py for the pre-open
routine, so every entry goes through this code. The CLAUDE.md hard rules apply:
- Entries: buy stop-limit day orders at the plan's trigger and limit, at most
  min(regime cap, MAX_TRADES_PER_DAY) a day, and none once the day is down 2%.
- Size: 0.5% of equity at risk down to the plan's stop, capped at 5% of equity.
- Exits: a good-until-cancelled sell stop on every position. It starts at the
  plan's stop and is raised after each close to just under the lowest low of
  the last 10 sessions. It is never lowered.
"""
import glob
import json
import logging
import math
import os
import subprocess
import sys
from datetime import date

import requests

from utils import memory
from utils.alpaca_client import (
    get_account, get_positions, get_orders, get_clock, close_position,
    place_entry_stop_limit, place_stop_order, replace_order, cancel_order,
)
from config import (
    ALPACA_BASE_URL, MAX_POSITION_PCT, DAILY_LOSS_CAP_PCT, MAX_TRADES_PER_DAY,
    MOMENTUM_DIR, MOMENTUM_RISK_PCT, MOMENTUM_TRAIL_SESSIONS,
)

log = logging.getLogger(__name__)

PLANS_DIR = os.path.join(MOMENTUM_DIR, "plans")
SCREEN_SUMMARY = os.path.join(MOMENTUM_DIR, "results", "latest", "summary.json")
MAX_SCREEN_AGE_DAYS = 9  # the weekend screen runs every Saturday; older means a run was missed
ORDER_PREFIX = "mom-"  # client_order_id prefix; Alpaca rejects a repeated id, so a rerun cannot double an entry
STOP_TYPES = ("stop", "stop_limit", "trailing_stop")


def _journal(text):
    memory.append("reasoning.md", f"## {memory.now_et()} — US momentum executor\n{text}\n---")


def _trading_allowed():
    """Paper account always; a live account only once strategy.md says live_trading: true."""
    if "paper" in ALPACA_BASE_URL or memory.get_flag("strategy.md", "live_trading") == "true":
        return True
    log.error("[Momentum] Live Alpaca URL but live_trading is not true in strategy.md — not trading")
    return False


def _daily_pnl_pct(account):
    last = float(account["last_equity"])
    return (float(account["equity"]) - last) / last if last else 0.0


def _max_stop_pct():
    with open(os.path.join(MOMENTUM_DIR, "config", "risk.json"), encoding="utf-8") as f:
        return float(json.load(f)["max_stop_pct"])


def _load_plan(today):
    path = os.path.join(PLANS_DIR, f"{today}.json")
    if not os.path.exists(path):
        # The pre-open plan routine did not run in time, so build the plan here (without its news check).
        log.warning(f"[Momentum] No plan for {today} — running preopen_plan.py")
        result = subprocess.run(
            [sys.executable, os.path.join("scripts", "preopen_plan.py"), "--date", today],
            cwd=MOMENTUM_DIR, capture_output=True, text=True, timeout=900,
        )
        if result.returncode != 0:
            log.error(f"[Momentum] preopen_plan.py failed: {result.stderr[-500:]}")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _shares(equity, trigger, stop):
    risk_per_share = trigger - stop
    if risk_per_share <= 0:
        return 0
    return math.floor(min(equity * MOMENTUM_RISK_PCT / risk_per_share,
                          equity * MAX_POSITION_PCT / trigger))


def _initial_stop(symbol, avg_entry):
    """The stop from the newest plan that listed this ticker, else max_stop_pct below the entry."""
    today = memory.today_et()
    for path in sorted(glob.glob(os.path.join(PLANS_DIR, "*.json")), reverse=True):
        if os.path.basename(path)[:10] > today:
            continue
        try:
            with open(path, encoding="utf-8") as f:
                tickets = json.load(f).get("tickets", [])
        except (OSError, ValueError):
            continue
        for t in tickets:
            if t.get("ticker") == symbol:
                return float(t["stop"])
    return round(avg_entry * (1 - _max_stop_pct()), 2)


def _trail_level(symbol):
    """Just under the lowest low of the last MOMENTUM_TRAIL_SESSIONS sessions, in raw prices."""
    try:
        import yfinance as yf
        lows = yf.Ticker(symbol).history(period="1mo", interval="1d", auto_adjust=False)["Low"].dropna()
    except Exception as e:
        log.warning(f"[Momentum] No price history for {symbol}, stop not trailed: {e}")
        return None
    if len(lows) < MOMENTUM_TRAIL_SESSIONS:
        return None
    return round(float(lows.tail(MOMENTUM_TRAIL_SESSIONS).min()) * 0.999, 2)


def enter():
    """Before the open: place today's plan as breakout entry orders."""
    if not _trading_allowed():
        return
    today = memory.today_et()
    clock = get_clock()
    if not clock["is_open"] and clock["next_open"][:10] != today:
        log.info(f"[Momentum] {today} is not a trading day — no entries")
        return

    with open(SCREEN_SUMMARY, encoding="utf-8") as f:
        data_date = json.load(f)["data_date"]
    age = (date.fromisoformat(today) - date.fromisoformat(data_date)).days
    if age > MAX_SCREEN_AGE_DAYS:
        _journal(f"No entries: the weekend screen is {age} days old (data {data_date}). "
                 f"Run the us-momentum-weekend-research routine.")
        return

    plan = _load_plan(today)
    if not plan or plan.get("status") != "ok" or plan.get("date") != today:
        _journal(f"No entries: no usable plan for {today} (status: {plan.get('status') if plan else 'missing'}).")
        return

    account = get_account()
    equity = float(account["equity"])
    pnl = _daily_pnl_pct(account)
    if pnl <= -DAILY_LOSS_CAP_PCT:
        _journal(f"No entries: daily P&L {pnl:.2%} is at or below the -{DAILY_LOSS_CAP_PCT:.0%} halt.")
        return

    tag = f"{ORDER_PREFIX}{today}-"
    already = [o for o in get_orders(status="all", limit=100) if (o.get("client_order_id") or "").startswith(tag)]
    slots = min(int(plan.get("max_orders", 0)), MAX_TRADES_PER_DAY) - len(already)
    busy = {p["symbol"] for p in get_positions()} | {o["symbol"] for o in get_orders(status="open")}

    placed, skipped = [], []
    for t in plan.get("tickets", []):
        symbol = t["ticker"]
        if symbol in busy:
            skipped.append(f"{symbol}: already held or has an open order")
            continue
        if slots <= 0:
            skipped.append(f"{symbol}: daily order cap reached")
            continue
        shares = _shares(equity, t["trigger"], t["stop"])
        if shares < 1:
            skipped.append(f"{symbol}: sizes to under 1 share")
            continue
        try:
            place_entry_stop_limit(symbol, shares, t["trigger"], t["limit"], f"{tag}{symbol}")
        except requests.HTTPError as e:
            skipped.append(f"{symbol}: order rejected ({e.response.text[:200]})")
            continue
        slots -= 1
        placed.append(f"{symbol} {shares}sh, buy-stop ${t['trigger']:.2f} limit ${t['limit']:.2f}, stop ${t['stop']:.2f}")
        log.info(f"[Momentum] Entry placed: {placed[-1]}")

    _journal(
        f"Pre-open entries. Regime {plan.get('regime')} (cap {plan.get('max_orders')}), equity ${equity:,.2f}.\n"
        f"Placed: {'; '.join(placed) or 'none'}.\n"
        f"Skipped: {'; '.join(skipped) or 'none'}."
    )


def protect():
    """Every few minutes in market hours: enforce the -2% halt and keep a stop on every position."""
    if not _trading_allowed():
        return
    account = get_account()
    open_orders = get_orders(status="open")

    pnl = _daily_pnl_pct(account)
    if pnl <= -DAILY_LOSS_CAP_PCT:
        entries = [o for o in open_orders
                   if o["side"] == "buy" and (o.get("client_order_id") or "").startswith(ORDER_PREFIX)]
        for o in entries:
            cancel_order(o["id"])
        if entries:
            _journal(f"Daily P&L {pnl:.2%} hit the -{DAILY_LOSS_CAP_PCT:.0%} halt: cancelled unfilled entries "
                     f"{', '.join(o['symbol'] for o in entries)}. Stops stay in place.")

    positions = {p["symbol"]: p for p in get_positions()}
    stops = {o["symbol"]: o for o in open_orders if o["side"] == "sell" and o["type"] in STOP_TYPES}
    other_sells = {o["symbol"] for o in open_orders if o["side"] == "sell" and o["type"] not in STOP_TYPES}

    for symbol, o in stops.items():
        if symbol not in positions:
            cancel_order(o["id"])  # a stop with nothing to protect would open a short when hit
            _journal(f"Cancelled the {symbol} stop: no {symbol} position is held.")

    for symbol, p in positions.items():
        qty = int(float(p["qty"]))
        if qty <= 0 or symbol in other_sells:
            continue  # not a long, or a sell is already working
        try:
            stop_order = stops.get(symbol)
            if stop_order:
                if int(float(stop_order["qty"])) != qty:  # the entry filled in pieces
                    replace_order(stop_order["id"], qty=qty)
                    _journal(f"Resized the {symbol} stop to {qty}sh to match the position.")
                continue
            stop = _initial_stop(symbol, float(p["avg_entry_price"]))
            price = float(p["current_price"])
            if price <= stop:
                close_position(symbol)
                _journal(f"{symbol} had no stop and is at ${price:.2f}, at or below its stop ${stop:.2f}: closed at market.")
            else:
                place_stop_order(symbol, qty, stop)
                _journal(f"Placed the {symbol} protective stop: sell {qty}sh at ${stop:.2f}, good until cancelled.")
        except requests.HTTPError as e:
            log.error(f"[Momentum] Could not protect {symbol}: {e.response.text[:300]}")


def _log_fills(today):
    """Append today's fills to trade_log.md; a sell is matched to the latest earlier buy for its P&L."""
    orders = [o for o in get_orders(status="closed", limit=200) if o.get("filled_at")]
    existing = memory.read("trade_log.md")
    rows = []
    for o in orders:
        if o["filled_at"][:10] != today:  # UTC date; regular-hours fills fall on the same ET date
            continue
        symbol, qty, price = o["symbol"], int(float(o["filled_qty"])), float(o["filled_avg_price"])
        if o["side"] == "buy":
            row = f"| {today} | {symbol} | ${price:.2f} | — | {qty} | — | — | US momentum entry filled |"
        else:
            buy = next((b for b in orders if b["symbol"] == symbol and b["side"] == "buy"
                        and b["filled_at"] < o["filled_at"]), None)
            if buy:
                entry = float(buy["filled_avg_price"])
                pnl = (price - entry) * qty
                row = (f"| {today} | {symbol} | ${entry:.2f} | ${price:.2f} | {qty} | ${pnl:+,.2f} "
                       f"({price / entry - 1:+.2%}) | {'✅' if pnl > 0 else '❌'} | US momentum {o['type']} exit |")
            else:
                row = f"| {today} | {symbol} | — | ${price:.2f} | {qty} | — | — | US momentum {o['type']} exit |"
        if row not in existing:
            memory.append("trade_log.md", row)
            rows.append(row)
    return rows


def end_of_day():
    """After the close: raise each stop to the trailing level, log today's fills, journal the book."""
    if not _trading_allowed():
        return
    protect()
    today = memory.today_et()
    positions = {p["symbol"]: p for p in get_positions()}
    stops = {o["symbol"]: o for o in get_orders(status="open") if o["side"] == "sell" and o["type"] in STOP_TYPES}

    raised, book = [], []
    for symbol, p in positions.items():
        o = stops.get(symbol)
        stop = float(o["stop_price"]) if o and o.get("stop_price") else None
        level = _trail_level(symbol) if stop else None
        if level and stop + 0.01 <= level < float(p["current_price"]):
            try:
                replace_order(o["id"], stop_price=level)
                raised.append(f"{symbol} ${stop:.2f} -> ${level:.2f}")
                stop = level
            except requests.HTTPError as e:
                log.error(f"[Momentum] Could not raise the {symbol} stop: {e.response.text[:300]}")
        book.append(f"{symbol} {p['qty']}sh avg ${float(p['avg_entry_price']):.2f} now ${float(p['current_price']):.2f} "
                    f"({float(p['unrealized_plpc']):+.2%}), stop {f'${stop:.2f}' if stop else 'NONE'}")

    fills = _log_fills(today)
    account = get_account()
    _journal(
        f"End of day. Equity ${float(account['equity']):,.2f} (day {_daily_pnl_pct(account):+.2%}).\n"
        f"Positions: {'; '.join(book) or 'none'}.\n"
        f"Stops raised: {'; '.join(raised) or 'none'}.\n"
        f"Fills logged: {len(fills)}."
    )
