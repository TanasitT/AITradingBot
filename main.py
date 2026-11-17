"""Runs the US momentum executor's stop jobs (engine/momentum.py).

  python main.py protect   one stop check; skipped while the market is closed
  python main.py eod       raise the stops after the close; skipped before 16:20 ET
  python main.py           both jobs on a loop, for running on your own machine instead

The GitHub Actions workflow (.github/workflows/executor.yml) runs the one-shot jobs. Entries are
not placed here: the pre-open routine places them with scripts/routine_entries.py after its news
check. Times are US/Eastern, so the US daylight-saving change needs no edits.
"""
import logging
import os
import sys
import time
from datetime import datetime
import pytz

from engine import momentum
from utils.alpaca_client import get_clock

ET = pytz.timezone("America/New_York")
log = logging.getLogger(__name__)

PROTECT_FROM, PROTECT_UNTIL = "09:25", "16:05"
PROTECT_EVERY_MIN = 5
EOD_AT = "16:20"                                 # daily bars are final by then


class _ErrorCount(logging.Handler):
    def __init__(self):
        super().__init__(logging.ERROR)
        self.count = 0

    def emit(self, record):
        self.count += 1


def _setup_logging(to_console):
    os.makedirs("logs", exist_ok=True)  # logs/ is gitignored, so it will not exist on a fresh clone
    handlers = [logging.FileHandler("logs/bot.log", encoding="utf-8")]
    if to_console:
        handlers.append(logging.StreamHandler())
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                        handlers=handlers)


def run(job):
    try:
        job()
    except Exception:
        log.exception(f"{job.__name__} failed")


def once(name):
    """One job, for a scheduler. The repo is public, so the Actions log must not show trades:
    print only done / skipped / failed, and keep the details in logs/bot.log on the runner.
    Exits 1 if the job raised or logged an error, so the workflow run fails and GitHub emails you."""
    _setup_logging(to_console=False)
    errors = _ErrorCount()
    logging.getLogger().addHandler(errors)
    now = datetime.now(ET)
    try:
        if name == "protect":
            if not get_clock()["is_open"]:
                print("protect: skipped, the market is closed")
                return 0
            momentum.protect()
        elif name == "eod":
            if now.weekday() >= 5 or now.strftime("%H:%M") < EOD_AT or get_clock()["is_open"]:
                print(f"eod: skipped, runs on weekdays from {EOD_AT} ET once the market has closed")
                return 0
            momentum.end_of_day()
        else:
            print(f"unknown job {name!r}: use protect or eod")
            return 2
    except Exception as e:
        log.exception(f"{name} failed")
        print(f"{name}: failed ({type(e).__name__})")
        return 1
    if errors.count:
        print(f"{name}: finished with {errors.count} error(s)")
        return 1
    print(f"{name}: done")
    return 0


def loop():
    _setup_logging(to_console=True)
    log.info("US momentum executor starting up")
    run(momentum.protect)  # covers any position that was left without a stop while the PC was off
    last_run = {}
    while True:
        now = datetime.now(ET)
        today, hhmm = now.strftime("%Y-%m-%d"), now.strftime("%H:%M")
        if now.weekday() < 5:
            if (PROTECT_FROM <= hhmm <= PROTECT_UNTIL and now.minute % PROTECT_EVERY_MIN == 0
                    and last_run.get("protect") != hhmm):
                last_run["protect"] = hhmm
                run(momentum.protect)
            if hhmm >= EOD_AT and last_run.get("eod") != today:
                last_run["eod"] = today
                run(momentum.end_of_day)
        time.sleep(20)


if __name__ == "__main__":
    sys.exit(once(sys.argv[1]) if len(sys.argv) > 1 else loop())
