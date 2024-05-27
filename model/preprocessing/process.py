import logging
import pandas as pd
import numpy as np
from preprocessing.decode import decode_input, count_elements
from typing import Union

logger = logging.getLogger(__name__)

def process_abi(
        contracts: pd.DataFrame
) -> pd.DataFrame:
    """
    Process the 'abi' and 'proxy_abi' columns in the contracts DataFrame.

    Args:
        contracts (pd.DataFrame): DataFrame containing contract data.

    Returns:
        pd.DataFrame: DataFrame with the 'abi' and 'proxy_abi' columns processed.
    """
    contracts['abi'] = contracts['abi'].apply(eval)
    contracts['proxy_abi'] = contracts['proxy_abi'].apply(lambda proxy_abi: eval(proxy_abi) if isinstance(proxy_abi, str) else proxy_abi)

    return contracts

def extract_signature_column(
        tsx: pd.DataFrame
) -> None:
    """
    Extracts the first 10 characters from the 'input' column in the transaction
    DataFrame and creates a new column 'signature' with these extracted characters.

    Args:
        tsx (pd.DataFrame): DataFrame containing the input data.

    Returns:
        pd.DataFrame: DataFrame with the 'signature' column added.
    """
    tsx['signature'] = tsx['input'].map(lambda x: x[:10])

def filter_data_tye(
        type: str
) -> bool:
    """
    Verify if type is in filtered_types

    Args:
        type (str)

    Returns:
        bool: if type is in filtered_types
    """
    filtered_types = {'address'}
    return type in filtered_types

def process_input(
        tsx: pd.DataFrame,
        contract: pd.Series,
        signature: str
) -> Union[pd.DataFrame, None]:
    """
    Process transaction input data by decoding it using the contract's ABI.

    Args:
        tsx (pd.DataFrame): DataFrame containing transaction data.
        contract (pd.Series): Series containing information about the contract.
        signature (str)
    Returns:
        pd.DataFrame: DataFrame with additional columns added based on decoded input data.
    """
    tsx = tsx.copy()
    tsx['decode_input'] = tsx['input'].apply(decode_input, args=(contract,))

    if tsx['decode_input'].isna().all():
        logger.error(f'SIGNATURE decode failure: contract {contract.name} signature: {signature}')
    
    try:
        for index, row in tsx.iterrows():
            tsx.at[index,'input_len'] = len(row['input'])
            decode_input_value = row['decode_input']
            if decode_input_value is np.nan: continue
            for (data_type, column_name, value) in decode_input_value:
                if(filter_data_tye(data_type)): continue
                processed_value = process_type(value, data_type)
                if isinstance(processed_value, tuple):
                    tsx.at[index, data_type + '_'+ column_name] = processed_value[0]
                    tsx.at[index, column_name + '_iszero'] = processed_value[1]
                else:
                    tsx.at[index, data_type + '_'+ column_name] = processed_value
    except Exception as e:
        logger.error(f"{signature}: {e}")

    tsx.fillna(0, inplace=True)

    tsx.drop(columns=['decode_input'], inplace=True)

    return tsx

def process_type(
        value: str,
        type: str
) -> int:
    """
    Keywords uint8 to uint256 in steps of 8 (unsigned of 8 up to 256 bits) and int8 to int256. 
    uint and int are aliases for uint256 and int256, respectively.
    """
    INT_TYPES = [
        'uint', 'uint8', 'uint16', 'uint24', 'uint32', 'uint40', 'uint48', 'uint56', 'uint64', 
        'uint72', 'uint80', 'uint88', 'uint96', 'uint104', 'uint112', 'uint120', 'uint128', 
        'uint136', 'uint144', 'uint152', 'uint160', 'uint168', 'uint176', 'uint184', 'uint192', 
        'uint200', 'uint208', 'uint216', 'uint224', 'uint232', 'uint240', 'uint248', 'uint256', 
        'int', 'int8', 'int16', 'int24', 'int32', 'int40', 'int48', 'int56', 'int64', 'int72', 
        'int80', 'int88', 'int96', 'int104', 'int112', 'int120', 'int128', 'int136', 'int144', 
        'int152', 'int160', 'int168', 'int176', 'int184', 'int192', 'int200', 'int208', 'int216', 
        'int224', 'int232', 'int240', 'int248', 'int256'
    ]

    PROCESSING_INT_TYPES = ['uint8', 'uint16', 'uint24', 'uint32', 'uint40', 'uint48', 'uint56', 'uint64',
                            'int8', 'int16', 'int24', 'int32', 'int40', 'int48', 'int56', 'int64']

    UNPROCESSING_INT_TYPES = ['int', 'int72', 'int80', 'int88', 'int96', 'int104', 'int112', 'int120', 'int128',
                              'int136', 'int144', 'int152', 'int160', 'int168', 'int176', 'int184', 'int192',
                              'int200', 'int208', 'int216', 'int224', 'int232', 'int240', 'int248', 'int256',
                              'uint', 'uint72', 'uint80', 'uint88', 'uint96', 'uint104', 'uint112', 'uint120', 'uint128', 
                              'uint136', 'uint144', 'uint152', 'uint160', 'uint168', 'uint176', 'uint184', 'uint192', 
                              'uint200', 'uint208', 'uint216', 'uint224', 'uint232', 'uint240', 'uint248', 'uint256']
    
    if type in PROCESSING_INT_TYPES:
        return int(value)

    if type in UNPROCESSING_INT_TYPES:
        try:
            value_int = int(value)
            return (len(str(value)), 1 if value_int == 0 else 0)
        except ValueError:
            return len(str(value))

    if isinstance(value, list):
        return count_elements(value)
    else:
        return len(str(value))