import streamlit as st
from utils.data_management import load_data

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
    children = st.number_input("Children", min_value=1, max_value=4, step=1)

with col7:
    babies = st.number_input("Babies", min_value=1, max_value=3, step=1)

with col8:
    meal = st.selectbox("Meal Plan", ["Bed & Breakfast", "Half Board", "Full Board", "Room Only"])
