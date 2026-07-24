import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from utils.data_management import load_raw, load_clean

def create_cancel_profile(hotel: str) -> pd.DataFrame:
    df = load_raw()
    df = df[df["is_canceled"] == 1]
    FEATURE_ORDER = ["Hotel", "Arrival Month", "Stay Length", "Lead Time",
                     "Lead Time Bucket", "Cancelled Before Arrival", 
                     "Cancel Window Bucket", "Estimated Booking Value", 
                     "Cancelled After Booking", "Market Segment", "Customer Type",
                     "Lifecycle Completed"]

    cancel_df = pd.DataFrame({
        "Hotel": df["hotel"],
        "Market Segment": df["market_segment"],
        "Customer Type": df["customer_type"],
        "Arrival Month": df["arrival_date_month"],
        "Lead Time": df["lead_time"],
        "Stay Length": df["stays_in_week_nights"] + df["stays_in_weekend_nights"],
    })

    arrival_date = pd.to_datetime(
        df["arrival_date_year"].astype(str) + " " +
        df["arrival_date_month"].astype(str) + " " +
        df["arrival_date_day_of_month"].astype(str)
    )
    cancel_date = pd.to_datetime(df["reservation_status_date"])
    book_date = arrival_date - pd.to_timedelta(cancel_df["Lead Time"], unit="D")
    bins = [-np.inf, 7, 30, 90, np.inf]
    labels = ["Last Minute", "Short Range", "Mid Range", "Long Range"]

    df["adr"] = df["adr"].drop(df[((df["adr"] < 0) | (df["adr"] > 1000))].index)
    cancel_df["Cancelled Before Arrival"] = (arrival_date - cancel_date).dt.days
    cancel_df["Cancelled After Booking"] = (cancel_date - book_date).dt.days
    cancel_df["Estimated Booking Value"] = df["adr"] * cancel_df["Stay Length"]
    cancel_df["Lead Time Bucket"] = pd.cut(
        cancel_df["Lead Time"], bins, labels=labels
    )
    cancel_df["Cancel Window Bucket"] = pd.cut(
        cancel_df["Cancelled Before Arrival"], bins, labels=labels
    )

    # Calculate the booking lifecycle
    # Same day arrivals have no measurable lifecycle, treat as fully elapsed 
    cancel_df["Lifecycle Completed"] = np.where(
        cancel_df["Lead Time"] > 0,
        cancel_df["Cancelled After Booking"] / cancel_df["Lead Time"],
        1.0)
    if hotel != "Combined":
        return cancel_df[cancel_df["Hotel"] == hotel]
    else:
        return cancel_df[FEATURE_ORDER]


def data_prep(data: dict) -> tuple[pd.DataFrame, dict]:
    df = load_clean()
    
    month_order = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
    df["arrival_date_month"] = pd.Categorical(
        df["arrival_date_month"], categories=month_order, ordered=True)
    
    if data["hotel"] != "Combined":
        df = df[df["hotel"] == data["hotel"]]
    
    lead_time_bins = [0, 7, 30, 90, df["lead_time"].max() + 1]
    lead_time_labels = ["0-7 days", "8-30 days", "31-90 days", "90+ days"]
    df["lead_time_binned"] = pd.cut(
        df["lead_time"], bins=lead_time_bins, labels=lead_time_labels, right=False)

    adr_bins = [0, 50, 75, 100, 125, 150, 200, df["adr"].max() + 1]
    adr_labels = ["0-50", "51-75", "76-100", "101-125", "126-150", "151-200", "200+"]
    df["adr_binned"] = pd.cut(df["adr"], bins=adr_bins, labels=adr_labels)
    
    df["stay_length"] = df["stays_in_week_nights"] + df["stays_in_weekend_nights"]
    
    stay_bins = [0, 1, 2, 3, 7, 14, 30, df["stay_length"].max() + 1]
    stay_labels = ["1", "2", "3", "4-7", "8-14", "15-30", "30+"]
    
    df["stay_length_binned"] = pd.cut(
        df["stay_length"], bins=stay_bins, labels=stay_labels, right=True
    )

    top_countries = df["country"].value_counts().head(10).index
    df["country"] = df["country"].where(df["country"].isin(top_countries), "Other")
    
    column_map = {
        "Market Segment": "market_segment",
        "Customer Type": "customer_type",
        "Distribution Channel": "distribution_channel",
        "Arrival Month": "arrival_date_month",
        "Lead Time": "lead_time_binned",
        "ADR": "adr_binned",
        "Stay Length": "stay_length_binned",
        "Deposit Type": "deposit_type",
        "Nationality": "country"
    }
    
    return df, column_map


