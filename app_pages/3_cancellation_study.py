import streamlit as st
from src.data_management import load_clean
from src.data_processing import (create_cancel_profile, generate_chart_text,
                                 build_guest_profile, style_guest_profile)
from src.charts import (cancellation_charts, cancel_window_rate,
                        cancel_value_rate, pps_features,
                        correlation_comparison)

img_col1, img_col2 = st.columns(2)
with img_col1:
    st.image("images/CancelProtect_logo.svg", width="stretch")

st.title("Cancellation Study")
st.info("""
This page explores cancellation patterns across TCS Hotels' two
properties to assess potential risk factors.
""")

cancellation_profile = create_cancel_profile("Combined")
clean_df = load_clean()

kpi_container = st.container(border=True)
kpi_container.header("KPIs")
kpi_container.write(
    f"* Total bookings analysed: {len(clean_df)}\n"
    f"* Overall Cancellation Rate: {clean_df['is_canceled'].mean():.0%}\n"
    f"* Average Room Revenue Per Cancelled Booking: "
    f"€{cancellation_profile['Estimated Booking Value'].mean():.2f}\n"
)

main_container = st.container(border=False)
main_container.header("Cancellation Rate Comparison")
col1, col2 = main_container.columns([1, 3])

with col1:
    radio_container = st.container(border=True, height="stretch")
    hotel = radio_container.radio(
        "Select Hotel:", ["Combined", "City Hotel", "Resort Hotel"])
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
        cancellation_charts(selection["hotel"], selection["choice"])

text_container = main_container.container(border=True)
text_container.write(generate_chart_text(selection["hotel"],
                                         selection["choice"]))

with st.expander(label="Cancellation Timing & Value"):
    col1, col2 = st.columns(spec=2, gap="medium")
    select_hotel = st.pills(
        "Choose Property:",
        ["Combined", "City Hotel", "Resort Hotel"],
        default="Combined")
    with col1:
        cancel_window_rate(select_hotel)

    with col2:
        cancel_value_rate(select_hotel)

    if select_hotel == "Combined":
        st.write("""
            Cancellation volume rises steadily with notice window across both
             properties - long-range cancellations (90+ days out) are the most
             common. Booking value is broadly similar across windows, though
             short- and long-range cancellations include a higher share of
              high-value outliers than last-minute ones.
            """)
    elif select_hotel == "City Hotel":
        st.write("""
            At the City Hotel, cancellation volume rises steadily with notice
             window, with long-range cancellations most common. Booking value
             stays fairlyconsistent across windows. If anything, long-range
             cancellations trend slightly lower in value than short- or
             mid-range ones, so City Hotel's furthest-out cancellations aren't
             generally its costliest.
        """)
    elif select_hotel == "Resort Hotel":
        st.write("""
            At the Resort Hotel, cancellation volume rises steadily with notice
             window, with long-range cancellations most common. Unlike City
             Hotel, booking value here increases with notice window too -
             long-range cancellations show the widest spread and thes
             highest-value outlier of any window, meaning Resort Hotel's
             highest-value bookings carry the most early-cancellation exposure.
        """)

with st.expander(label="Correlation Study and Features of Interest"):
    st.write("""Linear correlation analysis (Pearson and Spearman) showed weak
     relationships between individual features and cancellation outcome, with
     no feature reaching ±0.4""")

    correlation_comparison(clean_df)

    st.write("""
    However, Predictive Power Score analysis revealed several features —
     notably deposit type*, country, agent, and ADR — with meaningful
     non-linear predictive relationships not captured by linear correlation
     alone. This indicates that cancellation risk is driven more by specific
     categorical thresholds and subgroup effects (e.g. non-refundable
     deposits*, repeat-cancellation history) than by smooth linear trends.
    """)
    pps_features(clean_df)
    st.info("""
        *Despite its apparent importance, after extensive research, Deposit
         Type was removed from the dataset prior to final modelling due to
         it having uncertain provenance and its potential to act as a proxy
         for "is_canceled" see
         [model evaluation page](/model_evaluation#deposit-type-ablation-study)
    """)

guest_profile = build_guest_profile(clean_df)

with st.expander(label="Guest Behaviour and Booking Profile"):
    container = st.container(border=False)
    container.write("This summary reflects both properties combined, drawing"
                    " together the risk factors explored throughout this page"
                    " into a single guest profile")
    container.table(style_guest_profile(guest_profile))
    container.write("""
    The table breaks the guest profile down into individual risk factors,
    several of which are explored in more depth in the summary below.
    """)

st.info("""
It is indicated that:

* A cancelled booking is most strongly linked to guest history - bookings
 from guests with a prior cancellation are cancelled again 92% of the time,
 compared to 34% for guests with a clean history.
* A cancelled booking typically has a longer lead time - cancellation rate
 rises steadily from 9% for bookings made within a week of arrival to 51%
 for bookings made 90+ days out.
* A Group market segment booking has a 61% chance of cancellation - the
 highest of any segment.
* A cancelled booking typically comes from a guest with no additional needs
 specified - bookings with special requests or parking cancel at less than
 half the rate of those without (20% vs. 50%).
* A cancelled booking is more than twice as likely to originate from a
 domestic (PRT) guest than an international one - 56% vs. 24%.
""")
