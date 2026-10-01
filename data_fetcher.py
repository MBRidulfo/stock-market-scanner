import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period="6mo", interval="1d"):
    """
    Fetch historical stock data.

    Args:
        ticker (str): Ticker symbol.
        period (str): Time period (e.g., '1mo', '3mo', '6mo', '1y').
        interval (str): Data interval (e.g., '1d', '1h', '5m').

    Returns:
        pd.DataFrame: Stock OHLCV data.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        hist = hist[["Open", "High", "Low", "Close", "Volume"]]
        hist.dropna(inplace=True)

        if len(hist) < 15:
            print(f"[{ticker}] ⚠️ Not enough data.")
            return None

        hist["Ticker"] = ticker
        return hist

    except Exception as e:
        print(f"[{ticker}] ❌ Failed to fetch data: {e}")
        return None
