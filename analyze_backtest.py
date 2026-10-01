import pandas as pd

CSV_FILE = "backtest_results.csv"
SHARES_PER_TRADE = 100


def main():
    df = pd.read_csv(CSV_FILE)
    df["Net"] = df["Exit Price"] - df["Buy Price"]
    df["PnL"] = df["Net"] * SHARES_PER_TRADE
    df["Win"] = df["PnL"] > 0

    total_trades = len(df)
    wins = int(df["Win"].sum())
    losses = total_trades - wins
    win_rate = (wins / total_trades) * 100 if total_trades else 0
    starting_balance = df["Buy Price"].sum() * SHARES_PER_TRADE
    total_profit = df["PnL"].sum()
    ending_balance = starting_balance + total_profit
    roi = (total_profit / starting_balance) * 100 if starting_balance else 0

    print("📈 BACKTEST SUMMARY")
    print(f"Total Trades: {total_trades}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Win Rate: {win_rate:.2f}%")
    print("\n💵 FINANCIALS")
    print(f"Starting Balance: ${starting_balance:,.2f}")
    print(f"Total Profit: ${total_profit:,.2f}")
    print(f"Ending Balance: ${ending_balance:,.2f}")
    print(f"ROI: {roi:.2f}%")
    df.to_csv("backtest_results_analyzed.csv", index=False)


if __name__ == "__main__":
    main()
