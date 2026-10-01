import csv
import os
from datetime import datetime

from data_fetcher import fetch_stock_data
from rsi_calculator import calculate_rsi
from volume_analyzer import detect_volume_spike
from watchlist import load_watchlist

RSI_THRESHOLD = 30
CSV_FILE = "signal_log.csv"
CSV_HEADERS = ["Timestamp", "Ticker", "RSI", "Avg Volume", "Today Volume", "Signal Type"]


def ensure_signal_log(path=CSV_FILE):
    if not os.path.isfile(path):
        with open(path, mode="w", newline="") as file:
            csv.writer(file).writerow(CSV_HEADERS)


def scan_watchlist(path="tickers.csv"):
    watchlist = load_watchlist(path)
    ensure_signal_log()
    print("📊 Scanning watchlist for swing trade setups...\n")
    valid_signals = 0

    for ticker in watchlist:
        print(f"[{ticker}]")
        df = fetch_stock_data(ticker)
        if df is None or df.empty:
            print("  ⚠️  No data available.\n")
            continue

        df["RSI"] = calculate_rsi(df)
        volume_spike, avg_volume, _, today_volume = detect_volume_spike(df)
        current_rsi = df.iloc[-1]["RSI"]

        print(f"  RSI: {current_rsi:.2f}")
        print(f"  Volume: {today_volume:,}")
        print(f"  Avg Volume: {avg_volume:,.0f}")

        if volume_spike:
            print("  🚀 Volume spike detected!")

        if current_rsi < RSI_THRESHOLD and volume_spike:
            print("  ✅ Oversold + volume spike — possible swing trade setup!\n")
            valid_signals += 1
            with open(CSV_FILE, mode="a", newline="") as file:
                csv.writer(file).writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                    ticker,
                    round(current_rsi, 2),
                    round(avg_volume),
                    today_volume,
                    "RSI < 30 + Volume Spike",
                ])
        else:
            print("  ❌ No trade signal.\n")

    print(f"📈 Scan Complete: {valid_signals}/{len(watchlist)} potential trades found.")


if __name__ == "__main__":
    scan_watchlist()