def overall_cancel_rate(df: pd.DataFrame) -> pd.DataFrame:
    rate_df = (
        df["is_canceled"]
        .value_counts(normalize=True)
        .rename(index={0: "Not Cancelled", 1: "Cancelled"})
        .reset_index()
        )
    rate_df.columns = ["Status", "Cancellation Rate"]
    return rate_df


def grouped_cancel_rate(df: pd.DataFrame, data: dict, column_map: dict) -> pd.DataFrame:
    col = column_map[data["choice"]]
    grouped = (
        df.groupby(col, observed=True)["is_canceled"]
        .mean()
        .reset_index()
    )
    grouped.columns = [data["choice"], "Cancellation Rate"]
    return grouped


def generate_chart_text(data: dict) -> str:
    df, col_map = data_prep(data)
    rate_df = overall_cancel_rate(df)

    text_templates = {
        "Market Segment": "the '{top_cat}' segment shows the highest cancellation rate at {top_rate:.0%}, "
                        "compared to '{bottom_cat}' at {bottom_rate:.0%}.",
        "Customer Type": " '{top_cat}' bookings cancel most frequently ({top_rate:.0%}), "
                        "while '{bottom_cat}' bookings are the most reliable ({bottom_rate:.0%}).",
        "Lead Time": "cancellation rate increases with lead time, peaking at {top_rate:.0%} "
                    "for bookings made '{top_cat}' in advance.",
        "Distribution Channel": "the '{top_cat}' channel has the highest cancellation rate at {top_rate:.0%}.",
        "Arrival Month": "'{top_cat}' sees the highest cancellation rate ({top_rate:.0%}), "
                        "compared to a low of '{bottom_rate:.0%}' in {bottom_cat}.",
        "Stay Length": "stays of '{top_cat}' nights show the highest cancellation rate at {top_rate:.0%}.",
        "ADR": "Bookings in the '{top_cat}' price band cancel most at {top_rate:.0%}.",
        "Deposit Type": " '{top_cat}' deposit bookings show a markedly higher cancellation rate "
                        "({top_rate:.0%}) than '{bottom_cat}' bookings ({bottom_rate:.0%}). "
                        "This pattern is examined further in the Project Hypotheses page.",
        "Nationality": " customers from '{top_cat}' cancel the most at {top_rate:.0%}"
        }
    if data["hotel"] == "Combined":
        hotel_phrase = "Across both hotels, "
    else:
        hotel_phrase = f"At the {data["hotel"]}, " 

    rate = rate_df.loc[rate_df["Status"] == "Cancelled", "Cancellation Rate"].iloc[0]
    if data["choice"] == "Overall":
        return f"{hotel_phrase} the overall cancellation rate is {rate:.0%}"
    else:
        grouped_df = grouped_cancel_rate(df, data, col_map)
        sorted_df = grouped_df.sort_values("Cancellation Rate", ascending=False)
        top_cat, top_rate = sorted_df.iloc[0][data["choice"]], sorted_df.iloc[0]["Cancellation Rate"]
        bottom_cat, bottom_rate = sorted_df.iloc[-1][data["choice"]], sorted_df.iloc[-1]["Cancellation Rate"]

        template = text_templates.get(data["choice"], f"Cancellation rate varies by {data["choice"]}")
        body = template.format(
            rate=rate, top_cat=top_cat,
            top_rate=top_rate, bottom_cat=bottom_cat, bottom_rate=bottom_rate
        )

    return f"{hotel_phrase}{body}"
