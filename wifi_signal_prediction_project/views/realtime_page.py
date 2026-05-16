import streamlit as st
import random
import os
import pandas as pd

from components import show_signal_card, show_wifi_tips
from wifi_utils import get_wifi_info


# ---------------------------
# Detect Cloud
# ---------------------------
def is_cloud():
    return os.getenv("STREAMLIT_SERVER_PORT") is not None


# ---------------------------
# MAIN PAGE
# ---------------------------
def realtime_prediction_page():

    st.markdown(
        """
        <div class="section-card">
            <div class="badge-green">Real-Time Mode</div>
            <div class="section-title">Real-Time WiFi Signal Prediction</div>
            <div class="section-desc">
                Live signal detection (Real on local, Simulated on cloud)
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------
    # FORCE DATA (IMPORTANT FIX)
    # ---------------------------
    if is_cloud():

        # CLOUD SAFE DATA (NO get_wifi_info)
        info = type("WiFi", (), {
            "ssid": "Demo_WiFi_Network",
            "rssi_dbm": random.randint(-85, -35),
            "signal_percent": random.randint(40, 95),
            "frequency_ghz": 2.4
        })

    else:

        # LOCAL REAL DATA
        info = get_wifi_info()

        # fallback if local fails
        if info.rssi_dbm is None:
            info = type("WiFi", (), {
                "ssid": "Unknown",
                "rssi_dbm": -70,
                "signal_percent": 60,
                "frequency_ghz": 2.4
            })

    # ---------------------------
    # UI (NO N/A EVER)
    # ---------------------------
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("SSID", info.ssid)

    with col2:
        st.metric("Current Signal", f"{info.rssi_dbm} dBm")

    with col3:
        st.metric("Signal Percentage", f"{info.signal_percent}%")

    with col4:
        st.metric("Frequency", f"{info.frequency_ghz} GHz")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------
    # BUTTON
    # ---------------------------
    if st.button("Refresh Live Prediction", type="primary"):

        signal = info.rssi_dbm if info.rssi_dbm else -70

        st.divider()

        show_signal_card(signal)

        df = pd.DataFrame({
            "Type": ["Signal"],
            "dBm": [signal]
        })

        st.bar_chart(df, x="Type", y="dBm")

        show_wifi_tips(signal)
