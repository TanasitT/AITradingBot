import logging
import os
import schedule
import time
from datetime import datetime
import pytz

from engine import coordinator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)
ET = pytz.timezone("America/New_York")


def et_now():
    return datetime.now(ET)


def is_weekday():
    return et_now().weekday() < 5


def run_if_weekday(fn):
    def wrapper():
        if is_weekday():
            fn()
        else:
            log.info(f"Weekend — skipping {fn.__name__}")
    return wrapper


def check_trade_trigger():
    trigger_path = os.path.join("memory", "trade_trigger.md")
    if os.path.exists(trigger_path):
        try:
            with open(trigger_path, encoding="utf-8") as f:
                if "status: pending" in f.read():
                    coordinator.run_from_trigger()
        except Exception as e:
            log.warning(f"[Trigger] Failed to read trade_trigger.md: {e}")


schedule.every(30).seconds.do(check_trade_trigger)
schedule.every().day.at("08:33").do(run_if_weekday(coordinator.run_pre_market))
schedule.every().day.at("09:37").do(run_if_weekday(coordinator.run_market_open))
schedule.every(15).minutes.do(run_if_weekday(coordinator.run_intraday))
schedule.every().day.at("12:03").do(run_if_weekday(coordinator.run_pre_market))
schedule.every().day.at("15:47").do(run_if_weekday(coordinator.run_eod))
schedule.every().day.at("18:17").do(run_if_weekday(coordinator.run_pre_market))
schedule.every().monday.at("07:00").do(coordinator.run_benchmark)

# Friday-only weekly summary (approximated via daily check)
def maybe_weekly_summary():
    if is_weekday() and et_now().weekday() == 4:
        coordinator.run_weekly_summary()

schedule.every().day.at("17:23").do(maybe_weekly_summary)


if __name__ == "__main__":
    log.info("AI Trading Bot starting up")
    log.info("Schedules registered — entering loop")
    while True:
        schedule.run_pending()
        time.sleep(30)
