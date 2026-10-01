import pandas as pd
from data_fetcher import fetch_stock_data
from rsi_calculator import calculate_rsi
from backtester import backtest_stock_cached
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import pickle
import os
from multiprocessing import freeze_support


CORE_COUNT = max(1, min(4, (os.cpu_count() or 2) // 2))  # Use half of available cores, but at least 1 and at most 4
TEST_MODE = True  # Set to True for testing with a limited number of tickers
TEST_TICKER_LIMIT = 5

def test_combo(sl, tp, hold_days, rsi_thresh, vol_mult):
    with open("cached_data.pkl", "rb") as f:
        cached_data = pickle.load(f)

    all_trades = []
    for ticker, df in cached_data.items():
        trades = backtest_stock_cached(
            df,
            ticker,
            hold_days=hold_days,
            stop_loss_pct=sl,
            take_profit_pct=tp,
            rsi_threshold=rsi_thresh,
            volume_multiplier=vol_mult
        )
        all_trades.extend(trades)

    if not all_trades:
        return None

    df_trades = pd.DataFrame(all_trades)
    df_trades["Net"] = df_trades["Exit Price"] - df_trades["Buy Price"]
    df_trades["PnL"] = df_trades["Net"] * 10
    df_trades["Win"] = df_trades["PnL"] > 0

    starting_balance = df_trades["Buy Price"].sum() * 10
    total_profit = df_trades["PnL"].sum()
    roi = (total_profit / starting_balance) * 100 if starting_balance else 0

    return {
        "Stop Loss %": sl,
        "Take Profit %": tp,
        "Hold Days": hold_days,
        "RSI Threshold": rsi_thresh,
        "Vol Multiplier": vol_mult,
        "Total Trades": len(df_trades),
        "Wins": int(df_trades["Win"].sum()),
        "Losses": int(len(df_trades) - df_trades["Win"].sum()),
        "ROI": round(roi, 2)
    }



def main():
    CSV_FILE = "tickers.csv"
    print("📥 Fetching stock data for all tickers...")
    from watchlist import load_watchlist
    tickers = load_watchlist(CSV_FILE)
    cached_data = {}

    if TEST_MODE:
        tickers = tickers[:TEST_TICKER_LIMIT]

    for ticker in tickers:
        df = fetch_stock_data(ticker, period="6mo")
        if df is not None and not df.empty:
            df["RSI"] = calculate_rsi(df)
            cached_data[ticker] = df

    print(f"✅ Cached {len(cached_data)} tickers.\n")

    with open("cached_data.pkl", "wb") as f:
        pickle.dump(cached_data, f)

    if TEST_MODE:
        rsi_values = [30, 35]
        vol_multipliers = [1.3, 1.5]

        combos = [
            (sl, tp, hold, rsi, vol)
            for sl in [10, 15]
            for tp in [15, 20]
            for hold in [5, 7]
            for rsi in rsi_values
            for vol in vol_multipliers
        ]
    else:
        rsi_values = [25, 30, 35, 40]
        vol_multipliers = [1.2, 1.3, 1.5, 1.7]

        combos = [
            (sl, tp, hold, rsi, vol)
            for sl in range(5, 31)
            for tp in range(10, 31)
            for hold in range(5, 16)
            for rsi in rsi_values
            for vol in vol_multipliers
        ]


    results = []
    print("🚀 Launching parallel brute-force...\n")
    with ProcessPoolExecutor(max_workers=CORE_COUNT) as executor:
        futures = [executor.submit(test_combo, sl, tp, hold_days, rsi, vol) for sl, tp, hold_days, rsi, vol in combos]
        for f in tqdm(as_completed(futures), total=len(futures), desc="⚙️ Brute-forcing combos"):
            result = f.result()
            if result:
                results.append(result)

    df_results = pd.DataFrame(results).sort_values(by="ROI", ascending=False)
    df_results.to_csv("optimization_results.csv", index=False)

    print("\n🏆 Top 10 ROI combos:")
    print(df_results.head(10))

    if os.path.exists("cached_data.pkl"):
        os.remove("cached_data.pkl")


if __name__ == '__main__':
    freeze_support()
    main()
