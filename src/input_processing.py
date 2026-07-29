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

DROP_COLS = ["arrival_date_year", "arrival_date_week_number", "company", "deposit_type"]

# Build input dataframe from inputs
def build_input_df(raw_inputs: dict) -> pd.DataFrame:
    df = pd.DataFrame([raw_inputs])

    # Derive features
    df["lead_time"] = (raw_inputs["arrival_date"] - date.today()).days
    df['arrival_date_month'] = raw_inputs['arrival_date'].strftime("%B")
    df['arrival_date_day_of_month'] = raw_inputs['arrival_date'].day
    df['stays_in_week_nights'], df['stays_in_weekend_nights'] = midweek_weekend_nights(
        raw_inputs['arrival_date'], raw_inputs["los"])

    if raw_inputs["waitlist"] == "No":
        df["days_in_waiting_list"] = 0
    elif raw_inputs["waitlist"] == "Yes":
        df['days_in_waiting_list'] = (date.today() - raw_inputs["waitlist_date"]).days
    # Change format to match training data
    df["meal"] = meal_code(raw_inputs["meal"])
    df["reserved_room_type"] = room_code(raw_inputs["hotel"], raw_inputs["reserved_room_type"])
    
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
def midweek_weekend_nights(arrival_date: pd.Timestamp, los: int) -> tuple:
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
def meal_code(meal_plan: str):
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
def room_code(hotel: str, room_type: str):
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