import pandas as pd


def load_watchlist(path="tickers.csv", column_hint="symbol"):
    #Load ticker symbols from a CSV, tolerating common column-name variations.
    df = pd.read_csv(path)
    df.columns = [column.strip() for column in df.columns]
    lower_to_actual = {column.lower(): column for column in df.columns}

    if column_hint.lower() in lower_to_actual:
        column = lower_to_actual[column_hint.lower()]
    elif "symbol" in lower_to_actual:
        column = lower_to_actual["symbol"]
    elif "ticker" in lower_to_actual:
        column = lower_to_actual["ticker"]
    else:
        column = df.columns[0]

    return (
        df[column]
        .dropna()
        .astype(str)
        .str.strip()
        .str.upper()
        .unique()
        .tolist()
    )
