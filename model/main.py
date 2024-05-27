import os
import pandas as pd
import logging
from preprocessing.process import process_abi, extract_signature_column, process_input
from utils.parallel_execution import process
from multiprocessing import Manager
from export.dumper import export_models, import_models
from modeling.trainer import train
from typing import Tuple

logging.basicConfig(
    filename='model.log',
    level=logging.INFO, # nivel de profundidad del log DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL
    filemode='a' # 'w' para truncar y 'a' para añadir de 0
)

logger = logging.getLogger(__name__)

DATA_PATH = '../data/'
TSX_PATH = DATA_PATH + 'tsx'


def read() -> Tuple[pd.DataFrame, pd.DataFrame]:
    tsx = pd.read_csv(DATA_PATH + 'example_tsx.csv', sep=';', index_col='hash')
    contracts = pd.read_csv(DATA_PATH + 'contracts100.csv', sep=';', index_col='contract')
    
    return tsx, contracts

def read_all() -> Tuple[pd.DataFrame, pd.DataFrame]:
    contracts = pd.read_csv('../data/contracts100.csv', sep=';', index_col='contract')

    df_tsx = []
    for filename in os.listdir(TSX_PATH):
        if not filename.endswith('.csv'):
            continue

        filepath = os.path.join(TSX_PATH, filename)
        df = pd.read_csv(filepath, sep=';', index_col='hash')
        df_tsx.append(df)
    
    tsx = pd.concat(df_tsx)

    return tsx, contracts

def main() -> None:
    # tsx, contracts = read_all()
    tsx, contracts = read()
    
    contracts = process_abi(contracts)

    manager = Manager()
    models = manager.dict()

    process(tsx, contracts, models, manager)

    export_models(models, '../data/models.pkl')

if __name__=='__main__':
    main()