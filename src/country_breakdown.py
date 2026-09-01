import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

sql = """
DROP TABLE IF EXISTS country_category_revenue;

CREATE TABLE country_category_revenue AS
SELECT
    oc.country,
    ROUND(SUM(
        CASE
            WHEN oc.currency = 'EUR' THEN oc.qty * oc.unit_price
            WHEN oc.currency = 'RON' THEN oc.qty * oc.unit_price / fx.rate
        END
    )::numeric, 2) AS total_revenue_eur
FROM orders_clean oc
LEFT JOIN LATERAL (
    SELECT "EUR-to-RON" AS rate
    FROM fx_rates
    WHERE date <= oc.fx_reference_date
    ORDER BY date DESC
    LIMIT 1
) fx ON oc.currency = 'RON'
WHERE oc.status = 'completed'
  AND oc.category IN ('Books', 'Electronics')
GROUP BY oc.country
HAVING SUM(
    CASE
        WHEN oc.currency = 'EUR' THEN oc.qty * oc.unit_price
        WHEN oc.currency = 'RON' THEN oc.qty * oc.unit_price / fx.rate
    END
) > 40000
ORDER BY total_revenue_eur DESC;
"""

with engine.begin() as conn:
    conn.execute(text(sql))
    result = conn.execute(text("SELECT * FROM country_category_revenue"))
    for row in result:
        print(row)

print("\ncountry_category_revenue created")