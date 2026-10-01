import pandas as pd

from backtester import backtest_stock
from watchlist import load_watchlist


def main():
    all_results = []
    for ticker in load_watchlist("tickers.csv"):
        print(f"🔍 Backtesting {ticker}...")
        all_results.extend(backtest_stock(ticker))

    pd.DataFrame(all_results).to_csv("backtest_results.csv", index=False)
    print("✅ Backtest complete. Results saved to backtest_results.csv")


if __name__ == "__main__":
    main()
