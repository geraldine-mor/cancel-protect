import streamlit as st
from utils.data_management import load_clean
from utils.data_processing import hypothesis_1_crosstab
from utils.charts import (hypothesis_bar_plot, hypothesis_2_plot,
                          hypothesis_3_plot)

df = load_clean()

img_col1, img_col2 = st.columns(2)
with img_col1:
    st.image("images/CancelProtect_logo.svg", width="stretch")

st.title("Hypothesis Validation")
st.info("""
This page explores the results of the project's hyposthesis testing against
the hypotheses laid out in the initial business case.
""")

tab1, tab2, tab3 = st.tabs(["Hypothesis 1", "Hypothesis 2", "Hypothesis 3"])

with tab1:
    st.subheader("Hypothesis 1: We suspect that no deposit bookings cancel "
                 "more than deposit secured bookings")

    st.error("**Hypothesis Result: Rejected.** The relationship exists, "
             "but runs opposite to what was proposed.")

    st.markdown(
        "A Chi-Square test confirmed a statistically significant "
        "relationship between `deposit_type` and cancellation "
        "(p < 0.001), with a moderate effect size (Cramer's V = 0.48)."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "However, the direction is inverted from what H1 proposed: rather"
            " than deposit-secured bookings showing lower cancellation risk,"
            " **Non Refund** bookings cancel at close to 100% - the highest "
            "rate of any group in the dataset."
        )

        st.markdown(
            "A cancellation rate this extreme suggests Non Refund is unlikely"
            " to reflect genuine guest commitment. It more plausibly reflects "
            "an internal booking or operational process - which is also "
            "why the feature was excluded from the predictive model (see [Model"
            " Evaluation page](/model_evaluation#deposit-type-ablation-study)) "
            "despite its strength as a descriptive signal."
        )

    with col2:
        st.dataframe(hypothesis_1_crosstab(df),
                     column_config={
                        "not_canceled": st.column_config.NumberColumn(
                            format="percent"),
                        "canceled": st.column_config.NumberColumn(
                            format="percent"),
                    })

    col3, col4, col5 = st.columns([0.2, 0.6, 0.2])
    with col4:
        hypothesis_bar_plot(df)

with tab2:
    st.subheader("Hypothesis 2: Bookings with longer lead times have a " 
                 "higher cancellation rate than last-minute bookings")
    
    st.success("**Hypothesis Result: Accepted.** Longer range bookings " 
               "cancel more than last-minute bookings")
    
    st.markdown(
        "The point-biserial test confirms this relationship is statistically significant "
        "(r = 0.29, p < .001) — a small effect by Cohen's convention, though at the upper " 
        "end of a typical real-world relationship per Gignac and Szodorai (2016)"
        )

    st.markdown(
        "In practical terms, lead time alone won't reliably predict which individual "
        "bookings will cancel, but it remains a useful signal at portfolio level - "
        "cancellation risk rises consistently the further out a booking is made, "
        "which is useful for setting overbooking or deposit policy by booking window."
    )

    col6, col7, col8 = st.columns([0.2, 0.6, 0.2])
    with col7:
        hypothesis_2_plot(df)

with tab3:
    st.subheader("Hypothesis 3: Bookings made through the Online TA market segment have a higher" \
        " cancellation rate than bookings made through the Direct market segment")
        
    st.success("**Hypothesis Result: Accepted.** Online TA bookings have a higher cancelaltion" \
    "rate than direct bookings")

    st.markdown(
        "The Chi-Square test confirms this relationship is statistically significant "
        "(p < 0.001), though with a small effect size (Cramer's V = 0.18) - a weaker "
        "individual predictor than deposit type" 
    )

    st.markdown(
        "Because Online TA is by far the largest booking channel, this small "
        "per-booking effect compounds at volume: Online TA contributes a "
        "disproportionately large share of *all* cancellations dataset-wide, "
        "which is likely why it's often flagged operationally as a major "
        "cancellation source."
        )

    hypothesis_3_plot(df)
