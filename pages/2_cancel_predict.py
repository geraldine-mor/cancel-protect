import streamlit as st
import pandas as pd
from utils.data_management import load_data
from utils.input_processing import build_input_df

st.image("images/CancelProtect_logo.svg", use_container_width=True)

st.title("Cancellation Predictor")

st.markdown("""
:blue-badge[Please enter values in **each** of the below fields:]
""")

# Create columns to hold and space the input widgets
col1, col2, col3, col4, = st.columns(4)
col5, col6, col7, col8 = st.columns(4)
col9, col10, col11, col12 = st.columns(4)
col13, col14, col15, col16 = st.columns(4)
col17, col18, col19, col20 = st.columns(4)

df = load_data()

with col1:
    hotel = st.radio("Hotel", ["Resort Hotel", "City Hotel"])

with col2:
    arrival_date = st.date_input("Arrival Date", min_value="today")

with col3:
    los = st.number_input("Nights", min_value=1, max_value=100, format="%d")

with col4:
    adr = st.number_input("Price per night", format="%0.2f")
   
with col5:
    adults = st.number_input("Adults", min_value=1, max_value=4, step=1)
    
with col6:
    children = st.number_input("Children", min_value=0, max_value=4, step=1)

with col7:
    babies = st.number_input("Babies", min_value=0, max_value=3, step=1)

with col8:
    meal = st.selectbox("Meal Plan", ["Bed & Breakfast", "Half Board", "Full Board", "Room Only"])

with col9:
    values = pd.concat([pd.Series(["Unknown"]), pd.Series(df["country"].dropna().unique())])
    country = st.selectbox("Country (if known)", options=values)

with col10:
    market_segment = st.selectbox("Market Segment", ["Direct", "Corporate", "Online TA", "Offline TA/TO", "Complementary", "Groups"])

with col11:
    distribution_channel = st.selectbox("Distribution Channel", ["Direct", "Corporate", "TA/TO", "GDS"])

with col12:
    customer_type = st.selectbox("Customer Type", ["Transient", "Contract", "Group", "Transient-Party"])

with col13:
    special_requests = st.number_input("Special Requests", min_value=0, max_value=10, step=1)

with col14:
    req_room = st.selectbox("Requested Room Type", df["reserved_room_type"].unique()) # Check on excel sheet if Resort & City hotels have non-shared room types
    # If so conditional to display appropriate room types
    # Create dummy names for the room types and map to letter categories

with col15:
    ass_room = st.selectbox("Allocated Room Type", df["assigned_room_type"].unique())

with col16:
    parking = st.number_input("Required Parking Spaces", min_value=0, max_value=3, step=1)

with col17:
    agency = st.radio("Is this an agency booking?", ["No", "Yes"])
    if agency == "Yes":
        agent = st.number_input("Agent ID", min_value=1, max_value=df["agent"].max().astype("int64"))
    else:
        agent = 0

with col18:
    repeat = st.radio("Is this a repeat guest?", ["No", "Yes"])
    if repeat == "Yes":
        with col19:
            previous_cancellations = st.number_input(
                "Previous Cancellations", min_value=0, max_value=100, step=1)
        with col20:
            previous_completed_bookings = st.number_input(
                "Bookingss Not Cancelled", min_value=0, max_value=100, step=1)
    elif repeat == "No":
        previous_cancellations = 0
        previous_completed_bookings = 0

inputs = {
    "hotel": hotel,
    "arrival_date": arrival_date,
    "los": los,
    "adr": adr,
    "adults": adults,
    "children": children,
    "babies": babies,
    "meal": meal,
    "country": country,
    "market_segment": market_segment,
    "distribution_channel": distribution_channel,
    "customer_type": customer_type,
    "agent": agent,
    "reserved_room_type": req_room,
    "assigned_room_type": ass_room,
    "is_repeated_guest": repeat,
    "previous_cancellations": previous_cancellations,
    "previous_bookings_not_canceled": previous_completed_bookings,
    "required_car_parking_spaces": parking,
    "total_of_special_requests": special_requests
}

st.dataframe(build_input_df(inputs))