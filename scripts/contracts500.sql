SELECT 
    c.address AS contract,
    COUNT(c.address) AS count_contract
FROM bigquery-public-data.crypto_ethereum.transactions AS t 
JOIN bigquery-public-data.crypto_ethereum.contracts AS c
    ON t.to_address = c.address
WHERE t.block_timestamp >= TIMESTAMP(DATE "2023-01-01")
GROUP BY c.address
ORDER BY count_contract DESC
LIMIT 500