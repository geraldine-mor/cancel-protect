import pandas as pd
import numpy as np

FEATURE_ORDER = ['hotel', 'lead_time', 'arrival_date_year',
                 'arrival_date_month', 'arrival_date_week_number',
                 'arrival_date_day_of_month', 'stays_in_weekend_nights',
                 'stays_in_week_nights', 'adults', 'children', 'babies',
                 'meal', 'country', 'market_segment', 'distribution_channel',
                 'is_repeated_guest', 'previous_cancellations',
                 'previous_bookings_not_canceled', 'reserved_room_type',
                 'assigned_room_type', 'booking_changes', 'deposit_type',
                 'agent', 'company', 'days_in_waiting_list', 'customer_type',
                 'adr', 'required_car_parking_spaces', 'total_of_special_requests']

DROP_COLS = ["arrival_date_year", "arrival_date_week_number", "company", "deposit_type"]

# Build input dataframe from inputs
def build_input_df(raw_inputs: dict) -> pd.DataFrame:
    df = pd.DataFrame([raw_inputs])

    # Derive features
    # lead_time, arrival_date_month and arrival_date_day_of_month from arrival date
    # stays_in_weekend_nights and stays_in_week_nights from arrival date and LOS
    # New bookings don't have waitlist or changes yet
    df['booking_changes']  = 0
    df['days_in_waiting_list'] = 0

    return df