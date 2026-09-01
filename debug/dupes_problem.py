import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

df = pd.read_sql("SELECT * FROM orders_raw", engine)
print(f"Loaded: {len(df)} rows")

def parse_order_ts(value):
    value = str(value).strip()
    if value.isdigit():
        return pd.to_datetime(int(value), unit="s")
    if "/" in value:
        return pd.to_datetime(value, format="%d/%m/%Y %H:%M")
    return pd.to_datetime(value)

df["order_ts"] = df["order_ts"].apply(parse_order_ts)

dupe_mask = df.duplicated(keep=False)
print(f"Rows involved in full duplicates: {dupe_mask.sum()}")

before = len(df)
df_deduped = df.drop_duplicates()
after = len(df_deduped)
print(f"Rows removed by drop_duplicates(): {before - after}")

# If these two numbers disagree, show exactly what's different
removed_rows = df[~df.index.isin(df_deduped.index)]
print(f"\nSample of rows actually removed:")
print(removed_rows[["order_id", "customer_id", "order_ts", "sku", "qty", "unit_price"]].head(20))