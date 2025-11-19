# Bitcoin & Gold Allocation Portfolio Backtester

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bitcoingold.streamlit.app)

This Streamlit web app allows users to run historical backtests of multi-asset portfolios that combine traditional 60/40 allocations with custom Bitcoin (BTC) and Gold (GLD) exposures.

---

## 📊 Features

- Adjustable BTC and GLD allocations
- Slider control over equity/fixed income funding source
- Benchmark comparison with traditional 60/40 portfolio
- Performance metrics: Total Return, Sharpe and Sortino ratios
- Interactive Plotly chart (dark mode compatible)
- Asset allocation tables and Excel export
- Deployed to Streamlit Cloud – no local install required

---

## 🚀 Live App

👉 [Launch the app now](https://bitcoingold.streamlit.app)

---

## ⚙️ Requirements (for local use)

If you'd like to run this locally:

```bash
pip install -r requirements.txt
streamlit run bitcoin_gold_bt.py
```

---

## 🪄 How to Use / Customize

1. Adjust sliders in the sidebar to allocate BTC and GLD.
2. Choose whether the funding comes from equities or fixed income.
3. View the impact on performance, drawdowns, and allocation.
4. Download the results to Excel.

---

## 🌐 For Contributors

You can fork and deploy your own version:

```bash
# Fork the repo on GitHub
https://github.com/Sir-Rexalot/bitcoin_gold_backtester

# Clone it to your PC
$ git clone https://github.com/YOUR_USERNAME/bitcoin_gold_backtester
$ cd bitcoin_gold_backtester
$ pip install -r requirements.txt
$ streamlit run bitcoin_gold_bt.py
```

To deploy to the cloud:
- Push to your GitHub account
- Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
- Connect your repo and set `bitcoin_gold_bt.py` as your main file

---

Made with ❤️ by James Birrell

