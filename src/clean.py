import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

df = pd.read_sql("SELECT * FROM orders_raw", engine)
print(f"Start: {len(df)}")

#set singular timestamp
def correct_ts(value):
    value = str(value).strip()
    if value.isdigit():
        return pd.to_datetime(int(value), unit='s')
    if "/" in value:
        return pd.to_datetime(value, format="%d/%m/%Y %H:%M")
    return pd.to_datetime(value)

df["order_ts"] = df["order_ts"].apply(correct_ts)

# remove dupplicate orders, keep first instance
df = df.drop_duplicates()
print(f"After dropping exact duplicates: {len(df)}")

# remove test orders
df = df[df["status"] != "test"]
print(f"After dropping test status: {len(df)}")

# remove rows without customer id
df = df[df["customer_id"].notna()]
df["customer_id"] = df["customer_id"].astype(int)
print(f"After dropping null customer_id: {len(df)}")

# remove quantity < 1
df = df[df["qty"] >= 1]
print(f"After removing rows with quantity < 1: {len(df)}")

#remove unit price < 1 or above 10000
df = df[(df["unit_price"] >= 1) & (df["unit_price"] <= 10000)]
print(f"After removing rows with invalid unit price: {len(df)}")

# check final clean number + number of rows removed
print(f"\nFinal status breakdown:\n{df['status'].value_counts()}")

df.to_sql("orders_clean", engine, if_exists="replace", index=False)
print("\nLoaded into orders_clean")