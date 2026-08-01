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
            * Revenue loss in the form of room revenue and ancillary spend
              (food & beverage for instance)
            * Operations planning is difficult without a clear picture of how
              many guests to expect
            * Occupancy targets are difficult to manage and obtain
            """)

st.write("""
         This app is designed to allow reservations staff to flag high-risk
          cancellation bookings for follow-up or defensive strategies as well
          as allowing management to form an overall picture of cancellations
          and devise defensive policies.
""")

st.divider()
st.header("Dashboard Pages")
st.markdown("""
            * ℹ️ Cancel Protect Overview
                - Provide an overview of the project
            * ❓ Cancellation Predictor
                - Produce a cancellation prediction about a booking prospect
                 based on the input information provided
            * 📊 Cancellation Study
                - Provide business relevant insights about cancellations
            * ✅ Hypothesis Validation
                - Answer the 3 hypotheses laid out in the business
                  understanding
            * 🎯 Model Evaluation
                - Evaluate the ML model's perfomance and describe its main
                  features
""")
st.divider()

with st.expander(label="Business Requirements"):
    st.write("""
            **BR1:** TCS Hotels wants to understand cancellation patterns,
              trends and guest behaviour across their 2 Portuguese properties
              in order to identify risk factors and develop more effective
              cancellation defence strategies.

             **BR2:** TCS Hotels wants a machine learning model capable of
              predicting the likelihood of a booking cancellation, accessed
              through an operational dashboard that supports the reservations
              team with a prospective booking risk assessor.
    """)

with st.expander(label="Hypotheses"):
    st.write("""
             **H1:** Bookings with no deposit cancel more than deposit-secured
               bookings.

             **H2:** Bookings with longer lead times have a higher cancellation
               rate than last-minute bookings.

             **H3:** Bookings made through the Online TA market segment have a
             higher cancellation rate than Direct bookings.

    """)

st.divider()

st.header("How to use CancelProtect")
st.markdown("""
            * Navigate to the Cancel Predict page
            * :blue-badge[Prospective Booking]
                * Enter values in all form inputs
                * Click the "Predict" button
                * Interpret the results
""")

st.divider()

with st.expander(label="Dashboard Limitations"):
    st.warning("""
               * This dashboard is a prototype for demonstration and user
                 testing purposes
               * The dashboard is designed to demonstrate the functionality
                 of the final, integrated product
               * The model has not yet been tuned for production accuracy
               * The dashboard currently has no security layer
    """)

st.write("""
         For more information, please read the project's
           [README](https://github.com/geraldine-mor/cancel-protect) file
""")
