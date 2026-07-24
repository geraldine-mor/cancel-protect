import streamlit as st

img_col1, img_col2 = st.columns(2)
with img_col1:
    st.image("images/CancelProtect_logo.svg", width="stretch")

st.title("Dashboard Overview")

st.info(
    "**CancelProtect** predicts the likelihood of booking cancellations,"
    " helping **TCS Hotels** reduce revenue loss through proactive retention"
    " and smarter operational planning."
)

st.header("Business Context")

st.markdown("""
            Cancellations pose several problems for hotels: 
            * Revenue loss in the form of room revenue and ancillary spend (food & beverage for instance)  
            * Operations planning is difficult without a clear picture of how many guests to expect  
            * Occupancy targets are difficult to manage and obtain 
            """)

st.write("""
         This app is designed to allow reservations staff to flag high-risk cancellation bookings for follow-up
         as well as allowing management to form an overall picture of cancellations and devise defensive policies.
""")

st.divider()
# ⚠️ Add information about each page 

with st.expander(label="Business Requirements"):
    st.write("""
            **BR1:** TCS Hotels wants to understand cancellation patterns, trends and guest behaviour across 
             their 2 Portuguese properties in order to identify risk factors and develop more effective cancellation 
             defence strategies.

             **BR2:** TCS Hotels wants a machine learning model capable of predicting the likelihood of a booking 
             cancellation, accessed through an operational dashboard that supports the reservations team in three 
             ways: a risk report of upcoming arrivals, individual reservation search and a prospective booking risk assessor.

             **BR3:** TCS Hotels wants to identify distinct guest booking segments with meaningfully different cancellation 
             profiles, in order to better understand the composition of their demand and inform targeted retention strategies.
    """)

with st.expander(label="Hypotheses"):
    st.write("""
             **H1:** Bookings with no deposit cancel more than deposit-secured bookings.

             **H2:** Bookings with longer lead times have a higher cancellation rate than last-minute bookings.

             **H3:** Bookings made through the Online TA market segment have a higher cancellation rate than bookings 
             made through the Direct market segment.

             **H4:** Distinct guest booking segments exist within the data. These segments exhibit meaningfully different
              cancellation rates suggesting cancellation risk is not uniform across the customer base.
    """)

st.divider()

st.header("How to use CancelProtect")
st.markdown("""
            * Navigate to the Cancel Predict page
            * :blue-badge[Prospective Booking] 
                * Enter values in all form inputs
                * Click the "Predict" button
                * Interpret the results
            * :green-badge[Reservation Search]
                * Enter reservation number in the search box
                * Click the "Predict" button
                * Interpret the results
            * :violet-badge[Risk Report]
                * Click the "Generate Report" button 
                * Interpret the output        
""")

st.divider()

# ⚠️ Add expander to contain information about the dataset

with st.expander(label="Dashboard Limitations"):
    st.warning("""
               * This dashboard is a prototype for demonstration and user testing purposes
               * The dashboard is designed to demonstrate the functionality of the final, integrated product
               * The dashboard operates on a small, synthesised mock-data dataset
               * The model has not yet been tuned for production accuracy
               * The dashboard currently has no security layer
    """)

st.write("""
         For more information, please read the project's [README](https://github.com/geraldine-mor/cancel-protect) file
""")