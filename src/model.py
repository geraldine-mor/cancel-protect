"""
Model prediction utilities for CancelProtect dashboard.

This module loads the trained classification pipeline and provides helper
functions for generating cancellation predictions and extracting details of
the preprocessing and prediction steps used by the model.
"""

import pandas as pd
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from src.data_management import load_pipeline

pipeline = load_pipeline(
    "outputs/ml_pipeline/cancel_predict/v2/classification_model_pipeline.pkl")


def predict_cancellation(input_df: pd.DataFrame) -> tuple[int, float]:
    """
    Generate a cancellation prediction and probability score.

    Uses the loaded classification pipeline to predict whether a booking will
    be cancelled and calculates the probability of cancellation from the
    classifier output.

    Args:
        input_df (pd.DataFrame): Preprocessed input features for prediction.

    Returns:
        tuple: A tuple containing:
            - prediction (int): Binary classification result indicating whether
            the booking is predicted to be cancelled.
            - probability (float): Probability score for the cancellation
            class.
    """
    prediction = pipeline.predict(input_df)[0]
    probability = pipeline.predict_proba(input_df)[0][1]
    return prediction, probability


def pipeline_steps() -> tuple[Pipeline, str]:
    """
    Extract preprocessing steps and model configuration from the pipeline.

    Retrieves the preprocessing transformer and classifier from the loaded
    pipeline. It compares the classifier parameters against the default
    XGBClassifier parameters and returns only the parameters that have been
    modified.

    Returns:
        tuple: A tuple containing:
            - preprocessing_pipeline (Pipeline): The preprocessing component
              used before model prediction.
            - model_details (str): String representation of the configured
              XGBClassifier with non-default parameters.
    """

    preprocessing_pipeline = pipeline.named_steps["Preprocessing"]
    prediction_pipeline = pipeline.named_steps["model"]

    defaults = XGBClassifier().get_params()
    current = prediction_pipeline.get_params()

    changed = {
        k: v
        for k, v in current.items()
        if defaults.get(k) != v
    }

    # Exclude "missing" because NaN != NaN so is incorrectly flagged as changed
    changed.pop("missing", None)

    params = ",\n    ".join(f"{k}={v!r}" for k, v in changed.items())
    return preprocessing_pipeline, f"XGBClassifier({params})"
