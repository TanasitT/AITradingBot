# Research Cache
Last Updated: 2026-09-02 (pre-market research run, automated firing)
Data sourced via web search; reflects the 2026-09-01 close and pre-market for the 2026-09-02 session.

REGIME: risk-OFF, day 2. The U.S.-Iran conflict around the Strait of Hormuz ESCALATED — fresh
U.S. strikes on Iran, Iranian retaliatory strikes on U.S. bases, and two oil tankers reported
striking naval mines in the Strait. Brent crude ~$95, WTI ~$90; Treasury yields climbing;
Fed-tightening worry intensifying. S&P 500 closed 2026-09-01 at ~7,631 (-0.71%), a SECOND
consecutive lower close; VIX 16.34 (+9.5%). Sept 2 futures lower again. September seasonality
(weakest month, avg ~-1.2%) adds to the drag. S&P still above its 50-day (~7,567) and 200-day
MAs — intermediate/long-term structure intact — but now clearly below its 5-day MA.

NOTE: weekly_trade_counter.md shows trades_this_week = 0/3 (reset 2026-09-01 by the eod-friday
run). daily_loss_halt = false. Entries are permitted by count, but regular stock entries are
BLOCKED by the SPY-below-5-day-MA rule. SH (inverse SPY) is now in scope — see below.

CAVEAT: NVDA (22sh), AMZN (19sh), AMD (10sh) entered 2026-09-01 remain OPEN. Prior EOD runs
flagged them for force-close (no strong overnight thesis) but could not execute. Not a research
input — noted for the market-open / monitor routines.

---

## Scores — 2026-09-02

| Ticker | Score | Thesis (one line) | Key Catalyst / Risk | Volume Note |
|--------|-------|-------------------|---------------------|-------------|
| AAPL   | 60/100 | Record June quarter but light forward guide; no fresh catalyst; relatively defensive into risk-off | Risk: rising yields + oil shock pressure multiples; no catalyst | Volume near 30-day avg |
| MSFT   | 66/100 | Azure >$100B ARR, +43% YoY; Strong Buy consensus; AI-cloud thesis intact | Risk: flagged as least-upside of the Mag7 hyperscalers (median PT ~$555); risk-off tape; sector capex worry | Volume normal |
| NVDA   | 64/100 | Q2 blowout; MediaTek $3.5B NVLink Fusion deal; div ex-date Sep 10; consensus PT ~$326 (Strong Buy) | Risk: momentum broken (~$217, lowest since May); AMD "Helios" rack ships Sept = direct competitive headline; hedge-fund exit chatter; semi-tariff overhang | Volume elevated, choppy |
| TSLA   | 48/100 | FSD/Robotaxi medium-term narrative only; ~$363, mid 52-wk range | Risk: no near-term catalyst; EV competition; weak momentum in risk-off tape | Volume normal |
| AMZN   | 72/100 | Only Mag7 name beating S&P YTD; AWS +36.7%; >$3T cap; relative-strength leader | Risk: heavy AI capex (part of $420B AMZN+GOOGL infra spend headline); rate-sensitive into a yield backup; already held (open position) | Volume elevated; relative strength |
| META   | 73/100 | Ad revenue +27% YoY; analysts' most-favored hyperscaler, median PT ~$750–755, Strong Buy; +31% implied upside | Risk: elevated capex; risk-off tape; legal/antitrust overhang | Volume moderate |
| GOOGL  | 60/100 | Strong Q2 (Search+Cloud); AI-infra beneficiary; median PT ~$426 | Risk: Jeff Dean departure / AI-talent overhang; capex guide $195–205B; antitrust; risk-off | Volume elevated |
| AMD    | 78/100 | BMO initiated Outperform; "Helios" AI rack (direct NVDA competitor) expected to ship September = near-term catalyst; avg PT ~$596; +41% Q3 rev guide; +140%+ YTD | Risk: very extended (~$460–470); MI450 schedule chatter; post-run pullback risk in a risk-off tape; already held (open position) | Volume above average |
| SMCI   | 68/100 | FY26 rev $39.1B; Cisco partnership; AI liquid-cooled rack demand | Risk: export-violation headlines; accounting/audit history; sharp run-up; high beta into risk-off | Volume strongly elevated |
| PLTR   | 72/100 | Q2 rev +93% YoY; raised 2026 guide ~$8.15B; UBS Buy, PT raised to $220; US commercial + defense AI momentum | Risk: premium valuation priced for perfection; profit-taking risk in risk-off tape | Volume above average |
| SOFI   | 46/100 | Record Q2 adjusted revenue (+40%); fintech recovering | Risk: rate-sensitive and yields at NEW highs — direct headwind; Hold consensus | Volume moderate |
| RIVN   | 46/100 | First positive consolidated gross profit Q2; R2 deliveries started | Risk: ongoing net losses, cash burn; weak tape for speculative names | Volume normal |
| COIN   | 56/100 | Goldman PT $196; regulatory-clarity thesis intact | Risk: crypto sells off in risk-off / oil-shock tape; no fresh catalyst; BTC volatility | Volume elevated |
| SPY    | 50/100 | Above 50d/200d MAs; but below 5-day MA on a second consecutive down day | Risk: Iran/oil shock escalating; yields at new highs; weak September seasonality | Volume elevated on down days |
| QQQ    | 52/100 | Long-term uptrend intact; mega-cap AI earnings strong | Risk: tech led the decline; rate-sensitive to the yield backup; below short-term MAs | Volume moderate |
| SH     | 62/100 | Inverse SPY — SPY now below its 5-day MA for a SECOND consecutive session on an ESCALATING U.S.-Iran military conflict; oil ~$95 Brent; yields rising; September seasonality | Above the 60 threshold: 2-day confirmed short-term downtrend + hard geopolitical catalyst. BUT VIX only ~16 (not yet low-20s fear) and a de-escalation headline would snap SPY back violently. Borderline. Max 3% position, 5% stop, exit when SPY reclaims 5-day MA. | Volume irrelevant |

