import pandas as pd
import numpy as np
from typing import Dict, Any
from sklearn.model_selection import train_test_split
from modeling.MyLinearRegression import MyLinearRegression
from modeling.MyGradientBoostingRegressor import MyGradientBoostingRegressor

def train(
        signature_tsx: pd.DataFrame,
) -> Dict[str, Any]:
    models = dict()
    X = signature_tsx.drop(['to_address', 'input', 'signature', 'receipt_gas_used'], axis=1)
    y = signature_tsx['receipt_gas_used']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    random_index = np.random.choice(len(X_test), size=min(500, len(X_test)), replace=False)
    models['X_test'] = X_test.iloc[random_index]
    models['y_test'] = y_test.iloc[random_index]
    models['size'] = len(y)

    X_train.drop(['block_timestamp'], axis=1, inplace=True)
    X_test.drop(['block_timestamp'], axis=1, inplace=True)

    linear = MyLinearRegression()
    linear.train_model(X_train, X_test, y_train, y_test)
    models['LinearRegression'] = linear

    gradient_boost = MyGradientBoostingRegressor()
    gradient_boost.train_model(X_train, X_test, y_train, y_test)
    models['GradientBoost'] = gradient_boost
    
    return models