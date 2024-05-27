import pickle
from multiprocessing.managers import DictProxy
from typing import Dict

def export_models(
        models: DictProxy, 
        file_path: str
) -> None:
    """
    Export models stored in DictProxy to a file using pickle.

    Args:
        models (DictProxy): Dictionary proxy containing the models.
        file_path (str): File path to save the exported models.
    """
    models = {key : value.copy() for key,value in models.items()}
    with open(file_path, 'wb') as f:
        pickle.dump(models, f)

def import_models(
        file_path: str
) -> Dict:
    """
    Import models from a file using pickle and return as DictProxy.

    Args:
        file_path (str): File path to import the models from.

    Returns:
        Dict: Dictionary containing the imported models.
    """
    with open(file_path, 'rb') as f:
        models_dict = pickle.load(f)

    return dict(models_dict)
