import re
import logging
from datetime import datetime
import pytz
from utils import memory, github_sync
from utils.email_client import send_email
from config import EMAIL_RECIPIENT

log = logging.getLogger(__name__)
ET = pytz.timezone("America/New_York")


def _today_journal_entries():
    content = memory.read("reasoning.md")
    today = memory.today_et()
    entries = []
    for block in re.split(r"\n## ", content):
        if block.startswith(today):
            entries.append(block.strip())
    return entries


def _latest_benchmark_row():
    content = memory.read("benchmark_tracking.md")
    rows = [l for l in content.splitlines() if l.startswith("|") and memory.today_et() in l]
    return rows[-1] if rows else "No benchmark data yet"


def run_eod():
    log.info("[Reporter] Compiling EOD report")

    portfolio_content = memory.read("portfolio_state.md")
    positions_content = memory.read("open_positions.md")
    trade_log = memory.read("trade_log.md")
    benchmark_row = _latest_benchmark_row()
    counter_content = memory.read("weekly_trade_counter.md")
    journal_entries = _today_journal_entries()

    trades_today = [
        l for l in trade_log.splitlines()
        if memory.today_et() in l and l.startswith("|")
    ]

    trades_used = memory.get_flag("weekly_trade_counter.md", "trades_this_week") or "0"

    portfolio_lines = [
        l.strip("- ").strip()
        for l in portfolio_content.splitlines()
        if l.strip().startswith("-")
    ]

    daily_pnl_line = next((l for l in portfolio_lines if "Daily P&L" in l), "")
    equity_line = next((l for l in portfolio_lines if "Total equity" in l), "")

    subject_pnl = daily_pnl_line.replace("Daily P&L:", "").strip() if daily_pnl_line else "N/A"
    subject = f"Trading Bot — EOD Summary {memory.today_et()} | P&L: {subject_pnl}"

    text_body = f"""EOD SUMMARY — {memory.today_et()}
{'='*50}

PORTFOLIO
{chr(10).join(portfolio_lines)}

BENCHMARK
{benchmark_row}

TRADES THIS WEEK: {trades_used}/3

TODAY'S TRADES
{chr(10).join(trades_today) if trades_today else '  No trades today'}

OPEN POSITIONS
{positions_content.replace('# Open Positions', '').strip() or '  None'}

BOT REASONING TODAY
{chr(10).join(['  ' + e[:300] for e in journal_entries]) if journal_entries else '  No journal entries'}
"""

    send_email(subject, text_body)

    journal = f"## {memory.now_et()}\nEOD report sent to {EMAIL_RECIPIENT}.\n---"
    memory.append("reasoning.md", journal)
    github_sync.push(f"auto: EOD report sent | {memory.today_et()}")
    log.info("[Reporter] EOD report sent")


def run_weekly():
    log.info("[Reporter] Compiling weekly report")

    metrics = memory.read("performance_metrics.md")
    benchmark = memory.read("benchmark_tracking.md")
    patterns = memory.read("learned_patterns.md")
    trade_log = memory.read("trade_log.md")

    subject = f"Trading Bot — Weekly Summary | {memory.today_et()}"
    text_body = f"""WEEKLY SUMMARY
{'='*50}

PERFORMANCE METRICS
{metrics}

BENCHMARK (portfolio vs SPY)
{benchmark}

LEARNED PATTERNS
{patterns}

FULL TRADE LOG
{trade_log}
"""
    send_email(subject, text_body)

    journal = f"## {memory.now_et()}\nWeekly report sent.\n---"
    memory.append("reasoning.md", journal)
    github_sync.push(f"auto: weekly report sent | {memory.today_et()}")
    log.info("[Reporter] Weekly report sent")
