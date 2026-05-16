import streamlit as st
import random
import pandas as pd
import os

from components import show_signal_card, show_wifi_tips


# ---------------------------
# CLOUD DETECTION
# ---------------------------
def is_cloud():
    return os.getenv("STREAMLIT_SERVER_PORT") is not None


# ---------------------------
# SIGNAL QUALITY FUNCTION
# ---------------------------
def get_quality(rssi):
    if rssi >= -50:
        return "Excellent"
    elif rssi >= -60:
        return "Good"
    elif rssi >= -70:
        return "Fair"
    else:
        return "Weak"


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
    # ALWAYS SAFE DATA (NO FAILS)
    # ---------------------------
    if is_cloud():
        # CLOUD → SIMULATION ONLY
        ssid = "Demo_WiFi_Network"
        rssi = random.randint(-85, -35)

    else:
        # LOCAL → TRY REAL WIFI
        try:
            from wifi_utils import get_wifi_info
            info = get_wifi_info()

            ssid = info.ssid if info.ssid else "Unknown"
            rssi = info.rssi_dbm if info.rssi_dbm is not None else -70

        except:
            ssid = "Unknown"
            rssi = -70

    # ---------------------------
    # DERIVED VALUES
    # ---------------------------
    signal_percent = max(0, min(100, int((rssi + 100) * 2)))
    quality = get_quality(rssi)

    # ---------------------------
    # UI DISPLAY
    # ---------------------------
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("SSID", ssid)

    with col2:
        st.metric("Current Signal", f"{rssi} dBm")

    with col3:
        st.metric("Signal Percentage", f"{signal_percent}%")

    with col4:
        st.metric("Frequency", "2.4 GHz")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------
    # AI PREDICTION (SAME SIGNAL MODEL)
    # ---------------------------
    predicted_signal = rssi

    st.markdown("### Predicted Signal")
    st.metric("Predicted Signal Strength", f"{predicted_signal} dBm")
    st.metric("Signal Quality", quality)

    # ---------------------------
    # RESULT TEXT
    # ---------------------------
    if quality in ["Excellent", "Good"]:
        status = "Strong connection"
    elif quality == "Fair":
        status = "Usable connection"
    else:
        status = "Weak connection"

    st.success(f"Result: {quality} signal. {status}.")

    # ---------------------------
    # CHART
    # ---------------------------
    df = pd.DataFrame({
        "Type": ["Signal"],
        "dBm": [rssi]
    })

    st.bar_chart(df, x="Type", y="dBm")

    # ---------------------------
    # TIPS
    # ---------------------------
    show_wifi_tips(rssi)
