# Quantitative Research Workstation v4.1 (Cloud Edition)
**An Autonomous Multi-Agent Framework for Institutional Hypothesis Discovery**

## Overview
This workstation is a professional-grade quantitative tool designed to automate the discovery and statistical validation of trading hypotheses. By leveraging the **Llama-3.3-70B** model via the **Groq Inference Engine**, the system bridges the gap between raw market data and actionable investment theses.

The application is optimized for high-stakes environments, focusing on two primary asset classes: **Equities (AAPL)** and **Forex (EUR/USD)**.

## Core Architecture
The system operates through a high-performance "Agentic" pipeline:
1.  **Market Data Intake**: Pulls 24 months of adjusted historical price action via `yfinance`.
2.  **Autonomous Thesis Generation**: A Senior Quant Agent (Llama-3.3) identifies technical anomalies and structural inefficiencies.
3.  **Statistical Audit**: Every hypothesis is subjected to a variance-based backtest simulation to calculate the **Annualized Sharpe Ratio**.
4.  **Executive Verdict**: Strategies are categorized as **ACCEPTED** (Sharpe > 1.5) or **REJECTED** based on institutional risk thresholds.

## Key Features
- **Cloud-Native Intelligence**: Powered by Groq for sub-second inference speeds.
- **Zero-Friction UI**: Bloomberg-inspired minimalist interface designed for professional clarity.
- **Secure Environment**: Implements strict `secrets` management for API security, ensuring no sensitive credentials leak to public repositories.

## Technical Stack
- **Language**: Python 3.10+
- **Inference**: Groq Cloud API (Llama-3.3-70B-Versatile)
- **Framework**: Streamlit (Center-Aligned Custom CSS)
- **Data Engine**: Pandas, NumPy, YFinance

## Installation & Setup
1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/YourUsername/YourRepoName.git](https://github.com/YourUsername/YourRepoName.git)
    cd YourRepoName
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure API Key**:
    - **Local**: Create a `.env` file with `GROQ_API_KEY=your_key_here`.
    - **Cloud**: Add `GROQ_API_KEY` to your Streamlit Cloud "Secrets" manager.
4.  **Launch Station**:
    ```bash
    streamlit run app.py
    ```

---
**Project Status**: Production Ready | PhD Research Portfolio Piece