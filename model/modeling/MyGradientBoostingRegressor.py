from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error

class MyGradientBoostingRegressor:
    def __init__(self):
        self.model = GradientBoostingRegressor(random_state=42)

    def train_model(self, X_train, X_test, y_train, y_test):
        self.model.fit(X_train, y_train)

        self.evaluate_model(X_test, y_test)

    def evaluate_model(self, X_test, y_test):
        y_pred = self.model.predict(X_test)

        self.mse = mean_squared_error(y_test, y_pred)
        self.mae = mean_absolute_error(y_test, y_pred)
        self.r2 = r2_score(y_test, y_pred)
        self.mape = mean_absolute_percentage_error(y_test, y_pred)