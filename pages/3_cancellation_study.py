import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utils.data_management import load_data
from utils.data_processing import create_cancel_profile, generate_chart_text
from utils.charts import cancellation_charts, cancel_window_rate, cancel_value_rate

img_col1, img_col2 = st.columns(2)
with img_col1:
    st.image("images/CancelProtect_logo.svg", width="stretch")

st.title("Cancellation Study")

cancellation_profile = create_cancel_profile("Combined")
clean_df = load_data()

kpi_container = st.container(border=True)
kpi_container.header("KPIs")
kpi_container.write(
f"* Total bookings analysed: {len(clean_df)}\n"
f"* Overall Cancellation Rate: {clean_df["is_canceled"].mean():.0%}\n"
f"* Average Room Revenue Per Cancelled Booking: €{
    cancellation_profile["Estimated Booking Value"].mean():.2f}\n"
)

main_container = st.container(border=False)
main_container.header("Cancellation Rate Comparison")
col1, col2 = main_container.columns([1, 3])

with col1:
    radio_container = st.container(border=True, height="stretch")
    hotel = radio_container.radio("Select Hotel:", ["Combined", "City Hotel", "Resort Hotel"])
    radio_container.markdown("---")
    choice = radio_container.radio("Cancellation rate by:", [
        "Overall", "Market Segment", "Customer Type", "Lead Time", 
        "Distribution Channel", "Arrival Month", "Stay Length", "ADR",
        "Deposit Type", "Nationality"
    ])

selection = {
    "hotel": hotel,
    "choice": choice
}

with col2:
    chart_container = st.container(border=True)
    with chart_container:
        cancellation_charts(selection)

text_container = main_container.container(border=True)
text_container.write(generate_chart_text(selection))

with st.expander(label="Cancellation Timing & Value"):
    col1, col2 = st.columns(spec=2, gap="medium")
    select_hotel = st.pills("Choose Property:", ["Combined", "City Hotel", "Resort Hotel"], default="Combined")
    with col1:
        cancel_window_rate(select_hotel)

    with col2:
        cancel_value_rate(select_hotel)

    st.write("""
            Cancellation volume rises steadily with notice window across both
             properties - long-range cancellations (90+ days out) are the most
             common. Booking value is broadly similar across windows, though
             short- and long-range cancellations include a higher share of high-value
             outliers than last-minute ones.

            At the City Hotel, cancellation volume rises steadily with notice window,
             with long-range cancellations most common. Booking value stays fairly
             consistent across windows. If anything, long-range cancellations trend
             slightly lower in value than short- or mid-range ones, so City Hotel's
             furthest-out cancellations aren't generally its costliest.

            At the Resort Hotel, cancellation volume rises steadily with notice window,
             with long-range cancellations most common. Unlike City Hotel, booking value
             here increases with notice window too - long-range cancellations show the
             widest spread and the highest-value outliers of any window, meaning Resort
             Hotel's highest-value bookings carry the most early-cancellation exposure.
    
            """)