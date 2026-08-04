import streamlit as st

img_col1, img_col2 = st.columns(2)
with img_col1:
    st.image("images/CancelProtect_logo.svg", width="stretch")

st.title("Conclusion")
st.info("""
This page summarises the key findings, model outcome and recommendations
arising from the CancelProtect project, addressing Business Requirements
1 and 2 for TCS Hotels.
""")

st.header("BR1: Cancellation Patterns and Risk Factors")
st.success("""
* Guest history is the strongest individual risk factor — bookings from
guests with a prior cancellation cancel again 92% of the time, compared
to 34% for guests with a clean history.
* Cancellation risk rises steadily with lead time, from 9% for bookings
made within a week of arrival to 51% for bookings made 90+ days out.
* Non Refund deposit bookings cancel at over 99% — the opposite of what
was expected. This pattern is flagged as an operational concern rather
than a straightforward risk-mitigation signal (see Model Evaluation
 Ablation Study).
* Online TA bookings account for a disproportionately large share of
total cancellations due to booking volume, despite an individual
cancellation rate close to the property-wide average.
* Domestic (PRT) guests cancel at more than twice the rate of
international guests (57% vs. 24%).
* Bookings with no additional needs specified (no special requests or
parking) cancel at more than twice the rate of those with at least one.
""")

st.header("BR2: Predictive Model Outcome")
st.success("""
* The final model (XGBClassifier) achieves 87% recall on the Cancelled
class, exceeding the 80% target set out in the ML Business Case.
* Precision for the Not Cancelled class is 92%, comfortably clearing the
85% threshold required for the model to be considered successful.
* The model is integrated into the Cancellation Predictor dashboard page,
giving the reservations team a live, on-demand risk assessment for any
prospective booking.
""")

st.header("Hypothesis Outcomes")
st.error("""
* **H1 — Rejected:** No-deposit bookings do not cancel more than
deposit-secured bookings; Non Refund bookings cancel at a
near-total rate, the opposite of what was proposed.
""")
st.success("""
* **H2 — Accepted:** Bookings with longer lead times have a higher
cancellation rate than last-minute bookings.
* **H3 — Accepted:** Online TA bookings have a higher cancellation rate
than Direct bookings.
""")

st.header("Recommendations")
st.info("""
* Investigate the Non Refund deposit process directly with the
provider/booking system, given its cancellation rate and uncertain
derivation raise questions about how and when this status is set.
* Prioritise retention outreach for long-lead-time bookings (90+ days),
where cancellation risk is highest and there is the most time to
intervene before arrival.
* Consider targeted engagement strategies for domestic (PRT) guests,
given their notably higher cancellation rate relative to international
guests.
* Use the Cancellation Predictor page as a standard step in reviewing
new group and Online TA bookings, where risk is elevated.
""")

st.header("Limitations and Future Work")
st.warning("""
* `deposit_type` was excluded from the final model due to data leakage
concerns; if its derivation timing can be confirmed with the data
provider, its reinstatement could be reconsidered.
* This iteration focuses on cancellation prediction; future iterations
could add a regression model to estimate the likely cancellation window
of at-risk bookings, to better inform overbooking policy.
* An unsupervised clustering model could further explore guest and
market segmentation beyond the categories currently in the dataset.
* The current dashboard cannot demonstrate reservation lookup
against live data; synthesised mock 'live' data would allow this feature
to be showcased in a future iteration.
""")