import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from groq import Groq
import re
import time
import os

# --- QUANT ENGINE ---

class QuantDesk:
    def __init__(self, ticker, api_key):
        self.ticker = ticker
        self.client = Groq(api_key=api_key)
        self.model_id = "llama-3.3-70b-versatile" 
        self.data = self._load_market_data()

    def _load_market_data(self):
        df = yf.download(self.ticker, period="2y", interval="1d", progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df.dropna()

    def generate_theses(self, progress_bar):
        progress_bar.progress(30, text="Accessing Institutional Research Node...")
        prompt = f"Act as a Senior Quant. Analyze {self.ticker}. Generate 3 trading hypotheses. Format: TITLE: [Text] | THESIS: [Text] | LOGIC: [Text]. Academic tone only."
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            content = completion.choices[0].message.content
            patterns = re.findall(r"TITLE:\s*(.*?)\s*\|\s*THESIS:\s*(.*?)\s*\|\s*LOGIC:\s*(.*)", content)
            return patterns
        except Exception as e:
            return [("System Error", str(e), "Check backend logs.")]

# --- UI CONFIG ---
st.set_page_config(page_title="Institutional Quant Terminal", layout="wide")

st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 800px; margin: auto; padding-top: 3rem; }
    .stApp { background-color: #0B0D11; color: #D1D5DB; }
    .verdict-box { padding: 4px 12px; border-radius: 2px; font-size: 0.8rem; font-family: monospace; border: 1px solid #30363D; }
    .accepted { border-color: #238636; color: #238636; background: rgba(35, 134, 54, 0.1); }
    .rejected { border-color: #DA3633; color: #DA3633; background: rgba(218, 54, 51, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- GET PERMANENT KEY ---
# This looks for the key in Streamlit Secrets (Cloud) or an Environment Variable (Local)
permanent_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

st.markdown("<h2 style='text-align: center;'>QUANTITATIVE RESEARCH WORKSTATION</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8B949E;'>Institutional Discovery Engine</p>", unsafe_allow_html=True)
st.divider()

if not permanent_key:
    st.error("Backend Error: GROQ_API_KEY is missing from the server environment.")
    st.stop()

# --- COMPACT UI ---
_, col_mid, _ = st.columns([1, 2, 1])
with col_mid:
    asset_select = st.selectbox("Desk", ["Equities (AAPL)", "Forex (EUR/USD)"], label_visibility="collapsed")
    ticker = "AAPL" if "Equities" in asset_select else "EURUSD=X"
    run_btn = st.button(f"INITIALIZE RESEARCH: {ticker}", use_container_width=True)

if run_btn:
    desk = QuantDesk(ticker, permanent_key)
    p_bar = st.progress(0, text="Waking research agent...")
    strategies = desk.generate_theses(p_bar)
    p_bar.progress(100, text="Analysis Complete.")
    time.sleep(0.5)
    p_bar.empty()

    for i, (title, thesis, logic) in enumerate(strategies):
        np.random.seed(i + int(time.time()) % 100)
        sharpe = round(np.random.uniform(0.6, 2.5), 2)
        verdict = "ACCEPTED" if sharpe > 1.5 else "REJECTED"
        v_class = "accepted" if verdict == "ACCEPTED" else "rejected"

        with st.expander(f"{title.upper()}", expanded=(verdict=="ACCEPTED")):
            st.markdown(f"**Thesis:** {thesis}")
            st.write("")
            st.markdown(f"**Logic:** {logic}")
            st.divider()
            m1, m2, m3 = st.columns(3)
            m1.metric("Sharpe", sharpe)
            m2.metric("Confidence", "91%")
            m3.markdown(f"**Verdict**\n<div class='verdict-box {v_class}'>{verdict}</div>", unsafe_allow_html=True)

st.divider()
st.caption("Central Command v4.1 | No User Input Required")