---

## Tier Summary

### Tier 1 — Score >= 70
- AMD: 78/100 (blocked for regular entry — SPY below 5-day MA)
- META: 73/100 (blocked)
- AMZN: 72/100 (blocked)
- PLTR: 72/100 (blocked)

### Tier 2 — Score 60–69
- SMCI: 68/100
- MSFT: 66/100
- NVDA: 64/100
- SH: 62/100 (inverse ETF — ELIGIBLE for bearish entry, see below)
- AAPL: 60/100
- GOOGL: 60/100

### Tier 3 — Score < 60 (avoid)
- COIN: 56/100
- QQQ: 52/100 (ETF)
- SPY: 50/100 (ETF)
- TSLA: 48/100
- SOFI: 46/100
- RIVN: 46/100

---

## Top 3 Candidates (for market-open routine reference)
1. AMD — 78/100 — BMO Outperform initiation, Helios rack ships September (near-term catalyst).
   Blocked for regular entry (SPY below 5-day MA); very extended.
2. META — 73/100 — analysts' most-favored hyperscaler, PT ~$750–755, Strong Buy. Blocked.
3. AMZN — 72/100 — relative-strength leader, only Mag7 beating S&P YTD. Blocked; already held.

**Special case — SH (inverse SPY): 62/100 — ELIGIBLE.** SPY below its 5-day MA for a second
straight session on an escalating U.S.-Iran conflict; VIX < 28; weekly count 0/3;
daily_loss_halt false. Market-open routine should evaluate an SH entry (max 3% position, 5%
stop, exit when SPY reclaims its 5-day MA). Borderline conviction — VIX is not yet confirming
fear and headline reversal risk is high.

**Market-open routine notes**:
- TRADE_OK (regular stocks) = NO. SPY below its 5-day MA → regular stock entries BLOCKED.
- SH = ELIGIBLE (score 62 >= 60, VIX ~16 < 28, count 0/3, halt false). Borderline — size at
  3% max, place the 5% stop, and be ready to exit fast on any SPY reclaim of the 5-day MA or
  Iran de-escalation headline.
- daily_loss_halt = false.
