import pandas as pd


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer features for the traffic congestion model.
    Currently only handles one-hot encoding of categorical variables.
    """
    # One-hot encode protocol and service
    categorical = ["protocol", "service"]
    df = pd.get_dummies(df, columns=categorical, drop_first=True)

    # Validation: check for missing/invalid values
    if df.isnull().values.any():
        raise ValueError("Missing values found in features!")

    return df
