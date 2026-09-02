# Daily Market Context
Date: 2026-09-02 (pre-market research run — automated firing)
Data reflects the 2026-09-01 close and pre-market for the 2026-09-02 session.

---

## SPY Trend vs 5-Day Moving Average

**Determination: SPY is BELOW its 5-day moving average (second consecutive session).**

- S&P 500 close 2026-09-01: ~7,631.47 (-0.71%); a second straight lower close.
- The index was ~7,676 at the late-August highs; two risk-off sessions (08-31 and 09-01) have
  pulled it below its rising 5-day MA.
- S&P 50-day MA: ~7,567 — index still ABOVE (intermediate trend intact).
- S&P 200-day MA: well below — long-term structure still bullish.
- Breadth still deteriorating: well under 50% of S&P 500 names above their 50-day MA.
- Interpretation: regular stock entries are BLOCKED. SH (inverse SPY) is now IN SCOPE and, at a
  score of 62/100, above the 60 threshold — see below.

**Implication for strategy**: Regular stock entries BLOCKED. SH entry ELIGIBLE (borderline).

---

## VIX Level

**Current VIX: ~16.34 (2026-09-01 close, +9.5% on the day) | still historically low**

- VIX < 28 threshold: YES — comfortably below.
- VIX has risen two days running on the Iran/oil headlines but is not yet pricing sustained
  fear (no move toward the low 20s). This is the main reason the SH call is only borderline.

---

## TRADE_OK Determination

**TRADE_OK (regular stocks): no** — SPY below its 5-day MA.
**SH (inverse SPY): ELIGIBLE** — score 62 >= 60, VIX < 28, count 0/3, halt false.

Criteria check:
- SPY above 5-day MA: NO (second consecutive close below) → regular entries blocked
- VIX < 28: YES (~16.3)
- daily_loss_halt: false (confirmed in weekly_trade_counter.md)
- Weekly trade count: 0/3 — room for entries
- SH alternative: score 62/100, above the 60 threshold → market-open routine should evaluate
  an SH entry (3% max position, 5% stop, exit on SPY reclaiming its 5-day MA)

---

## Sector Context & Market Regime Notes

**Current regime: Risk-off, day 2 — escalating geopolitical shock. Fresh U.S. strikes on Iran,
Iranian retaliatory strikes on U.S. bases, and two oil tankers reported hitting naval mines in
the Strait of Hormuz. Brent ~$95, WTI ~$90; Treasury yields at new highs; Fed-tightening worry
intensifying. Weakest seasonal month. Mega-cap AI earnings remain fundamentally strong, so this
still reads as a sentiment/geopolitical drawdown rather than a fundamental break — but it has
now run two sessions and is escalating rather than fading.**

### Sector Rotation
- **Energy**: outperforming on the crude spike — the clear relative winner.
- **Semiconductors / AI infrastructure**: under pressure. NVDA ~$217 (weakest since May),
  momentum broken; AMD's "Helios" AI rack (a direct NVDA competitor) is expected to ship in
  September, and BMO just initiated AMD at Outperform (avg PT ~$596). Semi-tariff headlines
  add overhang for the whole group.
- **Cloud / Mega-cap**: AMZN the relative-strength leader (only Mag7 beating S&P YTD; AWS
  +36.7%). META analysts' favored name (median PT ~$750–755, Strong Buy). MSFT strong
  fundamentally (Azure >$100B ARR) but flagged as least hyperscaler upside (median PT ~$555).
  GOOGL weighed by the Jeff Dean AI-talent departure and antitrust overhang.
- **AI capex**: AMZN + GOOGL headlined at a combined ~$420B AI-infrastructure spend — a growing
  investor concern in a risk-off tape.
- **Crypto / Fintech**: COIN pressured in the risk-off move; SOFI a direct loser from yields at
  new highs.
- **Consumer Discretionary / EV**: TSLA ~$363, rangebound, no catalyst. RIVN improving but
  sub-threshold and speculative.

### Macro Context — Next 48 Hours
| Event | Date/Time | Market Impact |
|-------|-----------|---------------|
| U.S.-Iran / Strait of Hormuz escalation | ongoing, worsening | HIGH — primary swing factor; drives oil and yields |
| Brent crude ~$95 / WTI ~$90 | ongoing | HIGH — feeds inflation / Fed-tightening worry |
| Treasury yields at new highs | ongoing | MEDIUM-HIGH — pressures high-multiple / rate-sensitive names |
| September seasonality | month | LOW-MEDIUM — historically the weakest month (avg ~-1.2%) |

### Key Risks to Monitor (Next 48 Hours)
1. Further Iran/Hormuz escalation → another oil leg up → deeper equity drawdown.
2. Yield backup continues — direct hit to SOFI, COIN, and the high-multiple AI names.
3. Semiconductor-tariff headlines hitting NVDA/AMD/SMCI.
4. **De-escalation / ceasefire headline → violent SPY snap-back that would stop out an SH
   position.** This is the specific risk that keeps the SH call borderline.
5. Breadth keeps narrowing — a small group of mega-caps holding the index up.

### Inverse ETF (SH) Status
SH score: 62/100 — ABOVE the 60 threshold (up from 52 on 09-01). SPY has now posted two
consecutive lower closes below its 5-day MA on an escalating U.S.-Iran military conflict with
oil at ~$95. That is a confirmed short-term downtrend plus a hard catalyst. The one hold-back:
VIX (~16.3) is not yet showing genuine fear, and any de-escalation headline would snap SPY
back hard. Market-open routine: evaluate SH entry at 3% max position with a 5% stop; exit
immediately when SPY reclaims its 5-day MA.

---

## Summary for Market-Open Routine

| Parameter | Value | Pass/Fail |
|-----------|-------|-----------|
| SPY vs 5-day MA | Below (2nd consecutive close) | FAIL (regular entries blocked) |
| VIX | ~16.3 | PASS (< 28) |
| daily_loss_halt | false | PASS |
| Weekly trade count | 0/3 | PASS |
| TRADE_OK (regular stocks) | no | — |
| SH eligible | YES (score 62/100) — borderline | EVALUATE (3% size, 5% stop) |
| Top regular candidate (if allowed) | AMD (78/100) — extended, but Helios ships Sept | Blocked |
