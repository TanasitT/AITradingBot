import re
import logging
from utils import memory
from utils.perplexity_client import research_ticker, get_market_context
from utils import github_sync

log = logging.getLogger(__name__)


def parse_score(text):
    m = re.search(r"SCORE:\s*(\d+)\s*/\s*100", text, re.IGNORECASE)
    return int(m.group(1)) if m else 0


def parse_trade_ok(text):
    m = re.search(r"TRADE_OK:\s*(yes|no)", text, re.IGNORECASE)
    return m and m.group(1).lower() == "yes"


def run(tickers=None):
    log.info("[Research] Starting research run")

    watchlist_content = memory.read("watchlist.md")
    if tickers:
        symbols = [t.upper() for t in tickers]
    else:
        active_section = re.search(
            r"## Active.*?\n(.*?)(?=##|\Z)", watchlist_content, re.DOTALL
        )
        if active_section:
            symbols = [
                s.strip() for s in active_section.group(1).replace(",", " ").split()
                if s.strip().isupper() and len(s.strip()) <= 5
            ]
        else:
            from config import WATCHLIST_SEEDS
            symbols = WATCHLIST_SEEDS

    market_text = get_market_context()
    trade_ok = parse_trade_ok(market_text)
    log.info(f"[Research] Market context: TRADE_OK={trade_ok}")

    vix_match = re.search(r"VIX[:\s]+(\d+\.?\d*)", market_text, re.IGNORECASE)
    vix = float(vix_match.group(1)) if vix_match else 20.0

    spy_ok = "above" in market_text.lower() and "5-day" in market_text.lower()

    memory.write("daily_context.md", f"# Daily Market Context\nLast updated: {memory.now_et()}\n\n{market_text}")

    results = []
    for symbol in symbols:
        try:
            analysis = research_ticker(symbol)
            score = parse_score(analysis)
            results.append((symbol, score, analysis))
            log.info(f"[Research] {symbol}: {score}/100")
        except Exception as e:
            log.warning(f"[Research] Failed to research {symbol}: {e}")

    results.sort(key=lambda x: x[1], reverse=True)

    cache_lines = [f"# Research Cache — {memory.now_et()}\n"]
    for symbol, score, analysis in results:
        cache_lines.append(f"## {symbol} | Score: {score}/100\n\n{analysis}\n\n---\n")
    memory.write("research_cache.md", "\n".join(cache_lines))

    top = [f"{s}({sc})" for s, sc, _ in results[:5] if sc >= 60]
    journal_entry = (
        f"## {memory.now_et()}\n"
        f"Research complete. {len(symbols)} tickers scanned. "
        f"Top candidates: {', '.join(top) if top else 'none above threshold'}. "
        f"Market TRADE_OK={trade_ok}, VIX={vix:.1f}.\n---"
    )
    memory.append("reasoning.md", journal_entry)

    github_sync.push(f"auto: research update | {len(symbols)} tickers | top: {top[:3]}")
    log.info("[Research] Done")
    return results
