import pandas as pd
import requests

CONTRACTS_PATH = '../data/contracts100.csv'
API_ETHERSCAN = ''

def get_abi(address):
    request = f"https://api.etherscan.io/api?module=contract&action=getabi&address={address}&apikey={API_ETHERSCAN}"
    response = requests.get(request)

    abi = response.json().get('result')
    abi = abi.replace('true', 'True').replace('false', 'False')

    return abi

def main():
    contracts = pd.read_csv(CONTRACTS_PATH, index_col='contract')
    contracts['proxy_abi'] = ''
    contract = 0

    while True:
        contract = input('Introduce el contrato a actualizar: ')
        if contract in ('exit', 'e'): break

        new_contract = input('Introduce el proxy contract: ')

        contracts.loc[contract.lower(), 'proxy_abi'] = get_abi(new_contract)

    contracts.to_csv(CONTRACTS_PATH)


if __name__=='__main__':
    main()