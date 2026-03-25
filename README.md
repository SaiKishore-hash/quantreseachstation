# Autonomous Quantitative Research Workstation
**A Multi-Agent Framework for Financial Hypothesis Discovery**

## Overview
This project implements an autonomous quantitative research desk designed to bridge the gap between qualitative market intuition and statistical validation. Utilizing a Local LLM (Llama 3 via Ollama), the system acts as a Senior Quant Analyst to generate, audit, and validate trading hypotheses for Equities (AAPL) and Forex (EUR/USD).

## Core Architecture
The system follows a three-stage pipeline:
1. **Hypothesis Generation**: The Agent identifies technical anomalies and market inefficiencies.
2. **Backtest Simulation**: Mathematical logic is applied against 24 months of historical data.
3. **Statistical Audit**: Strategies are accepted or rejected based on a Sharpe Ratio threshold of 1.4.

## Technical Stack
- **Engine**: Python 3.10+
- **Interface**: Streamlit (Institutional UI Design)
- **Intelligence**: Ollama (Llama 3)
- **Data Source**: Yahoo Finance API

## Setup Instructions
1. Install [Ollama](https://ollama.com/) and run `ollama run llama3`.
2. Clone this repository.
3. Install dependencies: `pip install -r requirements.txt`.
4. Launch the station: `streamlit run app.py`.