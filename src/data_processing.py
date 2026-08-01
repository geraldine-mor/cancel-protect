"""
Data preparation and analysis utilities for the CancelProtect dashboard.

Provides functions for preprocessing data, creating derived features,
calculating cancellation statistics, generating guest profiles, and
preparing data for visualisation and model evaluation.
"""

import numpy as np
import pandas as pd
import streamlit as st
import ppscore as pps
from src.data_management import load_raw, load_clean


@st.cache_data
def create_cancel_profile(hotel: str) -> pd.DataFrame:
    """
    Create a cancellation profile for cancelled bookings.

    Builds derived features describing the timing and value of cancelled
    bookings, optionally filtering to a specific hotel.

    Args:
        hotel: Hotel name or ``"Combined"`` to include both hotels.

    Returns:
        pandas.DataFrame: Cancellation profile containing engineered
        booking features.
    """
    df = load_raw()
    df = df[df["is_canceled"] == 1]
    FEATURE_ORDER = ["Hotel", "Arrival Month", "Stay Length", "Lead Time",
                     "Lead Time Bucket", "Cancelled Before Arrival",
                     "Cancel Window Bucket", "Estimated Booking Value",
                     "Cancelled After Booking", "Market Segment",
                     "Customer Type", "Lifecycle Completed"]

    cancel_df = pd.DataFrame({
        "Hotel": df["hotel"],
        "Market Segment": df["market_segment"],
        "Customer Type": df["customer_type"],
        "Arrival Month": df["arrival_date_month"],
        "Lead Time": df["lead_time"],
        "Stay Length": (
            df["stays_in_week_nights"] + df["stays_in_weekend_nights"]
            )
    })

    arrival_date = pd.to_datetime(
        df["arrival_date_year"].astype(str) + " " +
        df["arrival_date_month"].astype(str) + " " +
        df["arrival_date_day_of_month"].astype(str)
    )
    cancel_date = pd.to_datetime(df["reservation_status_date"])
    book_date = arrival_date - pd.to_timedelta(
        cancel_df["Lead Time"], unit="D")
    bins = [-np.inf, 7, 30, 90, np.inf]
    labels = ["Last Minute", "Short Range", "Mid Range", "Long Range"]

    df = df[((df["adr"] > 0) & (df["adr"] <= 1000))]
    cancel_df["Cancelled Before Arrival"] = (
        arrival_date - cancel_date).dt.days
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
    """
    Prepare booking data for visualisation.

    Cleans, bins, and formats selected features before returning the
    processed dataset and a mapping between display names and column
    names.

    Args:
        data: Dictionary containing the selected hotel and chart option.

    Returns:
        tuple[pandas.DataFrame, dict]: The processed dataset and column
        mapping.
    """

    df = load_clean()

    month_order = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November",
                   "December"]
    df["arrival_date_month"] = pd.Categorical(
        df["arrival_date_month"], categories=month_order, ordered=True)

    if data["hotel"] != "Combined":
        df = df[df["hotel"] == data["hotel"]]

    lead_time_bins = [0, 7, 30, 90, df["lead_time"].max() + 1]
    lead_time_labels = ["0-7 days", "8-30 days", "31-90 days", "90+ days"]
    df["lead_time_binned"] = pd.cut(
        df["lead_time"],
        bins=lead_time_bins,
        labels=lead_time_labels,
        right=False)

    adr_bins = [0, 50, 75, 100, 125, 150, 200, df["adr"].max() + 1]
    adr_labels = [
        "0-50", "51-75", "76-100", "101-125", "126-150", "151-200", "200+"]
    df["adr_binned"] = pd.cut(df["adr"], bins=adr_bins, labels=adr_labels)

    df["stay_length"] = (
        df["stays_in_week_nights"] + df["stays_in_weekend_nights"])

    stay_bins = [0, 1, 2, 3, 7, 14, 30, df["stay_length"].max() + 1]
    stay_labels = ["1", "2", "3", "4-7", "8-14", "15-30", "30+"]

    df["stay_length_binned"] = pd.cut(
        df["stay_length"], bins=stay_bins, labels=stay_labels, right=True
    )

    top_countries = df["country"].value_counts().head(10).index
    df["country"] = df["country"].where(
        df["country"].isin(top_countries), "Other")

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
    """
    Calculate the overall cancellation rate.

    Args:
        df: Hotel bookings dataset.

    Returns:
        pandas.DataFrame: Cancellation rates for cancelled and
        non-cancelled bookings.
    """

    rate_df = (
        df["is_canceled"]
        .value_counts(normalize=True)
        .rename(index={0: "Not Cancelled", 1: "Cancelled"})
        .reset_index()
        )
    rate_df.columns = ["Status", "Cancellation Rate"]
    return rate_df


def grouped_cancel_rate(
        df: pd.DataFrame, data: dict, column_map: dict) -> pd.DataFrame:
    """
    Calculate cancellation rates grouped by a selected feature.

    Args:
        df: Processed bookings dataset.
        data: User selections including the grouping feature.
        column_map: Mapping of display names to column names.

    Returns:
        pandas.DataFrame: Cancellation rate for each group.
    """

    col = column_map[data["choice"]]
    grouped = (
        df.groupby(col, observed=True)["is_canceled"]
        .mean()
        .reset_index()
    )
    grouped.columns = [data["choice"], "Cancellation Rate"]
    return grouped


