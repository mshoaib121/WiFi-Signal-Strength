import random
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


def get_demo_wifi_data():
    signal = random.choice([-48, -50, -52, -55, -58, -60, -62])
    signal_percent = int(max(0, min(100, 2 * (signal + 100))))

    return {
        "ssid": "Demo WiFi Network",
        "rssi_dbm": float(signal),
        "signal_percent": signal_percent,
        "frequency_ghz": 2.4,
    }


def realtime_prediction_page():
    st.markdown(
        """
        <div class="section-card">
            <div class="badge-green">Real-Time Mode</div>
            <div class="section-title">Real-Time WiFi Signal Prediction</div>
            <div class="section-desc">
                This mode uses actual live WiFi signal when running locally. On Streamlit Cloud, demo live values are shown.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    info = get_wifi_info()

    is_live_available = info.rssi_dbm is not None

    if is_live_available:
        ssid = info.ssid
        current_signal = float(info.rssi_dbm)
        signal_percent = info.signal_percent
        frequency_ghz = info.frequency_ghz
        mode_label = "Local Live Mode"
    else:
        demo_data = get_demo_wifi_data()
        ssid = demo_data["ssid"]
        current_signal = demo_data["rssi_dbm"]
        signal_percent = demo_data["signal_percent"]
        frequency_ghz = demo_data["frequency_ghz"]
        mode_label = "Cloud Demo Mode"

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.caption(mode_label)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("SSID", ssid)

    with col2:
        st.metric("Current Signal", f"{current_signal} dBm")

    with col3:
        st.metric("Signal Percentage", f"{signal_percent}%")

    with col4:
        st.metric("Frequency", f"{frequency_ghz} GHz")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Refresh Live Prediction", type="primary"):
        if is_live_available:
            with st.spinner("Reading actual live WiFi signal..."):
                sampled_info, avg_rssi = get_live_wifi_sample(samples=4, delay_seconds=0.35)

            if avg_rssi is None:
                live_prediction = current_signal
                chart_current_signal = current_signal
            else:
                live_prediction = float(avg_rssi)
                chart_current_signal = (
                    sampled_info.rssi_dbm
                    if sampled_info is not None and sampled_info.rssi_dbm is not None
                    else live_prediction
                )
        else:
            demo_data = get_demo_wifi_data()
            live_prediction = demo_data["rssi_dbm"]
            chart_current_signal = live_prediction + random.choice([-1, 0, 1])

        st.divider()

        show_signal_card(live_prediction)

        st.markdown("### Live Signal Reading")

        chart_df = pd.DataFrame(
            {
                "Type": ["Current Signal", "Average Live Signal"],
                "Signal dBm": [chart_current_signal, live_prediction],
            }
        )

        st.bar_chart(
            chart_df,
            x="Type",
            y="Signal dBm",
            use_container_width=True,
        )

        show_wifi_tips(live_prediction)

    st.markdown("</div>", unsafe_allow_html=True)
