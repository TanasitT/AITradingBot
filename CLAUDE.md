# AITradingBot — Claude Code Context

## What This Project Is
An automated stock trading bot: Perplexity AI research → Alpaca paper trading → Gmail reports.
Runs on a schedule via Claude desktop local routines. All state in local `memory/*.md` files.

---

## Hard Rules (enforced in code — do not bypass)

| Rule | Value | Where enforced |
|---|---|---|
| Max position size | 5% of portfolio (3% for SH) | `config.py`, `engine/risk_manager.py` |
| Daily loss halt | -2% stops all trading for the day | `engine/monitor.py`, `engine/coordinator.py` |
| Max trades per day | 3 | `config.py`, `engine/risk_manager.py` |
| No options | Stocks + approved ETFs only | `engine/risk_manager.py`, `/trade` skill |
| Paper trading | Until `live_trading: true` in strategy.md | `engine/coordinator.py` |

---

## Entry Criteria (all must be true)

- Research score ≥ 70/100 (60/100 for SH inverse ETF)
- Volume ≥ 1.25x 30-day average
- SPY above 5-day MA (or below MA → evaluate SH instead)
- VIX < 28
- Daily trade count < 3
- Daily portfolio loss < 2%

---

## Key Config Values (`config.py`)

```python
MAX_POSITION_PCT = 0.05        # 5% per trade
DAILY_LOSS_CAP_PCT = 0.02      # -2% halt
MAX_TRADES_PER_DAY = 3
MIN_RESEARCH_SCORE = 70
MIN_VOLUME_MULTIPLIER = 1.25
MAX_VIX = 28.0
SYNC_TO_GITHUB = False         # set True to re-enable git push/pull
```

---

## Daily Routine Schedule (Bangkok time / ICT)

| Time | Routine | What It Does |
|---|---|---|
| 7:33 PM Mon–Fri | pre-market-research | Perplexity scan, score all watchlist tickers |
| 8:37 PM Mon–Fri | market-open | Evaluate scores, place trades if all criteria pass |
| 8:30–11:30 PM Mon–Fri | intraday-monitor (x4) | Check stop-loss and take-profit on open positions |
| 2:47 AM Tue–Sat | eod | Close weak positions, send email report, reset daily counter |
| 4:23 AM Saturdays | weekly-summary | Full week recap, email sent, performance metrics updated |

---

## Inverse ETF Mode (SH)

When SPY is below its 5-day MA, regular stock entries are blocked.
The bot evaluates **SH** (1x inverse SPY ETF) instead:
- Entry threshold: score ≥ 60
- Position size: 3% of portfolio max
- Exit: immediately when SPY reclaims 5-day MA
- No leveraged inverse ETFs (SQQQ, SPXS, etc.)

---

## What NOT to Do

- Never commit `.env` — it contains real API keys
- Never set `live_trading: true` without at least 4 weeks of paper trading results
- Never add options trading — `ALLOW_OPTIONS = False` is a hard rule
- Never edit `memory/reasoning.md` manually — it is append-only
- Never add a new skill by editing `.claude/commands/` — skills now live in `.claude/skills/`
