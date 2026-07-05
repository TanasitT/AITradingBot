import logging
from utils import memory, github_sync
from utils.alpaca_client import get_account, get_bars

log = logging.getLogger(__name__)


def run():
    log.info("[Benchmark] Running daily benchmark snapshot")

    account = get_account()
    equity = float(account["equity"])

    spy_bars = get_bars("SPY", timeframe="1Day", limit=2)
    spy_close = spy_bars[-1]["c"] if spy_bars else 0
    spy_prev = spy_bars[-2]["c"] if len(spy_bars) >= 2 else spy_close
    spy_chg_pct = (spy_close - spy_prev) / spy_prev if spy_prev else 0

    content = memory.read("benchmark_tracking.md")
    lines = [l for l in content.splitlines() if l.startswith("|") and not l.startswith("| Date")]

    prev_equity = equity
    for line in reversed(lines):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3:
            val_str = parts[2].replace("$", "").replace(",", "").strip()
            try:
                prev_equity = float(val_str)
                break
            except ValueError:
                pass

    portfolio_chg_pct = (equity - prev_equity) / prev_equity if prev_equity else 0
    alpha = portfolio_chg_pct - spy_chg_pct

    row = (
        f"| {memory.today_et()} "
        f"| ${equity:,.2f} "
        f"| {portfolio_chg_pct:+.2%} "
        f"| ${spy_close:.2f} "
        f"| {spy_chg_pct:+.2%} "
        f"| {alpha:+.2%} |"
    )
    memory.append("benchmark_tracking.md", row)

    journal = (
        f"## {memory.now_et()}\n"
        f"Benchmark logged. Portfolio: ${equity:,.2f} ({portfolio_chg_pct:+.2%}) | "
        f"SPY: ${spy_close:.2f} ({spy_chg_pct:+.2%}) | Alpha: {alpha:+.2%}\n---"
    )
    memory.append("reasoning.md", journal)

    github_sync.push(f"auto: benchmark | portfolio {portfolio_chg_pct:+.2%} | SPY {spy_chg_pct:+.2%} | alpha {alpha:+.2%}")
    log.info(f"[Benchmark] Done — alpha: {alpha:+.2%}")
