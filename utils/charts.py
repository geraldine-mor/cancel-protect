import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from utils.data_management import load_raw, load_clean
from utils.data_processing import (
    data_prep, overall_cancel_rate, 
    grouped_cancel_rate, create_cancel_profile,
    pps_predictions, correlations)

def cancellation_charts(data: dict):
    df, column_map = data_prep(data)

    if data["choice"] == "Overall":
        rate_df = overall_cancel_rate(df)

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(data=rate_df, x="Status", y="Cancellation Rate", ax=ax)
        ax.bar_label(
            ax.containers[0],
            labels=[f"{v:.0%}" for v in rate_df["Cancellation Rate"]])
        plt.ylim(0, 1)
        plt.title("Overall Cancellation Rate")
        st.pyplot(fig)
        plt.close(fig)
        
        
    elif data["choice"] != "Overall":
        grouped = grouped_cancel_rate(df, data, column_map)

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(data=grouped, x=data["choice"], y="Cancellation Rate", ax=ax)
        ax.bar_label(
            ax.containers[0],
            labels=[f"{v:.0%}" for v in grouped["Cancellation Rate"]])
        plt.title(f"Cancellation Rate by {data["choice"]}")
        st.pyplot(fig)
        plt.close(fig)


def cancel_window_rate(hotel: str):
    df = create_cancel_profile(hotel)
    fig, ax = plt.subplots()
    sns.countplot(df, x="Cancel Window Bucket", ax=ax)
    plt.title("Number of bookings per cancellation window")
    st.pyplot(fig)


def cancel_value_rate(hotel: str):
    df= create_cancel_profile(hotel)
    fig, ax = plt.subplots()
    sns.violinplot(df, x="Cancel Window Bucket", y="Estimated Booking Value")
    plt.title("Estimated booking value by cancellation window")
    st.pyplot(fig)


def pps_features(df: pd.DataFrame):
    df = pps_predictions(df)
    fig, ax = plt.subplots()
    fig.suptitle("PPS against target")
    ax.set_ylabel("Feature")

    sns.barplot(data=df,
            x="ppscore",
            y="x")
    st.pyplot(fig)


def correlation_comparison(df: pd.DataFrame):
    df = correlations(df)
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.suptitle("Pearson vs Spearman Correlations")

    sns.barplot(
        data=df,
        x="Value",
        y="Feature",
        hue="Method",
        ax=ax)
    st.pyplot(fig)

