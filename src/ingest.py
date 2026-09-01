import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SOURCE_API_URL = os.getenv("SOURCE_API_URL")
SOURCE_API_KEY = os.getenv("SOURCE_API_KEY")

def fetch_orders_raw():
    headers = {
        "apikey": SOURCE_API_KEY,
        "Authorization": f"Bearer {SOURCE_API_KEY}",
    }
    response = requests.get(SOURCE_API_URL, headers=headers)
    response.raise_for_status()  
    return response.json()

def main():
    data = fetch_orders_raw()
    df = pd.DataFrame(data)

    print(f"Pulled {len(df)} rows")
    print(df.head())
    #print("\n--------------------------------------------")
    print(df.dtypes)

    engine = create_engine(DATABASE_URL)
    df.to_sql('orders_raw', engine, if_exists='replace', index=False)
    print("loaded into orders_raw")

if __name__ == "__main__":
    main()