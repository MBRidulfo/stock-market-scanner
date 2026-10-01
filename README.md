# Stock Market Scanner & Backtester

An experimental Python project for scanning stocks for RSI/volume signals, backtesting the strategy, and brute-force testing strategy parameters.

## What it does

- Fetches historical OHLCV market data with `yfinance`
- Calculates RSI using Wilder-style smoothing
- Detects unusual volume activity
- Logs stocks meeting an RSI + volume-spike rule
- Backtests the rule with stop-loss, take-profit, and holding-period parameters
- Tests parameter combinations in parallel
- Can build a watchlist from Yahoo Finance most-active stocks

## Project structure

- `scanner.py` — scans the current watchlist and logs signals
- `data_fetcher.py` — downloads OHLCV data
- `rsi_calculator.py` — calculates RSI
- `volume_analyzer.py` — detects volume spikes
- `watchlist.py` — loads and normalizes ticker CSVs
- `backtester.py` — shared backtesting logic
- `run_backtest.py` — runs the default backtest across the watchlist
- `analyze_backtest.py` — summarizes saved backtest results
- `optimize_strategy.py` — brute-force parameter testing
- `generate_active_watchlist.py` — creates a Yahoo most-active watchlist

## Requirements
- Python 3.x
- Internet connection for market data
- Dependencies listed in `requirements.txt`

## Setup

```bash
pip install -r requirements.txt
python generate_active_watchlist.py
python scanner.py
```

Backtesting:

```bash
python run_backtest.py
python analyze_backtest.py
```

Parameter search:

```bash
python optimize_strategy.py
```

### Parameter Optimization
`optimize_strategy.py` defaults to `TEST_MODE = True`, which runs a small parameter search for demonstration purposes.
Set `TEST_MODE = False` to run the full parameter grid. The full optimization is computationally expensive and may take a significant amount of time.

## Status
(Last Worked On: Sometime in 2024)
Archived learning project. The strategy and backtesting code are experimental and should not be treated as financial advice or a validated trading system.
