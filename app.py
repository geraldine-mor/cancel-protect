import streamlit as st

st.set_page_config(page_title="Cancel Protect", page_icon="🏢", layout="wide")

pg = st.navigation([
    st.Page("app_pages/1_overview.py",
            title="Cancel Protect Overview", icon="ℹ️"),
    st.Page("app_pages/2_cancel_predict.py",
            title="Cancellation Predictor", icon="❓"),
    st.Page("app_pages/3_cancellation_study.py",
            title="Cancellation Study", icon="📊"),
    st.Page("app_pages/4_hypothesis_validation.py",
            title="Hypothesis Validation", icon="✅"),
    st.Page("app_pages/5_model_evaluation.py",
            title="Model Evaluation", icon="🎯"),
    st.Page("app_pages/project_conclusion.py",
            title="Project Conclusion", icon="🏢")
])

pg.run()
