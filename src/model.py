import streamlit as st
from sklearn import set_config
from xgboost import XGBClassifier
from src.data_management import load_pipeline

pipeline = load_pipeline(
    "outputs/ml_pipeline/cancel_predict/v2/classification_model_pipeline.pkl")


def predict_cancellation(input_df):
    prediction = pipeline.predict(input_df)[0]
    probability = pipeline.predict_proba(input_df)[0][1]
    return prediction, probability


def pipeline_steps():

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
