import streamlit as st

from wifi_utils import classify_signal, optimization_tips


def show_signal_card(signal_dbm: float):
    quality = classify_signal(signal_dbm)

    if signal_dbm >= -60:
        status = "Stable"
    elif signal_dbm >= -75:
        status = "Usable"
    else:
        status = "Weak"

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Predicted Signal", f"{signal_dbm} dBm")

    with col2:
        st.metric("Signal Quality", quality)

    with col3:
        st.metric("Network Status", status)

    if quality in ["Excellent", "Good"]:
        st.success(f"Result: {quality} signal. Your WiFi connection should work well.")
    elif quality == "Fair":
        st.warning("Result: Fair signal. Internet can work, but speed may drop sometimes.")
    else:
        st.error("Result: Weak signal. Connection drops and slow speed may happen.")


def show_wifi_tips(signal_dbm: float):
    st.markdown("### Optimization Tips")

    for tip in optimization_tips(signal_dbm):
        st.markdown(
            f'<div class="tip-item">✅ {tip}</div>',
            unsafe_allow_html=True,
        )