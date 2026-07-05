Append a reasoning entry to memory/reasoning.md.

This skill is called by other skills automatically, and can also be called manually.

Steps:
1. Take the text passed as the argument to this command as the journal entry.
   - If called manually with no argument (just `/journal`), ask the user: "What would you like to log?"
   - If called by another skill, use the message that skill passed as the argument.
2. Format the entry as:
   ```
   ## [YYYY-MM-DD HH:MM ET]
   [entry text]
   ---
   ```
3. Append this entry to memory/reasoning.md — NEVER overwrite the file, only append.
4. Commit and push memory/reasoning.md to GitHub with message: `auto: journal entry | [date] ET`

Examples of entries the bot writes automatically:
- "Research complete. 15 tickers scanned. Top candidates: NVDA(84), MSFT(76). Market TRADE_OK=yes, VIX=14.2."
- "Bought 3 shares of NVDA @ $142.50. Score: 84/100. Stop: $135.38. Thesis: Earnings beat 12%, data center guidance raised."
- "Skipped TSLA. Score 52 (below 70 threshold). Volume only 1.3x avg."
- "HALT triggered. Portfolio down -2.1% by 11:30 AM. Daily loss cap hit. All routines suspended."
- "EOD report sent to jankla2010@gmail.com."

Examples of entries you can write manually:
- `/journal I want to pause trading this week — markets feel uncertain`
- `/journal Remove RIVN from watchlist — thesis has been wrong 3 weeks in a row`
- `/journal Feeling good about NVDA earnings next week, keep an eye on it`
