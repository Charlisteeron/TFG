from google.cloud import bigquery
import os
import pandas as pd
import requests

# ETHERSCAN
API_ETHERSCAN = ''

# GOOGLE BIGQUERY
PROJECT = ''

# CREDENTIALS
CREDENTIALS = ''

ERROR_ABI = 'Contract source code not verified'

PATH_OUTPUT = '../data/contracts100.csv'

def get_abi(address):
    request = f"https://api.etherscan.io/api?module=contract&action=getabi&address={address}&apikey={API_ETHERSCAN}"
    response = requests.get(request)

    abi = response.json().get('result')
    abi = abi.replace('true', 'True').replace('false', 'False')

    return abi

def extract_contracts():
    
    with open('./contracts500.sql') as file:
        query_contracts = file.read()

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIALS

    client = bigquery.Client(project=PROJECT)
    df_contracts = client.query(query_contracts).result().to_dataframe()

    df_contracts['abi'] = df_contracts['contract'].map(get_abi)

    df_contracts = df_contracts[df_contracts['abi'] != ERROR_ABI].sort_values(by='count_contract', ascending=False)
    df_contracts = df_contracts[['contract', 'abi']].head(100)

    df_contracts.to_csv(PATH_OUTPUT, index=False)


if __name__=='__main__':
    extract_contracts()