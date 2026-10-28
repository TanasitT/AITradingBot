"""
Historical backtest of the bot's mechanical strategy (technical + risk rules)
against Alpaca daily bars. Does NOT include the Perplexity research-score
gate (score >= 70) — that's LLM judgment and can't be reconstructed for past
dates. This tests the pure technical/risk-management edge.

Simplifications vs. the live bot (daily bars only, no intraday ticks):
  - Decisions and fills happen at each day's close (standard EOD backtest).
  - Stop-loss / trailing-stop exits use the day's low to detect a hit
    intraday, filling at the stop price (or the open, if it gapped through).
  - VIX filter is skipped — no free historical VIX series wired up here.
  - Volume ratio compares today's volume to the prior 30 trading days'
    average (excludes today), rather than mixing today into the average.
  - Candidate ranking (since there's no score) uses volume_ratio descending.

Run: python scripts/backtest.py
"""
import sys
import os
import statistics
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.alpaca_client import get_bars_range
from config import WATCHLIST_SEEDS

STARTING_CASH = 100_000.0
MAX_POSITION_PCT = 0.05
MAX_TRADES_PER_DAY = 3
DAILY_LOSS_CAP_PCT = 0.02
MIN_VOLUME_MULTIPLIER = 1.25
HIGH_BETA_THRESHOLD = 1.5
STOP_LOSS_DEFAULT_PCT = 0.05
STOP_LOSS_HIGH_BETA_PCT = 0.07
TAKE_PROFIT_T1_PCT = 0.08
TRAILING_STOP_PCT = 0.03
SPY_MA_DAYS = 5

BENCHMARKS = {"SPY", "QQQ"}
SYMBOLS = [t for t in WATCHLIST_SEEDS if t not in BENCHMARKS]

SIM_YEARS = 2
sim_end = date.today() - timedelta(days=1)
sim_start = date(sim_end.year - SIM_YEARS, sim_end.month, sim_end.day)
fetch_start = sim_start - timedelta(days=400)  # warmup for MA200/RSI


def fetch_all():
    data = {}
    for sym in SYMBOLS + ["SPY"]:
        bars = get_bars_range(sym, fetch_start.isoformat(), sim_end.isoformat())
        data[sym] = {b["t"][:10]: b for b in bars}
        data[sym + "__ordered_dates"] = sorted(data[sym].keys())
    return data


def rolling_stats(dates, bars_by_date, idx):
    """Compute technical signals for bars_by_date at position idx in dates (inclusive)."""
    window_dates = dates[max(0, idx - 200):idx + 1]
    closes = [bars_by_date[d]["c"] for d in window_dates]
    volumes = [bars_by_date[d]["v"] for d in window_dates]
    current_price = closes[-1]

    if len(volumes) >= 31:
        avg_volume_30d = statistics.mean(volumes[-31:-1])
    elif len(volumes) >= 2:
        avg_volume_30d = statistics.mean(volumes[:-1])
    else:
        avg_volume_30d = volumes[-1]
    volume_ratio = volumes[-1] / avg_volume_30d if avg_volume_30d else 0

    ma5 = statistics.mean(closes[-5:]) if len(closes) >= 5 else None
    ma50 = statistics.mean(closes[-50:]) if len(closes) >= 50 else None

    gains = [max(closes[i] - closes[i - 1], 0) for i in range(1, len(closes))]
    losses = [max(closes[i - 1] - closes[i], 0) for i in range(1, len(closes))]
    period = 14
    if len(gains) >= period:
        avg_gain = statistics.mean(gains[-period:])
        avg_loss = statistics.mean(losses[-period:])
        rs = avg_gain / avg_loss if avg_loss else 100
        rsi = 100 - (100 / (1 + rs))
        rsi_sufficient = True
    else:
        rsi = None
        rsi_sufficient = False

    daily_returns = [(closes[i] - closes[i - 1]) / closes[i - 1] for i in range(1, len(closes))]
    if len(daily_returns) >= 20:
        vol = statistics.stdev(daily_returns[-20:])
        beta = vol / 0.01
    else:
        beta = 1.0

    above_ma50 = current_price > ma50 if ma50 else None
    high_beta = beta > HIGH_BETA_THRESHOLD
    volume_ok = volume_ratio >= MIN_VOLUME_MULTIPLIER
    rsi_ok = (not rsi_sufficient) or (40 <= rsi <= 70)
    technically_sound = volume_ok and rsi_ok and (above_ma50 is not False)

    return {
        "price": current_price,
        "volume_ratio": volume_ratio,
        "high_beta": high_beta,
        "technically_sound": technically_sound,
        "ma5": ma5,
    }


