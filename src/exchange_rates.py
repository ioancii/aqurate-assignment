import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

START_DATE = "2026-08-23"
END_DATE = "2026-09-03"

#get rates EUR - RON
def daily_fx_rates():
    url = f"https://api.frankfurter.dev/v1/{START_DATE}..{END_DATE}"
    params = {
        "base": "EUR",
        "symbols": "RON"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def main():
    data = daily_fx_rates()
    rates = data["rates"]
    rows = []

    for date, rate in rates.items():
        rows.append({"date": date, "EUR-to-RON": rate["RON"]})

    df = pd.DataFrame(rows)
    print(df)

    df.to_sql("fx_rates", engine, if_exists="replace", index=False)
    print("\nLoaded into fx_rates")

if __name__ == "__main__":
    main()