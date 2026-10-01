import pandas as pd

def calculate_rsi(df, period=14):
    delta = df["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Use Wilder's smoothing: first value is SMA, then recursive smoothing
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    # Initialize RSI series with NaN
    rsi = pd.Series(index=df.index, dtype=float)

    # Start at the first non-NaN avg gain/loss
    for i in range(period, len(df)):
        if i == period:
            current_gain = avg_gain.iloc[i]
            current_loss = avg_loss.iloc[i]
        else:
            current_gain = (prev_gain * (period - 1) + gain.iloc[i]) / period
            current_loss = (prev_loss * (period - 1) + loss.iloc[i]) / period

        rs = current_gain / current_loss if current_loss != 0 else float('inf')
        rsi.iloc[i] = 100 - (100 / (1 + rs))

        prev_gain = current_gain
        prev_loss = current_loss

    return rsi

