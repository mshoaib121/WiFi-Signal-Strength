import time

import pandas as pd
import streamlit as st

from components import show_signal_card, show_wifi_tips
from wifi_utils import get_wifi_info


def get_live_wifi_sample(samples: int = 4, delay_seconds: float = 0.35):
    readings = []
    last_info = None

    for _ in range(samples):
        current_info = get_wifi_info()
        last_info = current_info

        if current_info.rssi_dbm is not None:
            readings.append(float(current_info.rssi_dbm))

        time.sleep(delay_seconds)

    if readings:
        avg_rssi = round(sum(readings) / len(readings), 2)
    else:
        avg_rssi = None

    return last_info, avg_rssi


def realtime_prediction_page():
    st.markdown(
        """
        <div class="section-card">
            <div class="badge-green">Real-Time Mode</div>
            <div class="section-title">Real-Time WiFi Signal Prediction</div>
            <div class="section-desc">
                This mode uses actual live WiFi signal from your device.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    info = get_wifi_info()

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("SSID", info.ssid)

    with col2:
        st.metric(
            "Current Signal",
            f"{info.rssi_dbm} dBm" if info.rssi_dbm is not None else "N/A",
        )

    with col3:
        st.metric(
            "Signal Percentage",
            f"{info.signal_percent}%" if info.signal_percent is not None else "N/A",
        )

    with col4:
        st.metric("Frequency", f"{info.frequency_ghz} GHz")

    if info.rssi_dbm is None:
        st.error("Live WiFi signal could not be captured. Please connect to WiFi and try again.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Refresh Live Prediction", type="primary"):
        with st.spinner("Reading actual live WiFi signal..."):
            sampled_info, avg_rssi = get_live_wifi_sample(samples=4, delay_seconds=0.35)

        if avg_rssi is None:
            st.error("Could not read live RSSI value. Please check WiFi connection.")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        live_prediction = float(avg_rssi)

        st.divider()

        show_signal_card(live_prediction)

        st.markdown("### Live Signal Reading")

        chart_df = pd.DataFrame(
            {
                "Type": ["Current Signal", "Average Live Signal"],
                "Signal dBm": [
                    sampled_info.rssi_dbm if sampled_info.rssi_dbm is not None else live_prediction,
                    live_prediction,
                ],
            }
        )

        st.bar_chart(chart_df, x="Type", y="Signal dBm")

        show_wifi_tips(live_prediction)

    st.markdown("</div>", unsafe_allow_html=True)