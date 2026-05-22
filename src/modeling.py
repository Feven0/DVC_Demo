import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


def split_data(
    df: pd.DataFrame,
    features: list,
    target: str,
    test_size: float = 0.2,
    random_state: int = 42
):
    """
    Splits the data into training and testing sets.
    """
    X = df[features]
    y = df[target]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def train_random_forest_regressor(
    X_train,
    y_train,
    n_estimators: int = 100,
    max_depth: int = 10,
    random_state: int = 42
):
    """
    Trains a Random Forest Regressor.
    """
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state
    )
    model.fit(X_train, y_train)
    return model


def evaluate_regressor(model, X_test, y_test):
    """
    Evaluates the regression model performance.
    """
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    return {
        'mean_squared_error': mse,
        'r2_score': r2
    }
