"""Scheduler for the US momentum executor (engine/momentum.py).

The original research/trade bot (engine/coordinator.py) is retired and no longer scheduled.
Times are US/Eastern, so the US daylight-saving change needs no edits.
"""
import logging
import os
import time
from datetime import datetime
import pytz

from engine import momentum

os.makedirs("logs", exist_ok=True)  # logs/ is gitignored, so it will not exist on a fresh clone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)
ET = pytz.timezone("America/New_York")

ENTRY_FROM, ENTRY_UNTIL = "09:15", "09:30"     # after the pre-open plan routine, before the open only:
                                                 # a plan built mid-session would use partial-day prices
PROTECT_FROM, PROTECT_UNTIL = "09:25", "16:05"
PROTECT_EVERY_MIN = 5
EOD_AT = "16:20"                                 # daily bars are final by then


def run(job):
    try:
        job()
    except Exception:
        log.exception(f"{job.__name__} failed")


def main():
    log.info("US momentum executor starting up")
    run(momentum.protect)  # covers any position that was left without a stop while the PC was off
    last_run = {}
    while True:
        now = datetime.now(ET)
        today, hhmm = now.strftime("%Y-%m-%d"), now.strftime("%H:%M")
        if now.weekday() < 5:
            if ENTRY_FROM <= hhmm < ENTRY_UNTIL and last_run.get("enter") != today:
                last_run["enter"] = today
                run(momentum.enter)
            if (PROTECT_FROM <= hhmm <= PROTECT_UNTIL and now.minute % PROTECT_EVERY_MIN == 0
                    and last_run.get("protect") != hhmm):
                last_run["protect"] = hhmm
                run(momentum.protect)
            if hhmm >= EOD_AT and last_run.get("eod") != today:
                last_run["eod"] = today
                run(momentum.end_of_day)
        time.sleep(20)


if __name__ == "__main__":
    main()
