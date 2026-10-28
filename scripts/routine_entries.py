"""Entry orders for the us-momentum-preopen-plan routine.

The routine runs this after its news check. It places today's plan with the executor's own
entry code (engine/momentum.enter), so sizing, the order caps, the -2% halt and the
duplicate-order guard stay enforced in code. Two limits apply on top of that:
- Paper account only. A Claude routine never places live orders, even once live_trading is true.
- Before 09:10 ET only. The executor's own entry run starts at 09:15, and after the open the
  plan's prices would be partial-day.
Stops are not handled here: the executor (main.py) places and trails them.
Run from the repo root:  python scripts/routine_entries.py
"""
import logging
import os
import subprocess
import sys
from datetime import datetime

import pytz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from config import ALPACA_BASE_URL  # noqa: E402

ET = pytz.timezone("America/New_York")
LAST_ENTRY = "09:10"


def _executor_running():
    try:
        out = subprocess.run(["schtasks", "/query", "/tn", "AITradingBot", "/fo", "csv", "/nh"],
                             capture_output=True, text=True, timeout=30).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    return "Running" in out if out else None


def main():
    if "paper" not in ALPACA_BASE_URL:
        print("REFUSED: ALPACA_BASE_URL is not the paper account. The routine never places live orders.")
        return 2
    now = datetime.now(ET)
    if now.strftime("%H:%M") >= LAST_ENTRY:
        print(f"REFUSED: it is {now:%H:%M} ET, at or after {LAST_ENTRY} ET. "
              "The executor's 09:15 ET run places the entries instead.")
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

    running = _executor_running()
    if running is False:
        print("WARNING: the AITradingBot task (main.py) is not running. A fill gets no protective stop "
              "until it starts.")
    elif running is None:
        print("WARNING: could not confirm the AITradingBot task (main.py) is running. It places the stops.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
