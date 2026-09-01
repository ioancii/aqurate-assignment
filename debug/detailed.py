import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

df = pd.read_sql("SELECT * FROM orders_raw", engine)

# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)

# print("-- SHAPE --")
# print(df.shape)

# print("\n-- NULLS PER COLUMN --")
# print(df.isnull().sum())

# print("\n-- duplicate rows --")
# print(df.duplicated().sum())

# print("\n-- Duplicate order_ids --")
# dupe_ids = df[df.duplicated(subset=["order_id"], keep=False)].sort_values("order_id")
# print(dupe_ids.head(20))

# print("\n-- Unique values: status --")
# print(df["status"].value_counts(dropna=False))

# print("\n-- Unique values: currency --")
# print(df["currency"].value_counts(dropna=False))

# print("\n-- Unique values: category --")
# print(df["category"].value_counts(dropna=False))

# print("\n-- Unique values: country --")
# print(df["country"].value_counts(dropna=False))

# print("\n-- qty stats --")
# print(df["qty"].describe())

# print("\n-- unit_price stats --")
# print(df["unit_price"].describe())

# print("\n-- fx_reference_date range --")
# print(df["fx_reference_date"].min(), "to", df["fx_reference_date"].max())

# print("\n-- order_ts sample + dtype check --")
# print(df["order_ts"].head())

print("\n-- number of rows with negative quantity --")
print((df["qty"] < 0).sum())