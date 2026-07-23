import streamlit as st

st.set_page_config(page_title="Cancel Protect", page_icon="🏢", layout="wide")

pg = st.navigation([
    st.Page("pages/1_overview.py", title="Cancel Protect Overview", icon="ℹ️"),
    st.Page("pages/2_cancel_predict.py", title="Cancellation Predictor", icon="❓"),
    st.Page("pages/3_cancellation_study.py", title="Cancellation Study", icon="📊")
])

pg.run()