import streamlit as st

from model_service import load_model_bundle
from styles import apply_custom_css
from views.manual_page import manual_prediction_page
from views.realtime_page import realtime_prediction_page


st.set_page_config(
    page_title="AI WiFi Signal Prediction",
    page_icon="📶",
    layout="wide",
)


def show_header():
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">📶 AI-Based Real-Time WiFi Signal Strength Prediction System</div>
            <div class="hero-subtitle">
                A professional dashboard that supports manual AI prediction and actual real-time WiFi signal reading.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_sidebar():
    with st.sidebar:
        st.header("Navigation")

        page = st.radio(
            "Select Mode",
            [
                "Manual Prediction",
                "Real-Time Prediction",
            ],
        )

        st.divider()
        st.caption("Project")
        st.write("AI WiFi Signal Prediction")

        st.caption("Selected Mode")
        st.write(page)

    return page


def main():
    apply_custom_css()
    show_header()

    page = show_sidebar()

    if page == "Manual Prediction":
        model_bundle = load_model_bundle()
        manual_prediction_page(model_bundle)

    elif page == "Real-Time Prediction":
        realtime_prediction_page()


if __name__ == "__main__":
    main()