def generate_chart_text(data: dict) -> str:
    """
    Generate a narrative summary of cancellation trends.

    Creates descriptive text highlighting overall or grouped
    cancellation rates for the selected hotel and feature.

    Args:
        data: Dictionary containing the selected hotel and chart option.

    Returns:
        str: Summary of the observed cancellation rates.
    """
    df, col_map = data_prep(data)
    rate_df = overall_cancel_rate(df)

    text_templates = {
        "Market Segment": "the '{top_cat}' segment shows the highest"
        " cancellation rate at {top_rate:.0%}, compared to '{bottom_cat}'"
        " at {bottom_rate:.0%}.",
        "Customer Type": "'{top_cat}' bookings cancel most frequently "
        "({top_rate:.0%}), while '{bottom_cat}' bookings are the most "
        "reliable ({bottom_rate:.0%}).",
        "Lead Time": "cancellation rate increases with lead time, peaking "
        "at {top_rate:.0%} for bookings made '{top_cat}' in advance.",
        "Distribution Channel": "the '{top_cat}' channel has the highest "
        "cancellation rate at {top_rate:.0%}.",
        "Arrival Month": "'{top_cat}' sees the highest cancellation rate "
        "({top_rate:.0%}), compared to a low of '{bottom_rate:.0%}' in"
        " {bottom_cat}.",
        "Stay Length": "stays of '{top_cat}' nights show the highest "
        "cancellation rate at {top_rate:.0%}.",
        "ADR": "Bookings in the '{top_cat}' price band cancel most "
        "at {top_rate:.0%}.",
        "Deposit Type": "'{top_cat}' deposit bookings show a markedly "
        "higher cancellation rate ({top_rate:.0%}) than '{bottom_cat}'"
        " bookings ({bottom_rate:.0%}). This pattern is examined "
        "further in the Hypothesis Validation page.",
        "Nationality": " customers from '{top_cat}' cancel the"
        " most at {top_rate:.0%}"
        }
    if data["hotel"] == "Combined":
        hotel_phrase = "Across both hotels, "
    else:
        hotel_phrase = f"At the {data["hotel"]}, "

    rate = rate_df.loc[
        rate_df["Status"] == "Cancelled", "Cancellation Rate"].iloc[0]
    if data["choice"] == "Overall":
        return (
            f"{hotel_phrase} the overall cancellation rate is {rate:.0%}")
    else:
        grouped_df = grouped_cancel_rate(df, data, col_map)
        sorted_df = grouped_df.sort_values(
            "Cancellation Rate", ascending=False)
        top_cat, top_rate = (
            sorted_df.iloc[0][data["choice"]],
            sorted_df.iloc[0]["Cancellation Rate"])
        bottom_cat, bottom_rate = (
            sorted_df.iloc[-1][data["choice"]],
            sorted_df.iloc[-1]["Cancellation Rate"])

        template = text_templates.get(
            data["choice"], f"Cancellation rate varies by {data["choice"]}")
        body = template.format(
            rate=rate, top_cat=top_cat,
            top_rate=top_rate, bottom_cat=bottom_cat, bottom_rate=bottom_rate
        )

    return f"{hotel_phrase}{body}"


def group_nationality(df: pd.DataFrame) -> pd.Series:
    """Group guests as domestic or international."""
    return np.where(df["country"] == "PRT", "Domestic (PRT)", "International")


def group_lead_time(df: pd.DataFrame) -> pd.Series:
    """Bin lead time into categorical booking windows."""
    lead_time_bins = [0, 7, 30, 90, df["lead_time"].max() + 1]
    lead_time_labels = ["0-7 days", "8-30 days", "31-90 days", "90+ days"]
    df["lead_time_binned"] = pd.cut(
        df["lead_time"],
        bins=lead_time_bins,
        labels=lead_time_labels,
        right=False)
    return df["lead_time_binned"]


def group_repeat_guest(df: pd.DataFrame) -> pd.Series:
    """Label bookings by repeat guest status."""
    return df["is_repeated_guest"].map({0: "No", 1: "Yes"})


def group_prior_cancellations(df: pd.DataFrame) -> pd.Series:
    """Group guests by previous cancellation history."""
    return np.where(df["previous_cancellations"] > 0, "1+", "0")


def group_market_segment(df: pd.DataFrame) -> pd.Series:
    """Return the booking market segment."""
    return df["market_segment"]


def group_additional_needs(df: pd.DataFrame) -> pd.Series:
    """Group bookings by whether additional guest needs were requested."""
    has_needs = (
        (df["total_of_special_requests"] > 0) | (
            df["required_car_parking_spaces"] > 0))
    return np.where(has_needs, "Yes", "No")


