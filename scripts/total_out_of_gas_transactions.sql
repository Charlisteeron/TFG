WITH 

out_of_gas_transaction_failed AS (
  SELECT 
    COUNT(*) AS limit_gas_consumed,
    receipt_status
  FROM 
    `bigquery-public-data.crypto_ethereum.transactions`
  WHERE 
    gas = receipt_gas_used AND
    TIMESTAMP_TRUNC(block_timestamp, YEAR) = TIMESTAMP("2023-01-01")
  GROUP BY 
    receipt_status
),
transactions_2023 AS (
  SELECT 
    COUNT(*) AS total_transactions,
    receipt_status
  FROM 
    `bigquery-public-data.crypto_ethereum.transactions`
  WHERE 
    TIMESTAMP_TRUNC(block_timestamp, YEAR) = TIMESTAMP("2023-01-01")
  GROUP BY 
    receipt_status
)

SELECT 
  coalesce(t1.receipt_status, t2.receipt_status) as receipt_status,
  t1.limit_gas_consumed,
  t2.total_transactions
FROM 
  out_of_gas_transaction_failed t1
FULL OUTER JOIN 
  transactions_2023 t2
ON 
  t1.receipt_status = t2.receipt_status