# AITradingBot — Claude Code Context

## What This Project Is
An automated US momentum trading system on the Alpaca paper account (since 2026-10-20). It runs
without the local machine (since 2026-11-17):
- Two Claude Code **cloud routines** (claude.ai/code/routines) run on a fresh checkout of this repo.
  The weekday pre-open routine runs the screen (Minervini Trend Template + VCP) and the plan from
  `us-momentum-routines/`, checks each ticket's news, then places the entries with
  `scripts/routine_entries.py` (paper account only, before 09:10 ET). The Saturday routine runs the
  screen as a weekly report and places nothing.
- The executor's stop jobs run on **GitHub Actions** (`.github/workflows/executor.yml` →
  `python main.py protect` / `python main.py eod`).
- Nothing is kept between runs: no results, plans or journal are saved, and the broker account is
  the only state. Each routine's final message on claude.ai is its record.

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
| Paper trading | Until `live_trading: true` in `memory/strategy.md` (a local file the cloud runs do not have, so they trade paper only) | `engine/momentum.py` (`_trading_allowed`) |
| Routine entries | Paper account only (even after `live_trading: true`), before 09:10 ET | `scripts/routine_entries.py` |

---

## How It Trades (`engine/momentum.py`)

- **Entry (before the open):** the pre-open routine builds `us-momentum-routines/plans/<date>.json`,
  removes tickets with bad news, and runs `scripts/routine_entries.py`, which calls `momentum.enter()`.
  Each ticket becomes a buy stop-limit day order at the plan's trigger and limit. A repeated
  `client_order_id` is rejected, so a retry cannot double an entry. Entries come only from that
  news-checked plan: nothing else builds a plan or enters, so if the routine fails there are no
  entries that day. No entries if the screen is over 9 days old.
- **Protection (every 10 min while the market is open):** every position gets a good-until-cancelled
  sell stop at the plan's stop, rebuilt from the filled entry order (trigger = its stop price, plus
  the 10 sessions before its date); fallback `max_stop_pct` below entry.
- **Trailing (16:23 ET):** each stop is raised to just under the lowest low of the last
  10 sessions; it is never lowered.
- The Actions log is public: `main.py` one-shot jobs print only done / skipped / failed, and exit 1
  on any error so the run fails and GitHub emails the owner.

---

## Schedule

| When | What | Where |
|---|---|---|
| Saturdays 02:07 UTC (09:07 ICT) | Weekly screen report, no orders | Cloud routine `us-momentum-weekend-research` |
| Weekdays 12:07 UTC (19:07 ICT; 07:07 ET in winter, 08:07 ET in summer) | Screen, plan, news check, entries (paper only) | Cloud routine `us-momentum-preopen-plan` |
| Every 10 min, 13:00–20:59 UTC on weekdays | Stop check (skipped while the market is closed) | GitHub Actions `executor` (`main.py protect`) |
| 20:23 and 21:23 UTC on weekdays | Trail stops (the run before the close is skipped) | GitHub Actions `executor` (`main.py eod`) |

`python main.py` with no argument runs both stop jobs on a loop, for running on your own machine
instead of Actions. Do not run it alongside Actions without a reason.

---

## What NOT to Do

- Never commit `.env` — it contains real API keys. The cloud runs get the keys from the claude.ai
  environment's variables and from the repository's Actions secrets
- Never print executor details (symbols, sizes, prices) to stdout in the Actions workflow — the repo is public
- Never set `live_trading: true` without at least 4 weeks of paper trading results
- Never add options trading — `ALLOW_OPTIONS = False` is a hard rule
- Never edit `memory/reasoning.md` manually — it is append-only
- Never let a Claude routine place an order except through `scripts/routine_entries.py`: no direct
  Alpaca API calls, no order changes or cancels (stops belong to the executor), and never on a live account
- Never add a new skill by editing `.claude/commands/` — skills now live in `.claude/skills/`
