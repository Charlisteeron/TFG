import pandas as pd
import requests

PATH_CONTRACTS = "../data/contracts100.csv"
PATH_OUTPUT = "../data/contracts_abi.csv"

API = "" # API_KEY


def main():
    contracts_abi = pd.DataFrame(columns=['address', 'abi'])

    contracts = pd.read_csv(PATH_CONTRACTS, header=None).values[0]
    for address in contracts:
        request = f"https://api.etherscan.io/api?module=contract&action=getabi&address={address}&apikey={API}"

        response = requests.get(request)
        if response.status_code != 200:
            continue

        abi = response.json().get("result")
        abi = abi.replace("true", "True").replace("false", "False")

        contracts_abi.loc[len(contracts_abi)] = [address, abi]

    contracts_abi.to_csv(PATH_OUTPUT, index=False)

if __name__=="__main__":
    main()