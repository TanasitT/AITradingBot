import requests
from config import PERPLEXITY_API_KEY

API_URL = "https://api.perplexity.ai/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
    "Content-Type": "application/json",
}


def _query(system_prompt, user_prompt, model="sonar-pro"):
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "return_citations": True,
        "search_recency_filter": "day",
    }
    r = requests.post(API_URL, json=body, headers=HEADERS, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def research_ticker(symbol):
    system = (
        "You are a financial research analyst. Be factual, cite specific numbers, "
        "and focus only on information from the last 48 hours. Do not speculate."
    )
    user = f"""Research {symbol} stock and return a structured analysis covering:

1. CATALYST (0-25 pts): Any earnings, guidance changes, FDA decisions, M&A, macro events?
2. SENTIMENT (0-25 pts): Analyst upgrades/downgrades, news tone, social momentum?
3. TECHNICAL (0-25 pts): Price vs 50d/200d MA, RSI level, volume vs 30d average?
4. MARKET CONTEXT (0-25 pts): Sector strength, SPY trend, VIX environment?

End your response with exactly this line:
SCORE: [total]/100

Be specific with numbers. If no catalyst exists, say so clearly."""
    return _query(system, user)


def get_market_context():
    system = "You are a macro market analyst. Be brief and factual."
    user = """Give me current market context in 5 bullet points:
1. SPY trend (above/below 5-day MA?) and today's direction
2. VIX level and what it signals
3. Top performing sector today
4. Any major macro events in the next 48 hours (Fed, CPI, earnings)
5. Overall risk-on or risk-off environment?

End with: TRADE_OK: yes or TRADE_OK: no"""
    return _query(system, user)


def check_negative_catalyst(symbol, thesis):
    system = "You are a risk analyst checking if a trade thesis has been invalidated."
    user = f"""Original thesis for {symbol}: {thesis}

Search for any news in the last 6 hours that would INVALIDATE this thesis.
Examples: earnings miss, guidance cut, regulatory block, CEO scandal, sector selloff.

Answer with:
THESIS_INTACT: yes or THESIS_INTACT: no
REASON: [one sentence]"""
    return _query(system, user)
