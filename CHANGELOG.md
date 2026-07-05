# Changelog

All notable changes to AITradingBot are documented here.

---

## [0.5.0] — 2026-07-05

### Changed
- **Restructured project to follow Claude Code best practices**
  - `.claude/commands/` renamed to `.claude/skills/` — all 5 skill files moved
  - `agents/` (Python modules) renamed to `engine/` to eliminate naming conflict with Claude Code's
    agent convention (`agents` now means `.claude/agents/*.md` sub-agent definitions)
  - All imports updated: `main.py`, `engine/coordinator.py`

### Added
- **`.claude/agents/` sub-agent definitions** — four `.md` files with YAML frontmatter:
  - `researcher.md` — Perplexity AI research agent
  - `trader.md` — Alpaca order placement agent
  - `monitor.md` — intraday position monitor agent
  - `reporter.md` — EOD/weekly email report agent
- **Trimmed `CLAUDE.md`** — removed redundant file tree, current status, tutorial sections;
  kept only hard rules, config constants, schedule, and what-NOT-to-do safeguards

---

## [Unreleased] — Active Development

---

## [0.4.0] — 2026-07-03

### Fixed
- **Volume threshold lowered from 2x to 1.25x** — the 2x requirement was blocking every trade.
  Even strong catalyst stocks (COIN +11.87% on stablecoin deal) only reached 1.35x because
  Alpaca's IEX data feed captures only ~7–15% of total SIP market volume, making 2x unrealistic.
  1.25x still confirms above-average institutional interest.
  - `config.py` — `MIN_VOLUME_MULTIPLIER` 2.0 → 1.25
  - `memory/risk_rules.md` — updated threshold
  - `memory/strategy.md` — updated entry criteria
  - `.claude/commands/trade.md` — Step 9 updated
  - `.claude/commands/research.md` — volume note added
  - `MANUAL.md` — Rule 2 explanation updated

---

## [0.3.0] — 2026-06-30

### Added
- **Inverse ETF support (SH)** — bot can now profit during market downturns
  - SH (1x inverse SPY) added to `memory/watchlist.md`
  - When SPY is below its 5-day MA, bot evaluates SH instead of regular stocks
  - SH entry threshold: score ≥ 60 (vs 70 for stocks)
  - SH position size limit: 3% of portfolio (vs 5% for stocks)
  - SH exit trigger: closes immediately when SPY reclaims 5-day MA
  - No leveraged inverse ETFs allowed (SQQQ, SPXS blocked)
  - `.claude/commands/research.md` — SH scoring logic added
  - `.claude/commands/trade.md` — Step 8 routes to SH when market is bearish
  - `memory/risk_rules.md` — SH-specific rules section added
  - `memory/strategy.md` — inverse ETF entry criteria added

- **MANUAL.md** — plain-English user manual created covering:
  - All key terms (SPY, VIX, volume, stop-loss, take-profit, ETF, paper trading, alpha)
  - Full daily schedule in Bangkok time
  - All 5 entry rules with explanations
  - Position sizing table
  - Exit rules (stop-loss, take-profit tiers, force-close triggers)
  - Inverse ETF mode explanation
  - Memory files reference table
  - How to tune the bot without code
  - How to switch to live trading

---

## [0.2.0] — 2026-06-23

### Changed
- **Trade limit changed from 3 per week to 3 per day**
  - `config.py` — `MAX_TRADES_PER_WEEK` renamed to `MAX_TRADES_PER_DAY`
  - `agents/risk_manager.py` — `weekly_trades_remaining()` → `daily_trades_remaining()`
  - `agents/execution.py` — fixed hardcoded `trades_remaining` calculation
  - `agents/monitor.py` — `reset_weekly_counter()` → `reset_daily_counter()`
  - `agents/coordinator.py` — counter now resets every EOD (was Saturday only)
  - `memory/strategy.md` — rule updated to "DAILY TRADE LIMIT"
  - `.claude/commands/trade.md` — Step 2 label updated

---

## [0.1.1] — 2026-06-17

### Fixed
- Removed `ANTHROPIC_API_KEY` from `.env.example` and `config.py` — not needed since
  Claude is the runtime via local routines, not a Python API caller

### Changed
- Cloud routines reduced from 8 to 5 (pre-market, market-open, intraday monitor, EOD,
  weekly summary) due to Claude desktop 5-routine daily limit
- Switched from cloud routines (CCR) to local Claude desktop routines — cloud routines
  blocked `github.com` egress, making GitHub-based memory inaccessible
- All routine prompts updated to use local Windows paths (`d:\AITradingBot\memory\`)
  instead of Linux paths (`/home/user/AITradingBot/`)

---

## [0.1.0] — 2026-06-17 — Initial Release

### Added
- **Full project scaffold** at `d:\AITradingBot`
- **5 Claude skills** (slash commands):
  - `/research` — Perplexity AI market scan, scores tickers 0–100
  - `/trade` — Alpaca order placement with full rule enforcement (12 steps)
  - `/journal` — append timestamped reasoning entry to `memory/reasoning.md`
  - `/benchmark` — append daily portfolio vs SPY snapshot to benchmark tracking
  - `/report` — compile EOD summary and email to jankla2010@gmail.com
- **8 Python agents**: coordinator, research, technical, risk_manager, execution,
  monitor, reporter, benchmark
- **Utility modules**: alpaca_client, perplexity_client, email_client, github_sync, memory
- **15 memory files** in `memory/` — GitHub used as persistent data store
- **Hard rules enforced in code**:
  - Max 5% of portfolio per position
  - Daily loss cap -2% halts all routines
  - Max 3 trades per day
  - No options — stocks and approved ETFs only
  - Paper trading mode until `live_trading: true` set in `strategy.md`
- **Local Python scheduler** (`main.py`) using `schedule` library for Windows execution
- **`run_bot.bat`** — one-click launcher for Windows

### Trading Activity
- **2026-06-22** — First trade executed: BUY NVDA 23 shares @ $213.39
  - Closed same day EOD @ $207.88 (no overnight thesis confirmed by Perplexity)
  - Trade P&L: -$126.63 (-2.58%)
  - Week alpha vs SPY: +1.46% (SPY fell -1.59%, portfolio -0.13%)

---

## Hard Rules Reference (never change without understanding consequences)

| Rule | Value |
|---|---|
| Max position size | 5% of portfolio (3% for SH inverse ETF) |
| Daily loss halt | -2% stops all trading for the day |
| Max trades per day | 3 |
| No options | Stocks and approved ETFs only |
| Paper trading | Active until `live_trading: true` in strategy.md |
| Min research score | 70/100 (60/100 for SH) |
| Min volume | 1.25x 30-day average |
| Max VIX | 28 |
| SPY condition | Above 5-day MA for stocks; below 5-day MA for SH |
