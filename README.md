# Bitcoin & Gold Allocation Portfolio Backtester

This project allows users to simulate historical backtests of multi-asset portfolios with user-defined allocations to Bitcoin (BTC) and Gold (GLD), layered on top of a traditional 60/40 portfolio (SPY/AGG). It includes a command-line version and a Streamlit GUI version.

## Features

- User-defined BTC and GLD allocations
- Control over whether allocations are drawn from equities or fixed income
- Optional inclusion of standard 60/40 benchmark
- Performance summary with Sharpe and Sortino ratios
- Interactive Plotly visualization with annotations
- Export of results to Excel

## Requirements

Install required libraries using:

```bash
pip install -r requirements.txt
```

## Running the Script

```bash
python bitcoin_gold_backtester.py
```

## Streamlit Version (Optional)

If you have the Streamlit version:

```bash
streamlit run bitcoin_gold_backtester.py
```

## Output

- Excel file: `portfolio_backtest_results.xlsx`
- Plotly interactive chart
- Terminal summary of portfolio performance and allocations

## Author

James Birrell

## License

MIT License
