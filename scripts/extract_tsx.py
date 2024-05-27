import os
import pandas as pd
from datetime import date
from google.cloud import bigquery
from multiprocessing import Process

PATH_CONTRACTS = '../data/contracts100.csv'
PATH_OUTPUT = '../data/tsx/tsx-%s.csv'

# GOOGLE BIGQUERY
PROJECT = ''

# CREDENTIALS
CREDENTIALS = ''

# CONSTANTES PARA LA QUERY
DATE_START = '2023/01/01'
DATE_END = '2024/02/28'

QUERY_DAYS = (14, 28)

def extract(
            date: date,
            contracts: tuple
        ) -> None:
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIALS
    client = bigquery.Client(project=PROJECT)
    
    query = f"""
        SELECT 
            `hash`,
            to_address,
            input,
            block_timestamp,
            receipt_gas_used
        FROM bigquery-public-data.crypto_ethereum.transactions
        WHERE to_address IN {contracts}
            AND receipt_status = 1
            AND STRING(DATE(block_timestamp)) = "{date}"
    """
    
    df_tsx = client.query(query).to_dataframe()
    df_tsx.to_csv(PATH_OUTPUT % date, sep=';', index=False)


def main():
    contracts = tuple(pd.read_csv(PATH_CONTRACTS)['contract'].tolist())

    dates = pd.date_range(start=DATE_START, end=DATE_END, freq='D')
    dates = [date.date() for date in dates if date.day in QUERY_DAYS]

    processes = list()
    for date in dates:
        process = Process(target=extract,args=(date, contracts))
        processes.append(process)
        process.start()

    """
    for process in processes:
        process.join()
    """

if __name__=='__main__':
    main()