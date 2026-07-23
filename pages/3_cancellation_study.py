import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utils.data_management import load_data
from utils.data_processing import create_cancel_profile, cancellation_charts, generate_chart_text

img_col1, img_col2 = st.columns(2)
with img_col1:
    st.image("images/CancelProtect_logo.svg", width="stretch")

st.title("Cancellation Study")

cancellation_profile = create_cancel_profile()
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
main_container.header("Cancellation Rate Analysis")
col1, col2 = main_container.columns([1, 3])

with col1:
    radio_container = st.container(border=True, height="stretch")
    hotel = radio_container.radio("Select Hotel:", ["Combined", "City Hotel", "Resort Hotel"])
    radio_container.markdown("---")
    choice = radio_container.radio("Cancellation rate by:", [
        "Overall", "Market Segment", "Customer Type", "Lead Time", 
        "Distribution Channel", "Arrival Month", "Stay Length", "ADR",
        "Deposit Type"
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