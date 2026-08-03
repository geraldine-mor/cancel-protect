"""
Functions for loading datasets, models, and evaluation artefacts.

Provides cached utilities for loading data, trained pipelines, and model
evaluation outputs used throughout the Streamlit application.
"""

import streamlit as st
import pandas as pd
import joblib
import json


@st.cache_data
def load_dropdown_options():
    """
    Load the unique country and agent values used to populate
    dashboard input dropdowns.

    Returns:
        pandas.DataFrame: Unique, non-null country and agent values.
    """
    df = pd.read_csv(
        "outputs/datasets/cleaned/HotelBookingsValid.csv",
        usecols=["country", "agent"]
    )
    return df.dropna()


def load_raw():
    """
    Load the raw hotel bookings dataset.

    Returns:
        pandas.DataFrame: The raw hotel bookings dataset.
    """
    raw_df = pd.read_csv("outputs/datasets/collection/HotelBookings.csv")
    return raw_df


@st.cache_data
def load_clean():
    """
    Load the fully cleaned hotel bookings dataset.

    Returns:
        pandas.DataFrame: The fully cleaned hotel bookings dataset.
    """
    clean_df = pd.read_csv("outputs/datasets/cleaned/HotelBookingsClean.csv")
    return clean_df


@st.cache_resource
def load_pipeline(pipeline_path: str):
    """
    Load a trained machine learning pipeline.

    Args:
        pipeline_path: Path to the saved pipeline file.

    Returns:
        Any: The loaded pipeline object.
    """
    return joblib.load(filename=pipeline_path)


@st.cache_data
def load_evaluation_metrics():
    """
    Load model evaluation metrics.

    Returns:
        dict: Dictionary containing the model evaluation metrics.
    """
    with open(
              "outputs/ml_pipeline/cancel_predict/v2/evaluation_metrics.json"
              ) as f:
        return json.load(f)


@st.cache_data
def load_feature_importance():
    """
    Load feature importance scores for the trained model.

    Returns:
        pandas.DataFrame: Feature importance values sorted by importance.
    """
    feature_importance_df = pd.read_csv(
        "outputs/ml_pipeline/cancel_predict/v2/feature_importance.csv"
    )
    return feature_importance_df
