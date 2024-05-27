import pandas as pd
from multiprocessing import Process
from multiprocessing.managers import DictProxy, SyncManager
from modeling.trainer import train
from preprocessing.process import process_input, extract_signature_column


MIN_LEN_TSX = 10000


def process(
        tsx: pd.DataFrame,
        contracts: pd.DataFrame,
        models: DictProxy,
        manager: SyncManager
) -> None:
    """
    Process transactions data set.

    Args:
        tsx (pd.DataFrame): DataFrame containing transactions.
        contracts (pd.DataFrame): DataFrame containing contract information.
        models (DictProxy): Dictionary proxy for storing data models.
        manager (SyncManager): SyncManager object for creating shared objects like 'models'.
    """
    processes_contract = list()

    tsx = tsx.groupby('to_address')

    for contract, contract_tsx in tsx:
        models[contract] = manager.dict()
        process = Process(target=process_contract, args=(contracts.loc[contract], contract_tsx, models))
        processes_contract.append(process)
        process.start()

    for process in processes_contract:
        process.join()

def process_contract(
        contract: pd.Series,
        contract_tsx: pd.DataFrame,
        models: DictProxy,
) -> None:
    """
    Process transactions associated with a specific contract grouped by signature.

    Args:
        contract (pd.Series): Series containing information about the contract.
        contract_tsx (pd.DataFrame): DataFrame containing transactions associated with the contract.
        models (DictProxy): Dictionary proxy for storing data models.
    """
    processes_signature = list()

    extract_signature_column(contract_tsx)
    contract_tsx = contract_tsx.groupby('signature')
    
    for signature, signature_tsx in contract_tsx:
        if len(signature_tsx) > MIN_LEN_TSX: 
            process = Process(target=process_signature, args=(contract, signature, signature_tsx, models))
            processes_signature.append(process)
            process.start()

    for process in processes_signature:
        process.join()

def process_signature(
        contract: pd.Series,
        signature: str,
        signature_tsx: pd.DataFrame,
        models: DictProxy
) -> None:
    """
    Process transactions associated with a specific signature of a contract.

    Args:
        contract (pd.Series): Series containing information about the contract.
        signature (str): Signature associated with the transactions.
        signature_tsx (pd.DataFrame): DataFrame containing transactions associated with the signature.
        models (DictProxy): Dictionary proxy for storing data models.
    """
    signature_tsx = process_input(signature_tsx,contract, signature)

    models[contract.name][signature] = train(signature_tsx)

    return