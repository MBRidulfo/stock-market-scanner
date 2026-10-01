import requests
import pandas as pd

def fetch_most_active(limit=50):
    url = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"
    params = {
        'scrIds': 'most_actives',
        'count': limit,
    }

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    results = data['finance']['result'][0]['quotes']

    # Extract ticker and name
    tickers = [{"symbol": x["symbol"], "name": x.get("shortName", "")} for x in results]
    df = pd.DataFrame(tickers)
    return df

if __name__ == "__main__":
    df = fetch_most_active()
    df.to_csv("tickers.csv", index=False)
    print(df)