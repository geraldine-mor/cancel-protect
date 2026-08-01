import streamlit as st
import pandas as pd
import numpy as np
from src.data_management import load_data
from src.input_processing import build_input_df, input_df
from src.model import predict_cancellation

img_col1, img_col2 = st.columns(2)
with img_col1:
    st.image("images/CancelProtect_logo.svg", width="stretch")

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
col21, col22, col23 = st.columns(3)

df = load_data()

with col1:
    hotel = st.radio("Hotel", ["Resort Hotel", "City Hotel"])

with col2:
    arrival_date = st.date_input("Arrival Date", min_value="today")

with col3:
    los = st.number_input("Nights", min_value=1, max_value=100, format="%d")

with col4:
    adr = st.number_input("Price per night", min_value=0.0, format="%0.2f")

with col5:
    adults = st.number_input("Adults", min_value=1, max_value=4, step=1)

with col6:
    children = st.number_input("Children", min_value=0, max_value=4, step=1)

with col7:
    babies = st.number_input("Babies", min_value=0, max_value=3, step=1)

with col8:
    meal = st.selectbox("Meal Plan", ["Bed & Breakfast", "Half Board",
                                      "Full Board", "Room Only"])

with col9:
    values = pd.concat([pd.Series(["Unknown"]),
                        pd.Series(df["country"].dropna().unique())])
    country = st.selectbox("Country (if known)", options=values)

with col10:
    market_segment = st.selectbox(
        "Market Segment", ["Direct", "Corporate",
                           "Online TA", "Offline TA/TO",
                           "Complementary", "Groups"])

with col11:
    distribution_channel = st.selectbox(
        "Distribution Channel", ["Direct", "Corporate", "TA/TO", "GDS"])

with col12:
    customer_type = st.selectbox(
        "Customer Type", ["Transient", "Contract", "Group", "Transient-Party"])

with col13:
    special_requests = st.number_input(
        "Special Requests", min_value=0, max_value=10, step=1)

with col14:
    repeat = st.radio("Is this a repeat guest?", ["No", "Yes"])
    if repeat == "Yes":
        with col15:
            previous_cancellations = st.number_input(
                "Previous Cancellations", min_value=0, max_value=100, step=1)
        with col16:
            previous_completed_bookings = st.number_input(
                "Bookingss Not Cancelled", min_value=0, max_value=100, step=1)
    elif repeat == "No":
        previous_cancellations = 0
        previous_completed_bookings = 0

with col17:
    agency = st.radio("Is this an agency booking?", ["No", "Yes"])
    if agency == "Yes":
        agent_ids = pd.Series(df["agent"].dropna().unique()).sort_values()
        agent = st.selectbox("Agent ID", options=agent_ids)
    else:
        agent = np.nan

with col18:
    waitlist = st.radio("Was this guest waitlisted?", ["No", "Yes"])
    if waitlist == "Yes":
        waitlist_date = st.date_input("Date Waitlisted", max_value="today")
    elif waitlist == "No":
        waitlist_date = 0

with col19:
    city_rooms = ["Standard", "Superior", "Premium", "Standard Family",
                  "Superior Family", "Economy", "Other"]
    resort_rooms = ["Standard", "Superior", "Premium", "Deluxe",
                    "Other Db/Tw", "Standard Family", "Superior Family",
                    "Premium Family", "Other"]
    if hotel == "Resort Hotel":
        req_room = st.selectbox("Requested Room Type", resort_rooms)
    elif hotel == "City Hotel":
        req_room = st.selectbox("Requested Room Type", city_rooms)

with col20:
    parking = st.number_input(
        "Required Parking Spaces", min_value=0, max_value=3, step=1)


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
    "is_repeated_guest": repeat,
    "previous_cancellations": previous_cancellations,
    "previous_bookings_not_canceled": previous_completed_bookings,
    "required_car_parking_spaces": parking,
    "total_of_special_requests": special_requests,
    "waitlist": waitlist,
    "waitlist_date": waitlist_date
}

with col22:
    predict = st.button("**Predict**", type="primary", width="stretch")

if predict:
    data = build_input_df(inputs)

    prediction, probability = predict_cancellation(data)
    if prediction == 1:
        st.markdown(f":red-badge[This booking is expected to cancel, "
                    f" probability of cancellation is: {probability:.1%}]")
    elif prediction == 0:
        st.markdown(f":green-badge[This booking is not expeted to cancel, "
                    "it has a {probability:.1%} chance of cancellation]")

    st.dataframe(input_df(inputs))

    with st.expander(label="Model Ready Data"):
        st.dataframe(data)
