import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import matplotlib.ticker as mticker
from utils.data_management import load_feature_importance
from utils.data_processing import (
    data_prep, overall_cancel_rate, 
    grouped_cancel_rate, create_cancel_profile,
    pps_predictions, correlations, hypothesis_1_crosstab,
    hypothesis_2_crosstab, hypothesis_3_crosstab)

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


def hypothesis_bar_plot(df: pd.DataFrame):
    h1_df = hypothesis_1_crosstab(df)

    fig, ax = plt.subplots()
   
    h1_df.plot(kind="bar", ax=ax)
    ax.yaxis.set_major_formatter(
        mticker.PercentFormatter(xmax=1, decimals=0))
    ax.set_title("Cancellation Rate by Deposit Type")
    plt.xticks(rotation=0)
    st.pyplot(fig)


def hypothesis_2_plot(df: pd.DataFrame):
    h2_df = hypothesis_2_crosstab(df)

    fig, ax = plt.subplots()

    h2_df.plot(kind="bar", ax=ax)
    ax.yaxis.set_major_formatter(
        mticker.PercentFormatter(xmax=1, decimals=0))
    ax.set_title("Cancellation Rate by Lead Time Band")
    plt.xticks(rotation=0)
    st.pyplot(fig)


def hypothesis_3_plot(df: pd.DataFrame):
    h3_df, ota_direct = hypothesis_3_crosstab(df)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    h3_df.plot(kind="bar", ax=ax1)
    ax1.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
    ax1.axhline(y=df["is_canceled"].mean(), linestyle="--", color="black",
                label="Overall cancellation rate")
    ax1.legend()
    ax1.set_title("Cancellation Rate Direct and Online TA")
    ax1.tick_params(axis="x", labelrotation=0)
    ax1.set_ylabel("Cancellation Rate")
    ax1.set_xlabel("Market Segment")

    sns.countplot(data=ota_direct, x="market_segment",
                  hue="is_canceled", ax=ax2)
    ax2.set_title("Total Bookings Direct and Online TA")
    ax2.set_ylabel("Number of Bookings")
    ax2.set_xlabel("Market Segment")
    ax2.legend(
        title="Booking Status",
        labels=["Not Cancelled", "Cancelled"]
    )

    plt.tight_layout()
    st.pyplot(fig)


def plot_confusion_matrix(tn, fp, fn, tp, title):
    cm = np.array([[tn, fp], [fn, tp]])

    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt="d", cmap="winter",
                xticklabels=["Not Cancelled", "Cancelled"],
                yticklabels=["Not Cancelled", "Cancelled"],
                ax=ax)

    ax.set_title(title)
    ax.set_ylabel("Actual")
    ax.set_xlabel("Predicted")
    return fig


def plot_feature_importance():
    df = load_feature_importance()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=df.head(15), x="Importance", y="Feature", ax=ax)
    plt.title("Top 15 Feature Importances — Cancellation Prediction")
    st.pyplot(fig)