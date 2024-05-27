import logging
import pandas as pd
import numpy as np
from typing import Union
from web3_input_decoder import decode_function

logger = logging.getLogger(__name__)

def decode_input(
        input_value: str,
        contract: pd.Series
) -> Union[pd.Series, None]:
    """
    Decode the input of a transaction using the contract's ABI.

    Args:
        input_value (str): Hex string contains input value.
        contract (pd.Series): Series containing information about the contract.

    Returns:
        Union[List, None]: A list containing the decoded transaction if successful,
        or None if decoding fails in both attempts.
    """
    try:
        return decode_function(contract['abi'], input_value)
    except Exception as e:
        logger.warning(f'ABI: {e}')
        try:
            return decode_function(contract['proxy_abi'], input_value)
        except Exception as e:
            logger.warning(f'PROXY ABI: {e}')
            return np.nan
        
def count_elements(value):
    if isinstance(value, list):
        return sum(count_elements(item) for item in value)
    else:
        return 1