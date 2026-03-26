import streamlit as st
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import ollama

from src.tester import test_hypothesis
from src.hypothesis import Hypothesis

st.set_page_config(layout="wide")

st.title("Market Research Tool")

st.write("Ask about a market. The system will find a pattern and show how it performs over time.")

user_input = st.text_input("Your question")
run = st.button("Run")


# ---------------- PARSE ----------------
def parse_input(text):
    prompt = f"""
    Extract:
    1. ticker
    2. strategy: mean_reversion or momentum

    Input: {text}

    Output:
    ticker: ...
    strategy: ...
    """

    try:
        res = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )

        out = res["message"]["content"].lower()

        ticker = "EURUSD=X"
        strategy = "mean_reversion"

        for line in out.split("\n"):
            if "ticker" in line:
                ticker = line.split(":")[1].strip().upper()
            if "strategy" in line:
                strategy = line.split(":")[1].strip()

        if ticker == "EURUSD":
            ticker = "EURUSD=X"

        return ticker, strategy

    except:
        return "EURUSD=X", "mean_reversion"


# ---------------- DATA ----------------
@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, period="10y")

    prices = data["Close"]
    if hasattr(prices, "columns"):
        prices = prices.iloc[:, 0]

    returns = np.log(prices / prices.shift(1)).dropna()

    return prices, returns


# ---------------- HYPOTHESES ----------------
def generate_hypotheses(strategy):
    ideas = []

    for lb in [1, 3, 5]:

        if strategy == "mean_reversion":
            for t in [-0.01, -0.02, -0.03]:
                ideas.append(Hypothesis(t, lb, "mean_reversion"))

        else:
            for t in [0.01, 0.02, 0.03]:
                ideas.append(Hypothesis(t, lb, "momentum"))

    return ideas


# ---------------- BACKTEST ----------------
def backtest_equity(returns, condition):

    future_returns = returns.shift(-1)
    signal_returns = future_returns[condition].fillna(0)

    equity = (1 + signal_returns).cumprod()

    # align with full index
    equity_full = np.ones(len(returns))
    equity_full[-len(equity):] = equity

    return equity_full


# ---------------- RUN ----------------
if run:

    if not user_input:
        st.stop()

    ticker, strategy = parse_input(user_input)

    st.write(f"Asset: {ticker}")
    st.write(f"Strategy: {strategy}")

    prices, returns = load_data(ticker)

    st.markdown("## Price")
    st.line_chart(prices.tail(200))

    # ---------------- FIND BEST ----------------
    hypotheses = generate_hypotheses(strategy)

    results = []

    for h in hypotheses:
        res = test_hypothesis(returns, h)
        if res:
            results.append((h, res))

    results = sorted(results, key=lambda x: x[1]["sharpe"], reverse=True)

    h, res = results[0]

    rolling = returns.rolling(h.lookback).sum()

    if strategy == "momentum":
        condition = rolling > abs(h.threshold)
    else:
        condition = rolling < h.threshold

    # ---------------- EQUITY ----------------
    equity = backtest_equity(returns, condition)

    buy_hold = (1 + returns.fillna(0)).cumprod()

    # ---------------- PLOT ----------------
    st.markdown("## Strategy Performance (Equity Curve)")

    fig, ax = plt.subplots()

    ax.plot(equity, label="Strategy")
    ax.plot(buy_hold, label="Buy & Hold", linestyle="--")

    ax.legend()

    st.pyplot(fig)

    # ---------------- INTERPRETATION ----------------
    st.markdown("## What this means")

    final_return = equity[-1]

    st.write(f"""
If you followed this strategy over time:

- Your capital would grow to **{round(final_return,2)}x**

The blue line shows strategy performance.
The dashed line shows simply holding the asset.

This helps you compare whether the strategy actually adds value.
""")

    st.warning("Backtests are based on historical data and may not reflect future performance.")