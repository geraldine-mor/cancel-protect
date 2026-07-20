import streamlit as st
import joblib
from utils.data_management import load_pipeline

pipeline = load_pipeline(
    "outputs/ml_pipeline/cancel_predict/v2/classification_model_pipeline.pkl")

def predict_cancellation(input_df):
    prediction = pipeline.predict(input_df)[0]
    probability = pipeline.predict_proba(input_df)[0][1]
    return prediction, probability