# Aqurate Junior Data Engineer - Challenge

End-to-end ETL pipeline: pulls order data from an API, cleans it, converts revenue to EUR using daily FX rates, and produces two aggregate reporting tables.

## Setup

1. Create a `.env` file with:
DATABASE_URL=supabase_connection_string
SOURCE_API_URL=https://jzozteoirwfczccltcdr.supabase.co/rest/v1/orders_raw
SOURCE_API_KEY=source_api_key


2. Install dependencies:
pip install -r requirements.txt

Run order:
python src/ingest.py
python src/clean.py
python src/exchange_rates.py
python src/customer_spend.py
python src/country_breakdown.py


## Pipeline

- `ingest.py` — pulls `orders_raw` from source API into Supabase
- `clean.py` — cleans dupes, removes test/invalid rows and creates `orders_clean`
- `exchange_rates.py` — fetches the daily EUR to RON rates into `fx_rates`
- `customer_spend.py` — total EUR spend per customer, using the most recent FX rate on/before each order
- `country_breakdown.py` — EUR revenue by country for Books/Electronics, countries >€40k only
