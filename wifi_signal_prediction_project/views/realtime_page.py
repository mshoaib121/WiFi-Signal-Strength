import time
import pandas as pd
import streamlit as st
import random
import os

from components import show_signal_card, show_wifi_tips
from wifi_utils import get_wifi_info


# -------------------------------
# Detect Cloud Environment
# -------------------------------
def is_streamlit_cloud():
    return os.getenv("STREAMLIT_SERVER_PORT") is not None


# -------------------------------
# Live Sampling Function (SAFE)
# -------------------------------
def get_live_wifi_sample(samples: int = 4, delay_seconds: float = 0.35):
    readings = []
    last_info = None

    for _ in range(samples):

        # CLOUD MODE → simulate
        if is_streamlit_cloud():
            class FakeInfo:
                ssid = "Demo_WiFi_Network"
                rssi_dbm = random.randint(-85, -35)
                signal_percent = random.randint(40, 95)
                frequency_ghz = 2.4

            current_info = FakeInfo()

        # LOCAL MODE → real WiFi
        else:
            current_info = get_wifi_info()

        last_info = current_info

        if current_info.rssi_dbm is not None:
            readings.append(float(current_info.rssi_dbm))

        time.sleep(delay_seconds)

    avg_rssi = round(sum(readings) / len(readings), 2) if readings else None

    return last_info, avg_rssi


# -------------------------------
# MAIN PAGE
# -------------------------------
def realtime_prediction_page():

    st.markdown(
        """
        <div class="section-card">
            <div class="badge-green">Real-Time Mode</div>
            <div class="section-title">Real-Time WiFi Signal Prediction</div>
            <div class="section-desc">
                This mode shows live WiFi signal (real on local, simulated on cloud).
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------------
    # GET DATA (SAFE)
    # -------------------------------
    info = get_wifi_info() if not is_streamlit_cloud() else None

    if is_streamlit_cloud():
        info = type("obj", (), {
            "ssid": "Demo_WiFi_Network",
            "rssi_dbm": random.randint(-85, -35),
            "signal_percent": random.randint(40, 95),
            "frequency_ghz": 2.4
        })

    # -------------------------------
    # UI DISPLAY
    # -------------------------------
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("SSID", info.ssid)

    with col2:
        st.metric("Current Signal",
                  f"{info.rssi_dbm} dBm" if info.rssi_dbm else "N/A")

    with col3:
        st.metric("Signal Percentage",
                  f"{info.signal_percent}%" if info.signal_percent else "N/A")

    with col4:
        st.metric("Frequency", f"{info.frequency_ghz} GHz")

    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------
    # BUTTON ACTION
    # -------------------------------
    if st.button("Refresh Live Prediction", type="primary"):

        with st.spinner("Reading live WiFi signal..."):
            sampled_info, avg_rssi = get_live_wifi_sample()

        if avg_rssi is None:
            st.error("Could not read WiFi signal.")
            return

        st.divider()

        show_signal_card(avg_rssi)

        st.markdown("### Live Signal Reading")

        chart_df = pd.DataFrame({
            "Type": ["Current Signal", "Average Signal"],
            "Signal dBm": [
                sampled_info.rssi_dbm,
                avg_rssi
            ],
        })

        st.bar_chart(chart_df, x="Type", y="Signal dBm")

        show_wifi_tips(avg_rssi)
