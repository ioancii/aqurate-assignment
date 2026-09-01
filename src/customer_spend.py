import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

sql = """
DROP TABLE IF EXISTS customer_spend_eur;

CREATE TABLE customer_spend_eur AS
SELECT
    oc.customer_id,
    ROUND(SUM(
        CASE
            WHEN oc.currency = 'EUR' THEN oc.qty * oc.unit_price
            WHEN oc.currency = 'RON' THEN oc.qty * oc.unit_price / fx.rate
        END
    )::numeric, 2) AS total_spent_eur
FROM orders_clean oc
LEFT JOIN LATERAL (
    SELECT "EUR-to-RON" AS rate
    FROM fx_rates
    WHERE date <= oc.fx_reference_date
    ORDER BY date DESC
    LIMIT 1
) fx ON oc.currency = 'RON'
WHERE oc.status = 'completed'
GROUP BY oc.customer_id
ORDER BY total_spent_eur DESC;
"""

with engine.begin() as conn:
    conn.execute(text(sql))
    result = conn.execute(text("SELECT * FROM customer_spend_eur LIMIT 10"))
    for row in result:
        print(row)

print("\ncustomer_spend_eur created")