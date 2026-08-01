"""Custom data transformation functions used during preprocessing."""

import pandas as pd


# Custom Transformers
def undefined_meal(data: pd.DataFrame) -> pd.DataFrame:
    """
    Replace undefined meal values with the'SC' category.

    Args:
        data: DataFrame containing the hotel booking data.

    Returns:
        pandas.DataFrame: A copy of the input DataFrame with
        ``"Undefined"`` meal values replaced by ``"SC"``.
    """

    data = data.copy()
    data["meal"] = data["meal"].replace("Undefined", "SC")
    return data