def main():
    print(f"Fetching {SIM_YEARS}y of daily bars for {len(SYMBOLS)} symbols + SPY "
          f"({fetch_start} -> {sim_end})...")
    data = fetch_all()

    spy_dates_all = data["SPY__ordered_dates"]
    sim_dates = [d for d in spy_dates_all if date.fromisoformat(d) >= sim_start]
    if not sim_dates:
        print("No SPY trading days in range — aborting.")
        return

    spy_bars = data["SPY"]

    cash = STARTING_CASH
    positions = {}  # symbol -> dict
    prev_close_equity = STARTING_CASH
    equity_curve = []
    trade_log = []

    for date_str in sim_dates:
        idx_spy = spy_dates_all.index(date_str)
        spy_window = spy_dates_all[max(0, idx_spy - 5):idx_spy + 1]
        spy_closes = [spy_bars[d]["c"] for d in spy_window]
        spy_ma5 = statistics.mean(spy_closes[-5:]) if len(spy_closes) >= 5 else None
        spy_ok = spy_ma5 is not None and spy_closes[-1] > spy_ma5

        today_bars = {}
        for sym in SYMBOLS:
            b = data[sym].get(date_str)
            if b:
                today_bars[sym] = b

        # 1. Exits
        for sym in list(positions):
            if sym not in today_bars:
                continue
            bar = today_bars[sym]
            pos = positions[sym]
            pos["high_since_entry"] = max(pos["high_since_entry"], bar["h"])

            exit_price, reason = None, None
            if bar["l"] <= pos["stop_price"]:
                exit_price = pos["stop_price"] if bar["o"] > pos["stop_price"] else bar["o"]
                reason = "stop_loss"
            else:
                gain = (pos["high_since_entry"] - pos["entry"]) / pos["entry"]
                if gain >= TAKE_PROFIT_T1_PCT:
                    trailing_stop = round(pos["high_since_entry"] * (1 - TRAILING_STOP_PCT), 2)
                    if bar["l"] <= trailing_stop:
                        exit_price = trailing_stop if bar["o"] > trailing_stop else bar["o"]
                        reason = "trailing_stop"

            if exit_price:
                cash += exit_price * pos["shares"]
                pnl = (exit_price - pos["entry"]) * pos["shares"]
                trade_log.append({
                    "symbol": sym, "entry_date": pos["entry_date"], "exit_date": date_str,
                    "entry": pos["entry"], "exit": exit_price, "shares": pos["shares"],
                    "pnl": pnl, "reason": reason,
                })
                del positions[sym]

        def mark_to_market():
            return cash + sum(
                positions[s]["shares"] * today_bars[s]["c"] if s in today_bars
                else positions[s]["shares"] * positions[s]["entry"]
                for s in positions
            )

        equity = mark_to_market()

        # 2. Daily loss halt
        pnl_pct = (equity - prev_close_equity) / prev_close_equity if prev_close_equity else 0
        halted = pnl_pct <= -DAILY_LOSS_CAP_PCT
        if halted:
            for sym in list(positions):
                bar = today_bars.get(sym)
                px = bar["c"] if bar else positions[sym]["entry"]
                cash += px * positions[sym]["shares"]
                pnl = (px - positions[sym]["entry"]) * positions[sym]["shares"]
                trade_log.append({
                    "symbol": sym, "entry_date": positions[sym]["entry_date"], "exit_date": date_str,
                    "entry": positions[sym]["entry"], "exit": px, "shares": positions[sym]["shares"],
                    "pnl": pnl, "reason": "daily_halt",
                })
                del positions[sym]
            equity = cash

        # 3. New entries
        trades_today = 0
        if not halted and spy_ok:
            candidates = []
            for sym in SYMBOLS:
                if sym in positions or sym not in today_bars:
                    continue
                dates_sym = data[sym + "__ordered_dates"]
                idx_sym = dates_sym.index(date_str)
                tech = rolling_stats(dates_sym, data[sym], idx_sym)
                if tech["technically_sound"]:
                    candidates.append((sym, tech))
            candidates.sort(key=lambda x: x[1]["volume_ratio"], reverse=True)

            for sym, tech in candidates:
                if trades_today >= MAX_TRADES_PER_DAY:
                    break
                price = tech["price"]
                max_dollars = equity * MAX_POSITION_PCT
                shares = int(max_dollars / price)
                if shares < 1 or shares * price > cash:
                    continue
                stop_pct = STOP_LOSS_HIGH_BETA_PCT if tech["high_beta"] else STOP_LOSS_DEFAULT_PCT
                stop_price = round(price * (1 - stop_pct), 2)
                cash -= shares * price
                positions[sym] = {
                    "entry": price, "shares": shares, "stop_price": stop_price,
                    "high_beta": tech["high_beta"], "high_since_entry": price,
                    "entry_date": date_str,
                }
                trades_today += 1

        equity = mark_to_market()
        equity_curve.append((date_str, equity))
        prev_close_equity = equity

    # Close remaining positions at last available price
    last_date = sim_dates[-1]
    for sym, pos in positions.items():
        bar = today_bars.get(sym) if sym in today_bars else data[sym].get(last_date)
        px = bar["c"] if bar else pos["entry"]
        cash += px * pos["shares"]
        pnl = (px - pos["entry"]) * pos["shares"]
        trade_log.append({
            "symbol": sym, "entry_date": pos["entry_date"], "exit_date": last_date,
            "entry": pos["entry"], "exit": px, "shares": pos["shares"],
            "pnl": pnl, "reason": "sim_end",
        })
    final_equity = cash

    # --- Report ---
    total_return_pct = (final_equity / STARTING_CASH - 1) * 100
    n_trades = len(trade_log)
    wins = [t for t in trade_log if t["pnl"] > 0]
    losses = [t for t in trade_log if t["pnl"] <= 0]
    win_rate = len(wins) / n_trades * 100 if n_trades else 0
    avg_win = statistics.mean([t["pnl"] for t in wins]) if wins else 0
    avg_loss = statistics.mean([t["pnl"] for t in losses]) if losses else 0

    peak = STARTING_CASH
    max_dd = 0
    for _, eq in equity_curve:
        peak = max(peak, eq)
        dd = (eq - peak) / peak
        max_dd = min(max_dd, dd)

    spy_start_px = spy_bars[sim_dates[0]]["c"]
    spy_end_px = spy_bars[sim_dates[-1]]["c"]
    spy_return_pct = (spy_end_px / spy_start_px - 1) * 100

    print("\n" + "=" * 60)
    print(f"BACKTEST RESULTS  ({sim_dates[0]} -> {sim_dates[-1]})")
    print("=" * 60)
    print(f"Starting equity:     ${STARTING_CASH:,.2f}")
    print(f"Final equity:        ${final_equity:,.2f}")
    print(f"Total return:        {total_return_pct:+.2f}%")
    print(f"SPY buy & hold:      {spy_return_pct:+.2f}%")
    print(f"Max drawdown:        {max_dd*100:.2f}%")
    print(f"Trades:              {n_trades}  (win rate {win_rate:.1f}%)")
    print(f"Avg win / avg loss:  ${avg_win:,.2f} / ${avg_loss:,.2f}")
    exits_by_reason = {}
    for t in trade_log:
        exits_by_reason[t["reason"]] = exits_by_reason.get(t["reason"], 0) + 1
    print(f"Exit reasons:        {exits_by_reason}")
    print("=" * 60)

    import csv
    out_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(out_dir, "backtest_equity_curve.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "equity"])
        w.writerows(equity_curve)
    with open(os.path.join(out_dir, "backtest_trades.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["symbol", "entry_date", "exit_date", "entry", "exit", "shares", "pnl", "reason"])
        w.writeheader()
        w.writerows(trade_log)
    print(f"\nWrote {out_dir}\\backtest_equity_curve.csv and backtest_trades.csv")


if __name__ == "__main__":
    main()