def build_guest_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Create a guest profile summary table.

    Summarises cancellation rates and booking proportions across
    selected guest characteristics.

    Args:
        df: Hotel bookings dataset.

    Returns:
        pandas.io.formats.style.Styler: Styled summary table.
    """

    fields = {
        "Nationality": group_nationality,
        "Lead Time": group_lead_time,
        "Market Segment": group_market_segment,
        "Repeat Guest": group_repeat_guest,
        "Prior Cancellations": group_prior_cancellations,
        "Additional Needs": group_additional_needs,
    }
    rows = []
    for label, group_fn in fields.items():
        summary = (
            df.assign(_group=group_fn(df))
            .groupby("_group", observed=True)["is_canceled"]
            .agg(["mean", "count"])
            .reset_index()
        )
        summary["% of Total Bookings"] = summary["count"] / len(df)
        summary.insert(0, "Characteristic", label)
        summary.columns = ["Characteristic", "Group", "Cancellation Rate",
                           "Bookings", "% of Total Bookings"]
        rows.append(summary)

    guest_profile = pd.concat(
        rows, ignore_index=True).style.background_gradient(cmap="Blues")
    guest_profile = guest_profile.format({
        "Cancellation Rate": "{:.0%}",
        "% of Total Bookings": "{:.0%}"
    })

    return guest_profile


# Copied from notebook 05_correlation_study
def pps_predictions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Predictive Power Scores for each feature.

    Args:
        df: Hotel bookings dataset.

    Returns:
        pandas.DataFrame: Features ranked by Predictive Power Score.
    """

    pps_df = df.copy()

    pps_df["is_canceled"] = pps_df["is_canceled"].astype("category")

    pps_predict = pps.predictors(pps_df, y="is_canceled", sample=None)
    pps_predict.sort_values(by="ppscore", ascending=False)
    pps_plot_df = pps_predict[pps_predict["ppscore"] > 0].sort_values(
        by="ppscore", ascending=False)

    return pps_plot_df


def correlations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare Pearson and Spearman correlations.

    Args:
        df: Hotel bookings dataset.

    Returns:
        pandas.DataFrame: Correlation coefficients in long format.
    """

    numeric_features = ["lead_time", "stays_in_weekend_nights",
                        "stays_in_week_nights", "adults",
                        "children", "babies",
                        "previous_cancellations",
                        "previous_bookings_not_canceled",
                        "days_in_waiting_list", "adr",
                        "required_car_parking_spaces",
                        "total_of_special_requests"]

    corr_df = df[["is_canceled", *numeric_features]]

    comparison = pd.DataFrame({
        "Pearson": corr_df.corr(method="pearson")["is_canceled"],
        "Spearman": corr_df.corr(method="spearman")["is_canceled"],
    }).drop(index="is_canceled")

    return (
        comparison
        .reset_index(names="Feature")
        .melt(
            id_vars="Feature",
            var_name="Method",
            value_name="Value",
        )
    )


def hypothesis_1_crosstab(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate cancellation rates by deposit type.

    Args:
        df: Hotel bookings dataset.

    Returns:
        pandas.DataFrame: Normalised crosstab of deposit type and
        cancellation stat
    """

    h1_df = pd.crosstab(
        df["deposit_type"], df["is_canceled"], normalize="index")
    h1_df.columns = ["not_canceled", "canceled"]

    return h1_df


def hypothesis_2_crosstab(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate cancellation rates across lead time bands.

    Args:
        df: Hotel bookings dataset.

    Returns:
        pandas.DataFrame: Normalised crosstab of lead time band and
        cancellation status.
    """

    bins = [-np.inf, 7, 30, 90, np.inf]
    lead_time = pd.cut(df["lead_time"],
                       bins, labels=["Last Minute", "Short Range",
                                     "Mid Range", "Long Range"])

    df["lead_time"] = lead_time
    h2_df = pd.crosstab(df["lead_time"], df["is_canceled"], normalize="index")
    h2_df.columns = ["not_canceled", "canceled"]

    return h2_df


def hypothesis_3_crosstab(
        df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Compare Direct and Online TA booking cancellations.

    Args:
        df: Hotel bookings dataset.

    Returns:
        tuple[pandas.DataFrame, pandas.DataFrame]: Crosstab of
        cancellation rates and the filtered dataset.
    """

    features = ["Online TA", "Direct"]
    ota_direct = df[df["market_segment"].isin(features)]

    h3_df = pd.crosstab(
        ota_direct["market_segment"],
        ota_direct["is_canceled"], normalize="index")
    h3_df.columns = ["Not Cancelled", "Cancelled"]

    return h3_df, ota_direct


def classification_report_table(data: dict) -> pd.DataFrame:
    """
    Format classification report metrics as a table.

    Args:
        data: Classification report dictionary.

    Returns:
        pandas.DataFrame: Reformatted classification report.
    """

    data = data.copy()
    accuracy = data.pop("accuracy")

    df = pd.DataFrame(data).transpose()

    total_suport = df.loc["weighted avg", "support"]
    df.loc["accuracy"] = [None, None, accuracy, total_suport]

    row_order = ["Not Cancelled", "Cancelled",
                 "accuracy", "macro avg", "weighted avg"]
    df = df.reindex(row_order)

    return df
