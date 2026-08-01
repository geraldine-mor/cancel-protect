"""
Feature preparation utilities for hotel booking prediction models.

This module contains helper functions for transforming raw user booking
inputs into a pandas DataFrame formatted for model inference. It performs
feature engineering, including date-based calculations, categorical encoding,
and alignment of input features with the model's expected feature order.
"""

import pandas as pd
import numpy as np
from datetime import date

FEATURE_ORDER = ['hotel', 'lead_time', 'arrival_date_year',
                 'arrival_date_month', 'arrival_date_week_number',
                 'arrival_date_day_of_month', 'stays_in_weekend_nights',
                 'stays_in_week_nights', 'adults', 'children', 'babies',
                 'meal', 'country', 'market_segment', 'distribution_channel',
                 'is_repeated_guest', 'previous_cancellations',
                 'previous_bookings_not_canceled', 'reserved_room_type',
                 'deposit_type', 'agent', 'company', 'days_in_waiting_list',
                 'customer_type', 'adr', 'required_car_parking_spaces',
                 'total_of_special_requests']

DROP_COLS = ["arrival_date_year", "arrival_date_week_number",
             "company", "deposit_type"]


# Build input dataframe from inputs
def build_input_df(raw_inputs: dict) -> pd.DataFrame:
    """
    Build a model-ready input DataFrame from raw booking inputs.

    This function transforms raw booking information into the feature format
    expected by the prediction model. It derives date-related features,
    converts categorical values into training-compatible codes, handles
    missing values, removes unused input fields, and orders columns according
    to the model's required feature order.

    Args:
        raw_inputs (dict): Raw booking information containing fields such as
            arrival_date, hotel, meal, country, reserved_room_type, length of
            stay, and guest details.

    Returns:
        pd.DataFrame: A single-row DataFrame containing engineered features
        arranged in the order required by the prediction model.
    """
    df = pd.DataFrame([raw_inputs])

    # Derive features
    df["lead_time"] = (raw_inputs["arrival_date"] - date.today()).days
    df['arrival_date_month'] = raw_inputs['arrival_date'].strftime("%B")
    df['arrival_date_day_of_month'] = raw_inputs['arrival_date'].day
    df['stays_in_week_nights'], df['stays_in_weekend_nights'] = (
        midweek_weekend_nights(raw_inputs['arrival_date'], raw_inputs["los"]))

    if raw_inputs["waitlist"] == "No":
        df["days_in_waiting_list"] = 0
    elif raw_inputs["waitlist"] == "Yes":
        df['days_in_waiting_list'] = (
            date.today() - raw_inputs["waitlist_date"]).days
    # Change format to match training data
    df["meal"] = meal_code(raw_inputs["meal"])
    df["reserved_room_type"] = room_code(
        raw_inputs["hotel"], raw_inputs["reserved_room_type"])

    if raw_inputs["country"] == "Unknown":
        df["country"] = np.nan

    if raw_inputs["is_repeated_guest"] == "No":
        df["is_repeated_guest"] = 0
    elif raw_inputs["is_repeated_guest"] == "Yes":
        df['is_repeated_guest'] = 1
    df[DROP_COLS] = np.nan
    df = df.drop(columns=["arrival_date", "los"])

    return df[FEATURE_ORDER]


# Calculate midweek and weekend nights from arrival date and LOS
def midweek_weekend_nights(
        arrival_date: pd.Timestamp, los: int) -> tuple[int, int]:
    """
    Calculate the number of weekday and weekend nights for a stay.

    Iterates through each night of the booking period and counts nights
    occurring on weekdays versus Saturdays and Sundays.

    Args:
        arrival_date (pd.Timestamp): Guest arrival date.
        los (int): Length of stay in nights.

    Returns:
        tuple: A tuple containing:
            - midweek_nights (int): Number of weekday nights.
            - weekend_nights (int): Number of weekend nights.
    """

    weekend_nights = 0
    midweek_nights = 0
    for i in range(los):
        day_of_week = (arrival_date + pd.Timedelta(days=i)).weekday()
        if day_of_week in [5, 6]:  # Saturday or Sunday
            weekend_nights += 1
        else:
            midweek_nights += 1
    return midweek_nights, weekend_nights


# Convert meal plan to meal codes
def meal_code(meal_plan: str) -> str:
    """
    Convert a meal plan description into the corresponding model code.

    Maps human-readable meal plan names to the abbreviated codes used in the
    training dataset.

    Args:
        meal_plan (str): Meal plan description provided by the user.

    Returns:
        str: Encoded meal plan value. Returns "Undefined" if the meal plan is
        not recognised.
    """

    if meal_plan == "Bed & Breakfast":
        return "BB"
    elif meal_plan == "Half Board":
        return "HB"
    elif meal_plan == "Full Board":
        return "FB"
    elif meal_plan == "Room Only":
        return "SC"
    else:
        return "Undefined"


# Convert reserved room type to letter code
def room_code(hotel: str, room_type: str) -> str:
    """
    Convert a room type description into the corresponding model code.

    Room type mappings differ between City Hotel and Resort Hotel, so the
    appropriate mapping dictionary is selected based on the hotel type.

    Args:
        hotel (str): Hotel category, either City Hotel or Resort Hotel.
        room_type (str): Human-readable reserved room type.

    Returns:
        str: Encoded room type letter used by the model.

    Raises:
        KeyError: If the provided room type does not exist for the specified
            hotel category.
    """

    resort_rooms = {
        "Standard": "A", "Other Db/Tw": "B",
        "Standard Family": "C", "Superior": "D",
        "Premium": "E", "Deluxe": "F",
        "Superior Family": "G", "Premium Family": "H",
        "Other": "L"
    }

    city_rooms = {
        "Standard": "A", "Economy": "B",
        "Other": "C", "Superior": "D",
        "Premium": "E", "Standard Family": "F",
        "Superior Family": "G"
    }

    if hotel == "City Hotel":
        return city_rooms[room_type]
    elif hotel == "Resort Hotel":
        return resort_rooms[room_type]


def input_df(data: dict) -> pd.DataFrame:
    """Convert the inputs into a readable dataframe"""
    return pd.DataFrame([data])
