"""Entry orders for the us-momentum-preopen-plan routine.

The routine runs this after its news check. It places today's plan with the executor's own
entry code (engine/momentum.enter), so sizing, the order caps, the -2% halt and the
duplicate-order guard stay enforced in code. Two limits apply on top of that:
- Paper account only. A Claude routine never places live orders, even once live_trading is true.
- Before 09:10 ET only. After the open the plan's prices would be partial-day.
Stops are not handled here: the executor (python main.py, run by GitHub Actions) places and
trails them.
Run from the repo root:
  python scripts/routine_entries.py           place today's entries
  python scripts/routine_entries.py --check   read-only: are the keys set, is it the paper
                                              account, is today a trading day
"""
import logging
import os
import sys
from datetime import datetime

import pytz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from config import ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL  # noqa: E402

ET = pytz.timezone("America/New_York")
LAST_ENTRY = "09:10"


def check():
    """Read-only preflight. Prints no keys and no account balances."""
    if not (ALPACA_API_KEY and ALPACA_SECRET_KEY):
        print("CHECK FAILED: ALPACA_API_KEY and ALPACA_SECRET_KEY are not both set.")
        return 1
    if "paper" not in ALPACA_BASE_URL:
        print("CHECK FAILED: ALPACA_BASE_URL is not the paper account. The routine never places live orders.")
        return 2
    from utils.alpaca_client import get_account, get_clock
    try:
        status = get_account().get("status")
        clock = get_clock()
    except Exception as e:
        print(f"CHECK FAILED: the Alpaca paper API did not answer ({type(e).__name__}).")
        return 1
    today = datetime.now(ET).strftime("%Y-%m-%d")
    trading_day = clock["is_open"] or clock["next_open"][:10] == today
    print(f"CHECK OK: Alpaca paper account {status}. "
          f"{today} is {'a trading day' if trading_day else 'not a trading day'}.")
    return 0


def main():
    if "--check" in sys.argv[1:]:
        return check()
    if "paper" not in ALPACA_BASE_URL:
        print("REFUSED: ALPACA_BASE_URL is not the paper account. The routine never places live orders.")
        return 2
    now = datetime.now(ET)
    if now.strftime("%H:%M") >= LAST_ENTRY:
        print(f"REFUSED: it is {now:%H:%M} ET, at or after {LAST_ENTRY} ET. No entries are placed today.")
        return 3

    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.FileHandler("logs/bot.log", encoding="utf-8"), logging.StreamHandler()],
    )
    from engine import momentum
    from utils.alpaca_client import get_orders

    momentum.enter()  # journals its own "US momentum executor" entry in memory/reasoning.md

    tag = f"{momentum.ORDER_PREFIX}{now:%Y-%m-%d}-"
    ours = [o for o in get_orders(status="all", limit=100) if (o.get("client_order_id") or "").startswith(tag)]
    print(f"Entry orders for {now:%Y-%m-%d}: {len(ours) or 'none'}")
    for o in ours:
        print(f"  {o['symbol']} {o['qty']}sh buy-stop ${o['stop_price']} limit ${o['limit_price']} "
              f"status {o['status']} id {o['id']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
