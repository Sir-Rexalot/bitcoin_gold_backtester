# ============================================================
# Streamlit Portfolio Backtest App with BTC and GLD Allocation (2016–2025)
# Author: James Birrell
# Description: Streamlit GUI version includes sliders for BTC/GLD allocations,
#              control over funding source (equities/fixed income),
#              interactive Plotly chart, Sortino Ratio, allocation tables,
#              and Excel export functionality.
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objs as go

st.set_page_config(page_title="Portfolio Backtest", layout="wide")

# ---------------------------
# Load Data
# ---------------------------
tickers = ['SPY', 'AGG', 'GLD', 'BTC-USD']
start_date = '2016-01-01'
end_date = '2025-07-01'
initial_value = 100

@st.cache_data(show_spinner=False)
def load_data():
    data_raw = yf.download(tickers, start=start_date, end=end_date, group_by='ticker', auto_adjust=False)
    data = pd.concat([data_raw[ticker]['Adj Close'] for ticker in tickers], axis=1)
    data.columns = tickers
    data = data.dropna()
    returns = data.pct_change().dropna()
    return data, returns

data, returns = load_data()

# ---------------------------
# Sidebar Inputs
# ---------------------------
st.sidebar.title("Portfolio Configuration")
include_baseline = st.sidebar.checkbox("Include 60/40 Portfolio", value=True)

st.sidebar.subheader("Portfolio 1")
btc1 = st.sidebar.slider("BTC %", 0.0, 0.2, 0.02, step=0.01)
btc_eq1 = st.sidebar.slider("BTC from Equities %", 0.0, 1.0, 0.5, step=0.1)
gld1 = st.sidebar.slider("GLD %", 0.0, 0.2, 0.0, step=0.01)
gld_eq1 = st.sidebar.slider("GLD from Equities %", 0.0, 1.0, 0.5, step=0.1)

st.sidebar.subheader("Portfolio 2")
btc2 = st.sidebar.slider("BTC % (P2)", 0.0, 0.2, 0.05, step=0.01)
btc_eq2 = st.sidebar.slider("BTC from Equities % (P2)", 0.0, 1.0, 0.5, step=0.1)
gld2 = st.sidebar.slider("GLD % (P2)", 0.0, 0.2, 0.05, step=0.01)
gld_eq2 = st.sidebar.slider("GLD from Equities % (P2)", 0.0, 1.0, 0.5, step=0.1)

# ---------------------------
# Portfolio Weight Generator
# ---------------------------
def build_weights(base_weights, btc, btc_eq, gld, gld_eq):
    weights = base_weights.copy()
    weights['SPY'] -= btc * btc_eq + gld * gld_eq
    weights['AGG'] -= btc * (1 - btc_eq) + gld * (1 - gld_eq)
    weights['BTC-USD'] = btc
    weights['GLD'] = gld
    return weights

base_weights = {'SPY': 0.60, 'AGG': 0.40, 'GLD': 0.0, 'BTC-USD': 0.0}
portfolios = {}
if include_baseline:
    portfolios['60/40'] = base_weights.copy()
portfolios[f"Portfolio 1: BTC{int(btc1*100)} GLD{int(gld1*100)}"] = build_weights(base_weights, btc1, btc_eq1, gld1, gld_eq1)
portfolios[f"Portfolio 2: BTC{int(btc2*100)} GLD{int(gld2*100)}"] = build_weights(base_weights, btc2, btc_eq2, gld2, gld_eq2)

alloc_df = pd.DataFrame(portfolios).T

# ---------------------------
# Compute Portfolio Values
# ---------------------------
def compute_portfolio(weights, returns):
    w = np.array([weights[t] for t in returns.columns])
    daily_returns = returns @ w
    value = (1 + daily_returns).cumprod() * initial_value
    return value, daily_returns

port_vals, port_rets = {}, {}
for name, w in portfolios.items():
    v, r = compute_portfolio(w, returns)
    port_vals[name] = v
    port_rets[name] = r

# ---------------------------
# Performance Summary
# ---------------------------
def performance_summary(pval, pret):
    total = pval.iloc[-1] / pval.iloc[0] - 1
    annual = (1 + total) ** (252 / len(pval)) - 1
    maxdd = ((pval / pval.cummax()) - 1).min()
    vol = pret.std() * np.sqrt(252)
    sharpe = annual / vol if vol != 0 else np.nan
    downside = pret[pret < 0].std() * np.sqrt(252)
    sortino = annual / downside if downside != 0 else np.nan
    return total, annual, maxdd, vol, sharpe, sortino

summary_df = pd.DataFrame(
    [performance_summary(port_vals[n], port_rets[n]) for n in portfolios],
    columns=['Total Return', 'Annual Return', 'Max Drawdown', 'Volatility', 'Sharpe Ratio', 'Sortino Ratio'],
    index=portfolios.keys()
).round(4)

# ---------------------------
# Display Tables and Chart
# ---------------------------
col1, col2 = st.columns([1.5, 1])

with col1:
    st.plotly_chart(go.Figure([
        go.Scatter(x=series.index, y=series, name=name,
                    line=dict(width=4 if name == summary_df['Total Return'].idxmax() else 2))
        for name, series in port_vals.items()
    ]).update_layout(
        title='Portfolio Value Over Time',
        xaxis_title='Date', yaxis_title='Value (Indexed to 100)',
        hovermode='x unified', height=600
    ), use_container_width=True)

with col2:
    st.subheader("Performance Summary")
    st.dataframe(summary_df)

st.subheader("Asset Allocations")
st.dataframe(alloc_df.round(3))

# ---------------------------
# Export Option
# ---------------------------
with st.expander("Export to Excel"):
    if st.button("Download Excel File"):
        with pd.ExcelWriter("portfolio_backtest_results.xlsx") as writer:
            data.to_excel(writer, sheet_name='Price Data')
            returns.to_excel(writer, sheet_name='Daily Returns')
            pd.DataFrame(port_vals).to_excel(writer, sheet_name='Portfolio Values')
            summary_df.to_excel(writer, sheet_name='Performance Summary')
            alloc_df.to_excel(writer, sheet_name='Asset Allocations')
        st.success("Exported as portfolio_backtest_results.xlsx")
