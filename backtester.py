from data_fetcher import fetch_stock_data
from rsi_calculator import calculate_rsi


def backtest_dataframe(
    df,
    ticker,
    hold_days=5,
    stop_loss_pct=10,
    take_profit_pct=15,
    rsi_threshold=30,
    volume_multiplier=1.3,
):
    #Backtest the RSI + volume-spike strategy against a prepared DataFrame.
    if df is None or len(df) < 15:
        return []

    results = {}
    for i in range(15, len(df) - hold_days):
        row = df.iloc[i]
        previous_volume = df.iloc[i - 5:i]["Volume"].mean()
        volume_spike = row["Volume"] > volume_multiplier * previous_volume
        rsi_trigger = row["RSI"] < rsi_threshold

        if not (volume_spike and rsi_trigger):
            continue

        buy_price = df.iloc[i + 1]["Open"]
        stop_loss = buy_price * (1 - stop_loss_pct / 100)
        take_profit = buy_price * (1 + take_profit_pct / 100)
        exit_price = None
        exit_reason = None

        for j in range(i + 1, i + 1 + hold_days):
            day = df.iloc[j]
            if day["Low"] <= stop_loss:
                exit_price = stop_loss
                exit_reason = "Stop Loss"
                break
            if day["High"] >= take_profit:
                exit_price = take_profit
                exit_reason = "Take Profit"
                break

        if exit_price is None:
            exit_price = df.iloc[i + hold_days]["Close"]
            exit_reason = "Time Expired"

        net_return = (exit_price - buy_price) / buy_price * 100
        date = df.index[i].strftime("%Y-%m-%d")
        results[(date, ticker)] = {
            "Date": date,
            "Ticker": ticker,
            "Buy Price": round(buy_price, 2),
            "Exit Price": round(exit_price, 2),
            "Return %": round(net_return, 2),
            "Exit Reason": exit_reason,
            "RSI": round(row["RSI"], 2),
            "Volume Spike": True,
        }

    return list(results.values())


def backtest_stock(ticker, hold_days=7, stop_loss_pct=20, take_profit_pct=60):
    #Fetch data and run the original standalone backtest defaults.
    df = fetch_stock_data(ticker, period="6mo")
    if df is None:
        return []
    df["RSI"] = calculate_rsi(df)
    return backtest_dataframe(
        df, ticker, hold_days, stop_loss_pct, take_profit_pct,
        rsi_threshold=33, volume_multiplier=1.3
    )


# Backward-compatible name used by the optimizer.
def backtest_stock_cached(df, ticker, hold_days=5, stop_loss_pct=10, take_profit_pct=15, rsi_threshold=30, volume_multiplier=1.3):
    return backtest_dataframe(
        df, ticker, hold_days, stop_loss_pct, take_profit_pct,
        rsi_threshold, volume_multiplier
    )
