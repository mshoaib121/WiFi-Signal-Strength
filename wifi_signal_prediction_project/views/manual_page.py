import pandas as pd
import streamlit as st

from components import show_signal_card, show_wifi_tips
from model_service import predict_signal


def validate_manual_inputs(values: dict) -> bool:
    for value in values.values():
        if value is None:
            st.warning("Please select all options before prediction.")
            return False

    return True


def manual_prediction_page(model_bundle: dict):
    st.markdown(
        """
        <div class="section-card">
            <div class="badge-blue">Manual Mode</div>
            <div class="section-title">Manual WiFi Signal Prediction</div>
            <div class="section-desc">
                Select WiFi environment values manually. The AI model will predict expected signal strength in dBm.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        distance_m = st.selectbox(
            "Distance from router",
            options=[float(i) for i in range(1, 46)],
            index=None,
            placeholder="Choose distance",
            format_func=lambda value: f"{value:.0f} meters",
        )

        walls = st.selectbox(
            "Walls between device and router",
            options=list(range(0, 7)),
            index=None,
            placeholder="Choose walls",
            format_func=lambda value: f"{value} wall(s)",
        )

        obstacles = st.selectbox(
            "Physical obstacles",
            options=list(range(0, 9)),
            index=None,
            placeholder="Choose obstacles",
            format_func=lambda value: f"{value} obstacle(s)",
        )

    with col2:
        frequency_ghz = st.selectbox(
            "Frequency Band",
            options=[2.4, 5.0],
            index=None,
            placeholder="Choose frequency band",
            format_func=lambda value: f"{value} GHz",
        )

        bandwidth_mhz = st.selectbox(
            "Channel Bandwidth",
            options=[20, 40, 80],
            index=None,
            placeholder="Choose bandwidth",
            format_func=lambda value: f"{value} MHz",
        )

        congestion_percent = st.selectbox(
            "Channel congestion / interference",
            options=list(range(0, 101, 5)),
            index=None,
            placeholder="Choose congestion level",
            format_func=lambda value: f"{value}%",
        )

    values = {
        "distance_m": distance_m,
        "walls": walls,
        "obstacles": obstacles,
        "frequency_ghz": frequency_ghz,
        "bandwidth_mhz": bandwidth_mhz,
        "congestion_percent": congestion_percent,
    }

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Predict Signal Strength", type="primary"):
        if not validate_manual_inputs(values):
            st.markdown("</div>", unsafe_allow_html=True)
            return

        signal_dbm = predict_signal(model_bundle, values)

        st.divider()
        show_signal_card(signal_dbm)
        show_wifi_tips(signal_dbm)

        st.markdown("### Input Data Used by Model")
        st.dataframe(pd.DataFrame([values]), use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)