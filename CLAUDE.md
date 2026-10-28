# AITradingBot — Claude Code Context

## What This Project Is
An automated US momentum trading system on the Alpaca paper account (since 2026-10-20).
A weekend screen (Minervini Trend Template + VCP) and a weekday pre-open plan come from
`us-momentum-routines/` (two Claude desktop routines). After its news check, the pre-open
routine places the plan's entry orders by running `scripts/routine_entries.py`, which calls the
executor's own entry code (paper account only, before 09:10 ET). The Python executor `main.py` →
`engine/momentum.py` places any entries the routine did not and manages every stop.
State: the broker account plus local `memory/*.md` files.

The original Perplexity research bot (`engine/coordinator.py` and the `trading-bot-*`
routines) is **retired**: not scheduled, kept in the repo for reference.

---

## Hard Rules (enforced in code — do not bypass)

| Rule | Value | Where enforced |
|---|---|---|
| Max position size | 5% of equity | `config.py`, `engine/momentum.py` |
| Risk per trade | 0.5% of equity down to the stop | `config.py` (`MOMENTUM_RISK_PCT`), `engine/momentum.py` |
| Daily loss halt | -2%: no entries, unfilled entries cancelled; stops stay | `engine/momentum.py` |
| Max orders per day | 3 (and the regime cap: Offense 3, Selective 1, Defense 0) | `config.py`, `engine/momentum.py` |
| No options | Stocks only | `ALLOW_OPTIONS = False`; the screen universe is S&P 500 stocks |
| Paper trading | Until `live_trading: true` in strategy.md | `engine/momentum.py` (`_trading_allowed`) |
| Routine entries | Paper account only (even after `live_trading: true`), before 09:10 ET | `scripts/routine_entries.py` |

---

## How It Trades (`engine/momentum.py`)

- **Entry (before the open):** each ticket in `us-momentum-routines/plans/<date>.json`
  becomes a buy stop-limit day order at the plan's trigger and limit. The pre-open routine places
  them via `scripts/routine_entries.py` until 09:10 ET; the executor's own run at 09:15–09:30 ET
  places any it did not. Both use `momentum.enter()`, and a repeated `client_order_id` is rejected,
  so the two runs cannot double an entry. No entries if the weekend screen is over 9 days old.
  If the plan routine has not run, the executor builds the plan itself.
- **Protection (every 5 min, 09:25–16:05 ET, and at startup):** every position gets a
  good-until-cancelled sell stop at the plan's stop (fallback: `max_stop_pct` below entry).
- **Trailing (16:20 ET):** each stop is raised to just under the lowest low of the last
  10 sessions; it is never lowered. Fills are written to `memory/trade_log.md`.

---

## Schedule

| When | What | Where |
|---|---|---|
| Saturdays 09:07 ICT | Weekend screen | Claude desktop routine `us-momentum-weekend-research` |
| Weekdays 19:07 ICT (20:07 from 2 Nov 2026) | Pre-open plan + news check, then entry orders (paper only) | Claude desktop routine `us-momentum-preopen-plan` |
| Continuous while logged in | Executor (times in US/Eastern) | Windows task `AITradingBot` → `run_bot.bat` → `main.py` |

---

## What NOT to Do

- Never commit `.env` — it contains real API keys
- Never set `live_trading: true` without at least 4 weeks of paper trading results
- Never add options trading — `ALLOW_OPTIONS = False` is a hard rule
- Never edit `memory/reasoning.md` manually — it is append-only
- Never let a Claude routine place an order except through `scripts/routine_entries.py`: no direct
  Alpaca API calls, no order changes or cancels (stops belong to the executor), and never on a live account
- Never add a new skill by editing `.claude/commands/` — skills now live in `.claude/skills/`
